"""Tests del instalador y control del agente Renef embebido."""
from __future__ import annotations

import base64
from pathlib import Path

import pytest

from smalilog.renef._agent import (
    ACTION,
    AgentError,
    build_broadcast_argv,
    detect_lib_root,
    detect_package,
    detect_smali_root,
    encode_script,
    install_payload,
    patch_agent_manifest,
)
from smalilog.renef._cli import run_renef

MANIFEST = """\
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.demo">
    <application android:label="Demo">
        <activity android:name=".MainActivity" />
    </application>
</manifest>
"""


def _payload(tmp_path: Path) -> Path:
    root = tmp_path / "payload"
    smali = root / "smali" / "com" / "smalilog" / "agent"
    smali.mkdir(parents=True)
    (smali / "AgentReceiver.smali").write_text(
        ".class public Lcom/smalilog/agent/AgentReceiver;\n", encoding="utf-8")
    lib = root / "lib" / "arm64-v8a"
    lib.mkdir(parents=True)
    (lib / "libagent.so").write_bytes(b"\x7fELF-fake-agent")
    return root


def _app(tmp_path: Path, *, nested: bool = False, smali: bool = True) -> Path:
    root = tmp_path / "apk"
    root.mkdir()
    (root / "AndroidManifest.xml").write_text(MANIFEST, encoding="utf-8")
    if smali:
        (root / "smali" / "classes" / "com" / "example").mkdir(parents=True)
    if nested:
        (root / "root" / "lib" / "arm64-v8a").mkdir(parents=True)
    return root


class TestManifestPatch:
    def test_adds_receiver_permission_and_cleartext(self):
        text, added, cleartext, warnings = patch_agent_manifest(MANIFEST)
        assert "com.smalilog.agent.AgentReceiver" in text
        assert 'android:exported="true"' in text
        assert ACTION in text
        assert added == ["android.permission.INTERNET"]
        assert cleartext is True
        assert warnings == []
        assert 'android:usesCleartextTraffic="true"' in text

    def test_idempotent(self):
        first, _, _, _ = patch_agent_manifest(MANIFEST)
        second, added, cleartext, _ = patch_agent_manifest(first)
        assert second.count("AgentReceiver") == 1
        assert second.count("android.permission.INTERNET") == 1
        assert second.count("usesCleartextTraffic") == 1
        assert added == []
        assert cleartext is False

    def test_no_application_error(self):
        with pytest.raises(AgentError, match="application"):
            patch_agent_manifest("<manifest package=\"x\" />")

    def test_self_closing_application(self):
        text = (
            '<manifest xmlns:android="http://schemas.android.com/apk/res/android"'
            ' package="com.example.demo">'
            '<application android:label="Demo" /></manifest>'
        )
        patched, _, _, _ = patch_agent_manifest(text)
        assert "<application" in patched
        assert "</application>" in patched
        assert "AgentReceiver" in patched

    def test_network_security_warning(self):
        text = MANIFEST.replace(
            "<application ",
            '<application android:networkSecurityConfig="@xml/network" ')
        _, _, _, warnings = patch_agent_manifest(text)
        assert warnings


