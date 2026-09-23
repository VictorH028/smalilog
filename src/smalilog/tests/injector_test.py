import pytest
from smalilog.injector._injector import HookInjector

SAMPLE = """\
.class public Lcom/example/App;
.super Landroid/app/Application;

.method public onCreate()V
    .registers 2
    invoke-super {p0}, Landroid/app/Application;->onCreate()V
    return-void
.end method
"""

def test_load_and_resolve(tmp_path):
    f = tmp_path / "App.smali"
    f.write_text(SAMPLE)
    inj = HookInjector(str(f), "Lcom/deadnote/RemoteLogger;")
    assert inj.load()
    assert inj.resolve_method("onCreate")
    assert inj.target is not None

def test_inject_enter(tmp_path):
    f = tmp_path / "App.smali"
    f.write_text(SAMPLE)
    inj = HookInjector(str(f), "Lcom/deadnote/RemoteLogger;")
    inj.load()
    inj.resolve_method("onCreate")
    assert inj.inject_enter()
    text = "\n".join(inj.lines)
    assert "Hook ENTER inyectado" in text
    # Verifica orden: .registers antes del bloque
    reg_pos = text.find(".registers")
    hook_pos = text.find("Hook ENTER inyectado")
    assert reg_pos < hook_pos
