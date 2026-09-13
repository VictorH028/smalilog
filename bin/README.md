📐 Reglas de Smali que debemos respetar

1. .registers N → total de registros = v0..v(N-1).
2. Los parámetros ocupan los registros ALTOS:
   · p0 = v(N - total_params)
   · p1 = v(N - total_params + 1)
   · …
   · pK = v(N - 1)
3. .locals M es equivalente pero solo cuenta locales; los params van aparte. En .locals, p0 empieza en vM.
4. this cuenta como parámetro solo si el método NO es static.
5. long y double ocupan 2 registros cada uno.
6. El registro de return-X vN es el que hay que preservar.

---