class TestInstall:
    def test_installs_payload(self, tmp_path: Path):
        payload = _payload(tmp_path)
        app = _app(tmp_path, nested=True)
        report = install_payload(app, payload_dir=payload)

        assert report.changed
        assert (app / "smali" / "classes" / "com" / "smalilog" / "agent"
                / "AgentReceiver.smali").is_file()
        assert (app / "root" / "lib" / "arm64-v8a" / "libagent.so").read_bytes() \
            == b"\x7fELF-fake-agent"
        text = (app / "AndroidManifest.xml").read_text(encoding="utf-8")
        assert "AgentReceiver" in text
        assert "android.permission.INTERNET" in text
        assert "usesCleartextTraffic" in text
        backup = tmp_path / ".apk.smalilog-backup" / "AndroidManifest.xml"
        assert backup.is_file()
        assert not (app / "AndroidManifest.xml.bak").exists()

    def test_idempotent(self, tmp_path: Path):
        payload = _payload(tmp_path)
        app = _app(tmp_path)
        install_payload(app, payload_dir=payload)
        report = install_payload(app, payload_dir=payload)
        assert report.changed is False
        assert report.skipped

    def test_conflict_without_force(self, tmp_path: Path):
        payload = _payload(tmp_path)
        app = _app(tmp_path)
        target = app / "smali" / "classes" / "com" / "smalilog" / "agent"
        target.mkdir(parents=True)
        (target / "AgentReceiver.smali").write_text("otro", encoding="utf-8")
        with pytest.raises(AgentError, match="--force"):
            install_payload(app, payload_dir=payload)

    def test_force_and_no_backup(self, tmp_path: Path):
        payload = _payload(tmp_path)
        app = _app(tmp_path)
        target = app / "smali" / "classes" / "com" / "smalilog" / "agent"
        target.mkdir(parents=True)
        (target / "AgentReceiver.smali").write_text("otro", encoding="utf-8")
        report = install_payload(
            app, payload_dir=payload, force=True, backup=False)
        assert report.updated
        assert not (target / "AgentReceiver.smali.bak").exists()
        assert not (tmp_path / ".apk.smalilog-backup").exists()

    def test_rejects_binary_manifest(self, tmp_path: Path):
        payload = _payload(tmp_path)
        app = _app(tmp_path)
        (app / "AndroidManifest.xml").write_bytes(b"\x03\x00\x08\x00")
        with pytest.raises(AgentError, match="binario"):
            install_payload(app, payload_dir=payload)

    def test_rejects_source_project(self, tmp_path: Path):
        payload = _payload(tmp_path)
        app = _app(tmp_path, smali=False)
        with pytest.raises(AgentError, match="descompilada"):
            install_payload(app, payload_dir=payload)

    def test_missing_lib_error(self, tmp_path: Path):
        payload = _payload(tmp_path)
        (payload / "lib" / "arm64-v8a" / "libagent.so").unlink()
        app = _app(tmp_path)
        with pytest.raises(AgentError, match="libagent.so"):
            install_payload(app, payload_dir=payload)


class TestDetection:
    def test_detect_package(self, tmp_path: Path):
        app = _app(tmp_path)
        assert detect_package(app) == "com.example.demo"

    def test_detect_smali_editor(self, tmp_path: Path):
        app = _app(tmp_path)
        assert detect_smali_root(app) == app / "smali" / "classes"

    def test_detect_smali_apktool(self, tmp_path: Path):
        app = _app(tmp_path, smali=False)
        (app / "smali" / "com" / "example").mkdir(parents=True)
        assert detect_smali_root(app) == app / "smali"

    def test_detect_lib_nested(self, tmp_path: Path):
        app = _app(tmp_path, nested=True)
        assert detect_lib_root(app) == app / "root" / "lib"


class TestCommandLine:
    def test_broadcast_local(self):
        argv = build_broadcast_argv(
            "com.example.demo", "EXEC", b64="YWJj", host="10.0.0.5", port=9999)
        assert argv[0] == "am"
        assert argv[argv.index("-f") + 1] == "0x20"
        assert argv[argv.index("-a") + 1] == ACTION
        assert "com.example.demo/com.smalilog.agent.AgentReceiver" in argv
        assert argv[argv.index("--es") + 1] == "op"
        assert "10.0.0.5" in argv
        assert "9999" in argv

    def test_broadcast_adb(self):
        argv = build_broadcast_argv(
            "com.example.demo", "STATUS", adb=True, serial="emulator-5554")
        assert argv[:4] == ["adb", "-s", "emulator-5554", "shell"]
        assert "STATUS" in argv

    def test_encode_script_bytes(self):
        assert base64.b64decode(encode_script(b"print('x')")) == b"print('x')"

    def test_encode_script_too_large(self):
        with pytest.raises(AgentError, match="demasiado grande"):
            encode_script(b"x" * (256 * 1024 + 1))

    def test_install_cli_dry_run(self, tmp_path: Path, capsys):
        payload = _payload(tmp_path)
        app = _app(tmp_path)
        rc = run_renef([
            "install", str(app), "--payload-dir", str(payload), "--dry-run",
        ])
        assert rc == 0
        captured = capsys.readouterr()
        assert "Dry-run" in captured.out
        assert not (app / "smali" / "classes" / "com" / "smalilog").exists()

    def test_runtime_cli_dry_run(self, tmp_path: Path, capsys):
        app = _app(tmp_path)
        rc = run_renef([
            "runtime", "exec", "--code", "print('hola')",
            "--apk-dir", str(app), "--dry-run",
        ])
        assert rc == 0
        captured = capsys.readouterr()
        assert "am broadcast" in captured.out
        assert "com.example.demo/com.smalilog.agent.AgentReceiver" in captured.out
