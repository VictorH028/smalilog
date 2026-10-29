"""
Tests del análisis y parcheo de AndroidManifest.xml.

Ejecuta:
    pytest -q tests/manifest_test.py
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from smalilog.manifest import (
    ManifestError,
    parse_manifest,
    patch_manifest,
    run_manifest,
    scan_smali_entries,
)


SAMPLE_MANIFEST = """\
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.demo"
    android:versionCode="7"
    android:versionName="1.7">
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <application
        android:name=".DemoApp"
        android:debuggable="false">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
            <intent-filter>
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <data android:scheme="https" android:host="example.com"
                    android:pathPrefix="/demo" />
            </intent-filter>
        </activity>
        <service android:name=".SyncService" android:exported="false" />
        <receiver android:name=".BootReceiver" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED" />
            </intent-filter>
        </receiver>
        <provider android:name=".DataProvider" android:exported="false"
            android:authorities="com.example.demo.data" />
    </application>
</manifest>
"""


@pytest.fixture
def manifest_path(tmp_path: Path) -> Path:
    path = tmp_path / "AndroidManifest.xml"
    path.write_text(SAMPLE_MANIFEST, encoding="utf-8")
    return path


class TestParseManifest:
    def test_info(self, manifest_path: Path):
        info = parse_manifest(manifest_path)
        assert info.package == "com.example.demo"
        assert info.version_name == "1.7"
        assert info.version_code == "7"
        assert info.application == ".DemoApp"
        assert info.debuggable is False
        assert info.cleartext is None
        assert "android.permission.ACCESS_NETWORK_STATE" in info.permissions
        assert len(info.components) == 4
        assert [c.name for c in info.launchers] == [".MainActivity"]
        assert info.components[0].deep_links() == ["https://example.com/demo"]

    def test_component_flags(self, manifest_path: Path):
        info = parse_manifest(manifest_path)
        by_name = {c.name: c for c in info.components}
        assert by_name[".SyncService"].exported is False
        assert by_name[".BootReceiver"].exported is True
        assert by_name[".DataProvider"].kind == "provider"
        assert by_name[".MainActivity"].launcher is True

    def test_binary_manifest_error(self, tmp_path: Path):
        path = tmp_path / "AndroidManifest.xml"
        path.write_bytes(b"\x03\x00\x08\x00")
        with pytest.raises(ManifestError, match="binario"):
            parse_manifest(path)

    def test_missing_manifest_error(self, tmp_path: Path):
        with pytest.raises(ManifestError, match="No existe"):
            parse_manifest(tmp_path / "no-existe.xml")


class TestPatchManifest:
    def test_adds_internet_and_cleartext(self, manifest_path: Path):
        result = patch_manifest(manifest_path)
        text = manifest_path.read_text(encoding="utf-8")
        assert result.changed is True
        assert result.added_permissions == ["android.permission.INTERNET"]
        assert result.cleartext_changed is True
        assert text.count("android.permission.INTERNET") == 1
        assert 'android:usesCleartextTraffic="true"' in text
        assert manifest_path.with_name("AndroidManifest.xml.bak").exists()

    def test_idempotent(self, manifest_path: Path):
        patch_manifest(manifest_path)
        result = patch_manifest(manifest_path)
        assert result.changed is False
        assert result.added_permissions == []
        assert result.cleartext_changed is False
        text = manifest_path.read_text(encoding="utf-8")
        assert text.count("android:usesCleartextTraffic") == 1

    def test_existing_permission_not_duplicated(self, tmp_path: Path):
        path = tmp_path / "AndroidManifest.xml"
        path.write_text(SAMPLE_MANIFEST.replace(
            '<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />',
            '<uses-permission android:name="android.permission.INTERNET" />',
        ), encoding="utf-8")
        result = patch_manifest(path)
        assert "android.permission.INTERNET" not in result.added_permissions
        assert path.read_text(encoding="utf-8").count(
            "android.permission.INTERNET") == 1

    def test_cleartext_false_is_replaced(self, tmp_path: Path):
        path = tmp_path / "AndroidManifest.xml"
        path.write_text(SAMPLE_MANIFEST.replace(
            'android:debuggable="false"',
            'android:debuggable="false"\n        android:usesCleartextTraffic="false"',
        ), encoding="utf-8")
        result = patch_manifest(path, permissions=[])
        assert result.cleartext_changed is True
        assert 'android:usesCleartextTraffic="true"' in path.read_text(
            encoding="utf-8")

    def test_custom_permission_and_no_cleartext(self, manifest_path: Path):
        result = patch_manifest(
            manifest_path,
            permissions=["android.permission.ACCESS_NETWORK_STATE",
                         "android.permission.POST_NOTIFICATIONS"],
            cleartext=False,
        )
        text = manifest_path.read_text(encoding="utf-8")
        assert result.added_permissions == [
            "android.permission.POST_NOTIFICATIONS"]
        assert "android:usesCleartextTraffic" not in text
        assert text.count("android.permission.ACCESS_NETWORK_STATE") == 1

    def test_dry_run_does_not_write(self, manifest_path: Path):
        before = manifest_path.read_text(encoding="utf-8")
        result = patch_manifest(manifest_path, dry_run=True)
        assert result.changed is True
        assert manifest_path.read_text(encoding="utf-8") == before
        assert not manifest_path.with_name("AndroidManifest.xml.bak").exists()

    def test_output_does_not_touch_source(self, manifest_path: Path, tmp_path: Path):
        output = tmp_path / "AndroidManifest.new.xml"
        result = patch_manifest(manifest_path, output=output)
        assert result.output == output
        assert manifest_path.read_text(encoding="utf-8") == SAMPLE_MANIFEST
        assert output.exists()
        assert "android.permission.INTERNET" in output.read_text(encoding="utf-8")

    def test_network_security_config_warning(self, tmp_path: Path):
        path = tmp_path / "AndroidManifest.xml"
        path.write_text(SAMPLE_MANIFEST.replace(
            'android:debuggable="false"',
            'android:debuggable="false"\n        '
            'android:networkSecurityConfig="@xml/network_security_config"',
        ), encoding="utf-8")
        result = patch_manifest(path)
        assert result.warning is not None


class TestSmaliScan:
    def test_scan_known_base_types(self, tmp_path: Path):
        source = """\
