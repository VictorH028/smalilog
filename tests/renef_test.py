"""Tests del puente Renef → Smali.

Ejecuta:
    pytest -q tests/renef_test.py
"""
from __future__ import annotations

from pathlib import Path

import pytest

from smalilog.renef import apply_report, parse_script, run_renef
from smalilog.renef._apply import report_lines

SAMPLE_SMALI = """\
.class public Lcom/example/App;
.super Ljava/lang/Object;

.method public static isRooted()Z
    .registers 1
    const/4 v0, 0x1
    return v0
.end method

.method public static score()J
    .registers 2
    const-wide/16 v0, 0x2
    return-wide v0
.end method

.method public static label()Ljava/lang/String;
    .registers 1
    const-string v0, "original"
    return-object v0
.end method

.method public static observe(I)V
    .registers 2
    return-void
.end method
"""


@pytest.fixture
def smali_tree(tmp_path: Path) -> Path:
    target = tmp_path / "smali" / "com" / "example"
    target.mkdir(parents=True)
    (target / "App.smali").write_text(SAMPLE_SMALI, encoding="utf-8")
    return tmp_path


def _write_script(tmp_path: Path, source: str) -> Path:
    path = tmp_path / "hook.lua"
    path.write_text(source, encoding="utf-8")
    return path


class TestParseScript:
    def test_safe_hook_skip(self):
        report = parse_script("""
safe_hook("com/example/App", "check", "()Z", {
    onEnter = function(args) args.skip = true end
}, "Check")
""")
        recipe = report.recipes[0]
        assert recipe.action.value == "stub"
        assert recipe.class_name == "com/example/App"
        assert recipe.method == "check"
        assert recipe.signature == "()Z"
        assert recipe.label == "Check"

    def test_safe_hook_return_constant(self):
        report = parse_script("""
hook("com/example/App", "isRooted", "()Z", {
    onLeave = function(retval) return false end
})
""")
        recipe = report.recipes[0]
        assert recipe.action.value == "stub"
        assert recipe.return_value is False

    def test_string_return_is_constant(self):
        report = parse_script("""
hook("com/example/App", "name", "()Ljava/lang/String;", {
    onLeave = function(retval) return "oculto" end
})
""")
        recipe = report.recipes[0]
        assert recipe.action.value == "stub"
        assert recipe.return_value == "oculto"

    def test_return_nil_is_not_stub(self):
        report = parse_script("""
hook("com/example/App", "name", "()Z", {
    onLeave = function(retval) return nil end
})
""")
        assert report.recipes[0].action.value == "log_exit"

    def test_observation_both(self):
        report = parse_script("""
hook("com/example/App", "run", "()V", {
    onEnter = function(args) print("in") end,
    onLeave = function(retval) print("out") end
})
""")
        assert report.recipes[0].action.value == "log_both"

    def test_native_hook_is_reported(self):
        report = parse_script("""
hook("libc.so", 0x1234, { onLeave = function(retval) return 1 end })
""")
        recipe = report.recipes[0]
        assert recipe.action.value == "native"
        assert "libc.so" in recipe.reason

    def test_runtime_features(self):
        report = parse_script("""
local m = Module.find("libc.so")
local list = Memory.scan("abc")
""")
        assert any("Module" in f for f in report.runtime_features)
        assert any("Memory" in f for f in report.runtime_features)

    def test_constructor_stub_blocked(self):
        report = parse_script("""
hook("com/example/App", "<init>", "()V", {
    onEnter = function(args) args.skip = true end
})
""")
        recipe = report.recipes[0]
        assert recipe.action.value == "unsupported"
        assert "constructor" in recipe.reason

    def test_comments_are_ignored(self):
        report = parse_script("""
-- hook("com/example/App", "fake", "()Z", { onLeave = function() return true end })
hook("com/example/App", "real", "()Z", { onLeave = function() return true end })
""")
        assert len(report.recipes) == 1
        assert report.recipes[0].method == "real"


