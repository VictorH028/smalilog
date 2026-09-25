"""
Tests del HookInjector.

Ejecuta:
    pytest -q src/smalilog/tests/injector_test.py
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from smalilog.injector._injector import HookInjector


REMOTE_LOGGER = "Lcom/deadnote/RemoteLogger;"
MARKER_ENTER = "Hook ENTER inyectado"
MARKER_EXIT = "Hook EXIT inyectado"


# --------------------------------------------------------------------------- #
#  Fixtures
# --------------------------------------------------------------------------- #
@pytest.fixture
def write_smali(tmp_path: Path):
    """Devuelve una función que escribe smali en un archivo temporal."""
    counter = {"n": 0}

    def _write(content: str, name: str | None = None) -> Path:
        counter["n"] += 1
        fname = name or f"Test{counter['n']}.smali"
        path = tmp_path / fname
        path.write_text(content, encoding="utf-8")
        return path

    return _write


@pytest.fixture
def make_injector(write_smali):
    """Fábrica: content → HookInjector ya cargado y (opcional) resuelto."""
    def _make(content: str, method: str | None = None) -> HookInjector:
        path = write_smali(content)
        inj = HookInjector(str(path), REMOTE_LOGGER)
        assert inj.load(), "load() falló"
        if method is not None:
            assert inj.resolve_method(method), f"resolve_method({method}) falló"
        return inj

    return _make


# --------------------------------------------------------------------------- #
#  Helpers de aserción (independientes del formato exacto)
# --------------------------------------------------------------------------- #
def _body_text(inj: HookInjector) -> str:
    """Devuelve el texto del cuerpo del método objetivo, sin comentarios."""
    m = inj.target
    assert m is not None
    end = inj._find_end_method_line()
    assert end is not None
    lines = inj.lines[m.start_line:end + 1]
    return "\n".join(re.sub(r"#.*", "", ln) for ln in lines)


def _registers_value(inj: HookInjector) -> int:
    """Lee el valor actual de .registers/.locals del método objetivo."""
    m = inj.target
    assert m is not None
    idx = inj._find_registers_line()
    assert idx is not None
    match = re.search(r"\.(registers|locals)\s+(\d+)", inj.lines[idx])
    assert match is not None
    return int(match.group(2))


def _has_hook_enter(inj: HookInjector) -> bool:
    return any(MARKER_ENTER in ln for ln in inj.lines)


def _has_hook_exit(inj: HookInjector) -> bool:
    return any(MARKER_EXIT in ln for ln in inj.lines)


def _count_invoke(inj: HookInjector, needle: str) -> int:
    return sum(1 for ln in inj.lines if needle in ln)


# --------------------------------------------------------------------------- #
#  Smali de ejemplo
# --------------------------------------------------------------------------- #
SAMPLE_STATIC_VOID = """\
.class public Lcom/example/App;
.super Landroid/app/Application;

.method public static final isPremium(Lcom/example/Benefit;)Z
    .registers 2
    const-string v0, "x"
    return v0
.end method
"""

SAMPLE_INSTANCE_NO_ARGS = """\
.class public Lcom/example/App;
.super Landroid/app/Application;

.method public onCreate()V
    .registers 2
    invoke-super {p0}, Landroid/app/Application;->onCreate()V
    return-void
.end method
"""

SAMPLE_STATIC_NO_ARGS = """\
.class public Lcom/example/App;

.method public static foo()V
    .registers 1
    return-void
.end method
"""

SAMPLE_LOCALS_DIRECTIVE = """\
.class public Lcom/example/App;

.method public static bar(I)I
    .locals 2
    const/4 v0, 0x0
    return v0
.end method
"""

SAMPLE_OVERLOADED = """\
.class public Lcom/example/App;

.method public static foo()V
    .registers 1
    return-void
.end method

.method public static foo(I)V
    .registers 2
    return-void
.end method
"""

SAMPLE_NO_BODY = """\
.class public Lcom/example/App;

.method public abstract baz()V
.end method
"""

SAMPLE_WIDE_PARAM = """\
.class public Lcom/example/App;

.method public static qux(J)V
    .registers 3
    return-void
