> [!NOTE]
> Podemos poner nuestro hook en una un archivo que se ejecuta bajo siertas comdiciomes y por esa puede cer que no veas nada en el servidor 

# Ideas de uso 

Si savesmos lo que queremos llamar y enbiar desde el archivo primcipal 

Ejp:
```smali
const-string v1, "Beneficios"

invoke-virtual {v0}, Ljava/lang/Object;->toString()Ljava/lang/String;

move-result-object v2

invoke-static {v1, v2}, Ltb0/c;->d(Ljava/lang/String;Ljava/lang/String;)V
```

Al inicio de los metodos 

```smali
const-string v1, "a()"
const-string v2, "this"
invoke-static {v1, v2, p0}, Lcom/deadnote/RemoteLogger;->hookEnter(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Object;)V
```

antes de los return-object

```
invoke-static {v1, v0}, Lcom/deadnote/RemoteLogger;->hookExit(Ljava/lang/String;Ljava/lang/Object;)V
return-object v0
```

Esto es fundamental para leer firmas Smali.
Por ejemplo:

```
.method public foo(Ljava/lang/String;IZ)Ljava/lang/Integer;
```
se puede leer como:
```
foo(
    String,
    int,
    boolean
) → Integer
```
