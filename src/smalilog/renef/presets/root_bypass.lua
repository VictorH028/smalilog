-- Preset de evasión de detección de root para smalilog renef.
-- Solo hooks Java: se traducen a stubs Smali estáticos (sin root).
-- La evasión nativa (open/access/stat de libc) queda fuera de este preset:
-- requiere el agente dinámico de Renef.

-- RootBeer (librería más común).
hook("com/scottyab/rootbeer/RootBeer", "isRooted", "()Z",
     { onLeave = function(retval) return false end }, "RootBeer.isRooted")

hook("com/scottyab/rootbeer/RootBeer", "isRootedWithoutBusyBoxCheck", "()Z",
     { onLeave = function(retval) return false end }, "RootBeer.isRootedWithoutBusyBoxCheck")

hook("com/scottyab/rootbeer/RootBeer", "detectRootManagementApps", "()Z",
     { onLeave = function(retval) return false end }, "RootBeer.detectRootManagementApps")

hook("com/scottyab/rootbeer/RootBeer", "detectPotentiallyDangerousApps", "()Z",
     { onLeave = function(retval) return false end }, "RootBeer.detectPotentiallyDangerousApps")

hook("com/scottyab/rootbeer/RootBeer", "detectTestKeys", "()Z",
     { onLeave = function(retval) return false end }, "RootBeer.detectTestKeys")

hook("com/scottyab/rootbeer/RootBeer", "checkForBusyBoxBinary", "()Z",
     { onLeave = function(retval) return false end }, "RootBeer.checkForBusyBoxBinary")

hook("com/scottyab/rootbeer/RootBeer", "checkForSuBinary", "()Z",
     { onLeave = function(retval) return false end }, "RootBeer.checkForSuBinary")

hook("com/scottyab/rootbeer/RootBeer", "checkSuExists", "()Z",
     { onLeave = function(retval) return false end }, "RootBeer.checkSuExists")

hook("com/scottyab/rootbeer/RootBeer", "checkForRWPaths", "()Z",
     { onLeave = function(retval) return false end }, "RootBeer.checkForRWPaths")

hook("com/scottyab/rootbeer/RootBeer", "checkForDangerousProps", "()Z",
     { onLeave = function(retval) return false end }, "RootBeer.checkForDangerousProps")

hook("com/scottyab/rootbeer/RootBeer", "checkForRootNative", "()Z",
     { onLeave = function(retval) return false end }, "RootBeer.checkForRootNative")

-- Variantes que consultan el entorno.
hook("com/scottyab/rootbeer/util/Utils", "isRooted", "()Z",
     { onLeave = function(retval) return false end }, "RootBeer Utils.isRooted")