class TestApply:
    def test_apply_stubs_and_observation(self, smali_tree):
        script = """
hook("com/example/App", "isRooted", "()Z", {
    onLeave = function(retval) return false end
})
hook("com/example/App", "score", "()J", {
    onLeave = function(retval) return 0 end
})
hook("com/example/App", "label", "()Ljava/lang/String;", {
    onLeave = function(retval) return "oculto" end
})
hook("com/example/App", "observe", "(I)V", {
    onEnter = function(args) print("in") end,
    onLeave = function(retval) print("out") end
})
hook("libc.so", 0x1234, { onLeave = function(retval) return 1 end })
"""
        result = apply_report(parse_script(script), smali_tree, backup=False)
        assert result.applied == 4
        assert result.failed == 0
        assert result.skipped == 1

        content = (smali_tree / "smali" / "com" / "example" / "App.smali").read_text()
        assert content.count("Renef STUB inyectado") == 3
        assert 'const-string v1, "oculto"' in content
        assert "const-wide/16 v2, 0x0" in content
        assert "traceIn" in content
        assert "traceOutVoid" in content

    def test_apply_stub_with_locals_directive(self, tmp_path):
        target = tmp_path / "smali" / "com" / "example"
        target.mkdir(parents=True)
        path = target / "App.smali"
        path.write_text("""\
.class public Lcom/example/App;

.method public static check(Ljava/lang/String;)Z
    .locals 1
    const/4 v0, 0x1
    return v0
.end method
""", encoding="utf-8")

        report = parse_script("""
hook("com/example/App", "check", "(Ljava/lang/String;)Z", {
    onLeave = function(retval) return false end
})
""")
        assert apply_report(report, tmp_path, backup=False).applied == 1
        content = path.read_text()
        assert ".registers 3" in content
        assert "const/4 v1, 0x0" in content
        assert "return v1" in content

    def test_apply_is_idempotent(self, smali_tree):
        report = parse_script("""
hook("com/example/App", "isRooted", "()Z", {
    onLeave = function(retval) return false end
})
""")
        assert apply_report(report, smali_tree, backup=False).applied == 1
        assert apply_report(report, smali_tree, backup=False).applied == 1
        content = (smali_tree / "smali" / "com" / "example" / "App.smali").read_text()
        assert content.count("Renef STUB inyectado") == 1

    def test_missing_class_is_skipped(self, smali_tree):
        report = parse_script("""
hook("com/example/NoExiste", "x", "()Z", {
    onLeave = function(retval) return true end
})
""")
        result = apply_report(report, smali_tree, backup=False)
        assert result.applied == 0
        assert result.skipped == 1
        assert "no encontrada" in report_lines(result)[0]

    def test_dry_run_does_not_write(self, smali_tree):
        report = parse_script("""
hook("com/example/App", "isRooted", "()Z", {
    onLeave = function(retval) return false end
})
""")
        path = smali_tree / "smali" / "com" / "example" / "App.smali"
        before = path.read_text()
        result = apply_report(report, smali_tree, dry_run=True)
        assert result.applied == 1
        assert path.read_text() == before
        assert not path.with_suffix(".smali.bak").exists()

    def test_only_filter(self, smali_tree):
        report = parse_script("""
hook("com/example/App", "isRooted", "()Z", {
    onLeave = function(retval) return false end
})
hook("com/example/App", "score", "()J", {
    onLeave = function(retval) return 0 end
})
""")
        result = apply_report(report, smali_tree, only="isRooted", backup=False)
        assert result.applied == 1
        content = (smali_tree / "smali" / "com" / "example" / "App.smali").read_text()
        assert content.count("Renef STUB inyectado") == 1


class TestExamples:
    def test_demo_script_is_valid(self):
        path = (Path(__file__).resolve().parents[1]
                / "build_payloads" / "renef_demo.lua")
        report = parse_script(path.read_text(encoding="utf-8"), path)
        assert len(report.applicable) == 3
        actions = {r.action.value for r in report.applicable}
        assert actions == {"stub", "log_both"}


class TestCli:
    def test_presets_lists(self, capsys):
        assert run_renef(["presets"]) == 0
        out = capsys.readouterr().out
        assert "ssl" in out
        assert "root" in out

    def test_parse_preset(self, capsys):
        assert run_renef(["parse", "--preset", "ssl"]) == 0
        out = capsys.readouterr().out
        assert "checkServerTrusted" in out

    def test_apply_cli(self, smali_tree, tmp_path, capsys):
        script = _write_script(tmp_path, """
hook("com/example/App", "isRooted", "()Z", {
    onLeave = function(retval) return false end
})
""")
        rc = run_renef([
            "apply", str(script), "--smali-dir", str(smali_tree),
            "--no-backup",
        ])
        assert rc == 0
        content = (smali_tree / "smali" / "com" / "example" / "App.smali").read_text()
        assert "Renef STUB inyectado" in content

    def test_apply_requires_source(self, smali_tree):
        with pytest.raises(SystemExit):
            run_renef(["apply", "--smali-dir", str(smali_tree)])
