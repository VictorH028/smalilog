Identificar en Smali las llamadas a Class.forName, Method.invoke, getDeclaredMethod, etc.

Reemplazar esas llamadas por llamadas a Lcom/deadnote/Reflect;->forName y Lcom/deadnote/Reflect;->invoke.

Reflect hace el log con RemoteLog y luego llama al original.
