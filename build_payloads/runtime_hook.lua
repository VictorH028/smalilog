-- Hook en tiempo de ejecución para build_payloads.
--
-- Copiar al directorio privado de la app desde Termux:
--   cat runtime_hook.lua | run-as com.deadnote sh -c 'cat > files/runtime_hook.lua'
--
-- Enviar la orden con la app en ejecución:
--   am broadcast -a com.deadnote.ACCION_DESDE_TERMUX \
--     -n com.deadnote/.ReceptorTermux \
--     --es orden LUA --es arg1 files/runtime_hook.lua
--
-- Al pulsar "prueba1" se espera ver en el servidor smalilog:
--   [RenefLua] [runtime] demoRenefCheck -> false
--   [RenefDemo] demoRenefCheck=false
--   [RenefDemo] demoRenefLabel=runtime-hook

-- Evita duplicar hooks si se reenvía el script sin reiniciar la app.
if _G.__smalilog_runtime_hook then
    print("[runtime] hooks ya instalados; usa LUA_UNHOOK para recargar")
    return
end
_G.__smalilog_runtime_hook = true

print("[runtime] cargando hooks Lua...")

pcall(function()
    hook("com/deadnote/MainActivity", "demoRenefCheck", "()Z", {
        onLeave = function(retval)
            print("[runtime] demoRenefCheck -> false")
            -- En runtime el agente ignora el booleano Lua directo; hay que
            -- usar el descriptor JNI para modificar el retorno.
            return JNI.boolean(false)
        end
    })
    print("[runtime] hook demoRenefCheck instalado")
end)

pcall(function()
    hook("com/deadnote/MainActivity", "demoRenefLabel", "()Ljava/lang/String;", {
        onLeave = function(retval)
            print("[runtime] demoRenefLabel original=" .. tostring(retval.value))
            return JNI.string("runtime-hook")
        end
    })
    print("[runtime] hook demoRenefLabel instalado")
end)

pcall(function()
    hook("com/deadnote/MainActivity", "prueba1", "()V", {
        onEnter = function(args)
            print("[runtime] prueba1 entra")
        end,
        onLeave = function(retval)
            print("[runtime] prueba1 sale")
        end
    })
    print("[runtime] hook prueba1 instalado")
end)

print("[runtime] listo")
