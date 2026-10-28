-- Ejemplo ejecutable del puente Renef -> Smali sobre build_payloads.
--
-- Esperado tras instalar la APK y pulsar "prueba1":
--   [RenefDemo] demoRenefCheck=false
--   [RenefDemo] demoRenefLabel=parcheado
--   [TRACE] ... MainActivity;->prueba1()V ...
--
-- demoRenefCheck/demoRenefLabel existen en MainActivity.java solo para este
-- ejemplo (ver src/com/deadnote/MainActivity.java).

hook("com/deadnote/MainActivity", "demoRenefCheck", "()Z", {
    onLeave = function(retval) return false end
})

hook("com/deadnote/MainActivity", "demoRenefLabel", "()Ljava/lang/String;", {
    onLeave = function(retval) return "parcheado" end
})

hook("com/deadnote/MainActivity", "prueba1", "()V", {
    onEnter = function(args) print("[demo] prueba1 entra") end,
    onLeave = function(retval) print("[demo] prueba1 sale") end
})