.class public Lcom/example/MainActivity;
.super Landroid/app/Activity;

.method protected onCreate(Landroid/os/Bundle;)V
    .registers 2
    return-void
.end method
"""
        app = """\
.class public Lcom/example/DemoApp;
.super Landroid/app/Application;

.method protected attachBaseContext(Landroid/content/Context;)V
    .registers 2
    return-void
.end method
"""
        smali = tmp_path / "smali" / "com" / "example"
        smali.mkdir(parents=True)
        (smali / "MainActivity.smali").write_text(source, encoding="utf-8")
        (smali / "DemoApp.smali").write_text(app, encoding="utf-8")

        entries = scan_smali_entries(tmp_path)
        by_name = {entry.name: entry for entry in entries}
        assert by_name["Lcom/example/MainActivity;"].kind == "activity"
        assert by_name["Lcom/example/MainActivity;"].on_create is True
        assert by_name["Lcom/example/DemoApp;"].kind == "application"
        assert by_name["Lcom/example/DemoApp;"].attach_base_context is True

    def test_scan_ignores_plain_classes(self, tmp_path: Path):
        smali = tmp_path / "smali"
        smali.mkdir()
        (smali / "Util.smali").write_text(
            ".class public Lcom/example/Util;\n"
            ".super Ljava/lang/Object;\n",
            encoding="utf-8",
        )
        assert scan_smali_entries(tmp_path) == []


class TestManifestCli:
    def test_info_json(self, manifest_path: Path, capsys):
        assert run_manifest(["info", str(manifest_path), "--json"]) == 0
        payload = json.loads(capsys.readouterr().out)
        assert payload["package"] == "com.example.demo"
        assert payload["launchers"] == [".MainActivity"]
        assert len(payload["components"]) == 4

    def test_permissions_json(self, manifest_path: Path, capsys):
        assert run_manifest(["permissions", str(manifest_path), "--json"]) == 0
        payload = json.loads(capsys.readouterr().out)
        assert payload["permissions"] == [
            "android.permission.ACCESS_NETWORK_STATE"]

    def test_fix_cli(self, manifest_path: Path, capsys):
        assert run_manifest(["fix", str(manifest_path)]) == 0
        out = capsys.readouterr().out
        assert "android.permission.INTERNET" in out
        assert "usesCleartextTraffic" in out

    def test_fix_missing_manifest(self, tmp_path: Path, capsys):
        assert run_manifest(["fix", str(tmp_path / "no.xml")]) == 1
        assert "No existe" in capsys.readouterr().out