.end method
"""


# --------------------------------------------------------------------------- #
#  Carga y resolución
# --------------------------------------------------------------------------- #
class TestLoad:
    def test_load_ok(self, write_smali):
        path = write_smali(SAMPLE_STATIC_VOID)
        inj = HookInjector(str(path), REMOTE_LOGGER)
        assert inj.load()
        assert inj.class_name == "Lcom/example/App;"
        assert len(inj.methods) == 1

    def test_load_missing_file(self, tmp_path):
        inj = HookInjector(str(tmp_path / "nope.smali"), REMOTE_LOGGER)
        assert inj.load() is False

    def test_class_name_parsed(self, make_injector):
        inj = make_injector(SAMPLE_STATIC_VOID)
        assert inj.class_name == "Lcom/example/App;"


class TestResolveMethod:
    def test_resolve_simple(self, make_injector):
        inj = make_injector(SAMPLE_STATIC_VOID, method="isPremium")
        assert inj.target is not None
        assert inj.target.name == "isPremium"

    def test_resolve_nonexistent(self, make_injector):
        inj = make_injector(SAMPLE_STATIC_VOID)
        assert inj.resolve_method("nope") is False
        assert inj.target is None

    def test_resolve_overloaded_requires_sig(self, make_injector):
        inj = make_injector(SAMPLE_OVERLOADED)
        assert inj.resolve_method("foo") is False

    def test_resolve_overloaded_with_sig(self, make_injector):
        inj = make_injector(SAMPLE_OVERLOADED)
        assert inj.resolve_method("foo", "(I)V") is True
        assert inj.target is not None
        assert inj.target.signature == "(I)V"

    def test_resolve_no_body_fails(self, make_injector):
        inj = make_injector(SAMPLE_NO_BODY)
        assert inj.resolve_method("baz") is False


# --------------------------------------------------------------------------- #
#  enter
# --------------------------------------------------------------------------- #
class TestInjectEnter:
    def test_enter_static_ref_arg(self, make_injector):
        """Arg de referencia: 2 temps, no boxing, arg_sym=p0."""
        inj = make_injector(SAMPLE_STATIC_VOID, method="isPremium")
        before = _registers_value(inj)
        assert inj.inject_enter()

        assert _has_hook_enter(inj)
        assert _registers_value(inj) == before + 2
        # El invoke usa p0 (el objeto original)
        body = _body_text(inj)
        assert "invoke-static" in body
        assert "hookEnter" in body
        # No debe haber move-result-object (no hay boxing)
        assert "move-result-object" not in body

    def test_enter_instance_no_args(self, make_injector):
        """Sin args y no estático: arg_sym=p0, arg_name=this, no boxing."""
        inj = make_injector(SAMPLE_INSTANCE_NO_ARGS, method="onCreate")
        before = _registers_value(inj)
        assert inj.inject_enter()

        assert _has_hook_enter(inj)
        assert _registers_value(inj) == before + 2

    def test_enter_static_no_args(self, make_injector):
        """Sin args y estático: arg_desc=None → necesita boxing (null)."""
        inj = make_injector(SAMPLE_STATIC_NO_ARGS, method="foo")
        before = _registers_value(inj)
        assert inj.inject_enter()

        assert _has_hook_enter(inj)
        # 3 temps por boxing de null
        assert _registers_value(inj) == before + 3

    def test_enter_primitive_arg_boxes(self, make_injector):
        """Arg primitivo (I): boxing → 3 temps."""
        inj = make_injector(
            """.class public Lcom/example/App;
.method public static f(I)V
    .registers 2
    return-void
.end method
""",
            method="f",
        )
        before = _registers_value(inj)
        assert inj.inject_enter()
        assert _registers_value(inj) == before + 3

    def test_enter_wide_arg(self, make_injector):
        """J ocupa 2 registros; aun así boxing → 3 temps."""
        inj = make_injector(SAMPLE_WIDE_PARAM, method="qux")
        before = _registers_value(inj)
        assert inj.inject_enter()
        assert _registers_value(inj) == before + 3

    def test_enter_idempotent(self, make_injector):
        inj = make_injector(SAMPLE_STATIC_VOID, method="isPremium")
        assert inj.inject_enter() is True
        regs_after_first = _registers_value(inj)
        assert inj.inject_enter() is True      # no falla
        assert _registers_value(inj) == regs_after_first
        assert _count_invoke(inj, "hookEnter") == 1

    def test_enter_locals_directive(self, make_injector):
        """.locals N → el nuevo .locals debe ser N+need, sin tocar params."""
        inj = make_injector(SAMPLE_LOCALS_DIRECTIVE, method="bar")
        before = _registers_value(inj)       # N = 2
        assert inj.inject_enter()
        # Se convierte a .registers (el planner lo hace así)
        assert _registers_value(inj) == before + 2 + 1  # locals + need + param_regs

    def test_enter_temps_dont_clobber_params(self, make_injector):
        """Los temps frescos no deben coincidir con p0 tras expandir."""
        inj = make_injector(SAMPLE_STATIC_VOID, method="isPremium")
        assert inj.inject_enter()
        m = inj.target
        assert m is not None
        # p0 = último registro tras expandir
        p0_reg = _registers_value(inj) - 1
        # Los const-string del hook usan temps frescos ≠ p0
        for ln in inj.lines:
            if "const-string" in ln and "arg" in ln:
                reg = re.search(r"const-string (v\d+)", ln)
                if reg:
                    assert int(reg.group(1)[1:]) != p0_reg


# --------------------------------------------------------------------------- #
#  exit
# --------------------------------------------------------------------------- #
class TestInjectExit:
    def test_exit_void(self, make_injector):
        inj = make_injector(SAMPLE_INSTANCE_NO_ARGS, method="onCreate")
        before = _registers_value(inj)
        assert inj.inject_exit()
        assert _has_hook_exit(inj)
        assert _registers_value(inj) == before + 2

    def test_exit_idempotent(self, make_injector):
        inj = make_injector(SAMPLE_INSTANCE_NO_ARGS, method="onCreate")
        assert inj.inject_exit()
        regs = _registers_value(inj)
        assert inj.inject_exit()
        assert _registers_value(inj) == regs

    def test_exit_no_returns(self, make_injector):
        inj = make_injector(
            """.class public Lcom/example/App;
.method public static f()V
    .registers 0
.end method
""",
            method="f",
        )
        assert inj.inject_exit() is False

    def test_exit_before_each_return(self, make_injector):
        """Con varios returns, inyecta antes de cada uno."""
        inj = make_injector(
            """.class public Lcom/example/App;
.method public static f(I)I
    .registers 2
    if-eqz p0, :end
    const/4 v0, 0x1
    return v0
    :end
    const/4 v0, 0x0
    return v0
.end method
""",
            method="f",
        )
        assert inj.inject_exit()
        assert inj.lines.count("    return v0") == 2  # se preservan
        # Debe haber al menos 2 invokes a hookExit
        assert _count_invoke(inj, "hookExit") >= 2


# --------------------------------------------------------------------------- #
#  save
# --------------------------------------------------------------------------- #
class TestSave:
    def test_save_in_place(self, make_injector, write_smali, tmp_path):
        path = write_smali(SAMPLE_STATIC_VOID, name="Target.smali")
        inj = HookInjector(str(path), REMOTE_LOGGER)
        inj.load()
        inj.resolve_method("isPremium")
        inj.inject_enter()
        inj.save(backup=True)

        assert path.exists()
        bak = path.with_suffix(".smali.bak")
        assert bak.exists()

        content = path.read_text()
        assert MARKER_ENTER in content
        # El backup es el original
        assert MARKER_ENTER not in bak.read_text()

    def test_save_to_output(self, make_injector, write_smali, tmp_path):
        path = write_smali(SAMPLE_STATIC_VOID, name="Orig.smali")
        out = tmp_path / "Copy.smali"
        inj = HookInjector(str(path), REMOTE_LOGGER)
        inj.load()
        inj.resolve_method("isPremium")
        inj.inject_enter()
        inj.save(output=str(out), backup=False)

        assert out.exists()
        assert MARKER_ENTER in out.read_text()
        # El original queda intacto
        assert MARKER_ENTER not in path.read_text()

    def test_save_no_backup(self, write_smali):
        path = write_smali(SAMPLE_STATIC_VOID, name="NoBak.smali")
        inj = HookInjector(str(path), REMOTE_LOGGER)
        inj.load()
        inj.resolve_method("isPremium")
        inj.inject_enter()
        inj.save(backup=False)
        assert not path.with_suffix(".smali.bak").exists()


# --------------------------------------------------------------------------- #
#  lifecycle
# --------------------------------------------------------------------------- #
class TestLifecycle:
    def test_lifecycle_ok(self, make_injector):
        inj = make_injector(SAMPLE_INSTANCE_NO_ARGS, method="onCreate")
        assert inj.inject_lifecycle_tracker()
        joined = "\n".join(inj.lines)
        assert "LifecycleTracker;->init(" in joined

    def test_lifecycle_idempotent(self, make_injector):
        inj = make_injector(SAMPLE_INSTANCE_NO_ARGS, method="onCreate")
        assert inj.inject_lifecycle_tracker()
        assert inj.inject_lifecycle_tracker()
        joined = "\n".join(inj.lines)
        assert joined.count("LifecycleTracker;->init(") == 1

    def test_lifecycle_wrong_method(self, make_injector):
        inj = make_injector(SAMPLE_STATIC_VOID, method="isPremium")
        assert inj.inject_lifecycle_tracker() is False


# --------------------------------------------------------------------------- #
#  show_method (smoke test)
# --------------------------------------------------------------------------- #
class TestShow:
    def test_show_runs(self, make_injector, capsys):
        inj = make_injector(SAMPLE_STATIC_VOID, method="isPremium")
        assert inj.show_method(color=False) is True
        out = capsys.readouterr().out
        assert "isPremium" in out
        assert "registers" in out

    def test_show_with_hook_marks(self, make_injector, capsys):
        inj = make_injector(SAMPLE_STATIC_VOID, method="isPremium")
        inj.inject_enter()
        inj.show_method(color=False)
        out = capsys.readouterr().out
        assert "bloque(s) inyectado(s)" in out
