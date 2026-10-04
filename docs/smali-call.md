Para llamar correctamente a métodos u objetos de otros archivos Smali (o cualquier otra actividad), debes tener en cuenta varios aspectos técnicos fundamentales de la MV Dalvik/ART.

1. Tipos de métodos y sus instrucciones de llamada

Smali utiliza distintas instrucciones según cómo esté declarado el método que deseas invocar:
 * Métodos estáticos (static):
   * No requieren instanciar la clase.
   * Se invocan con invoke-static.
   invoke-static {p0, p1}, Lcom/ejemplo/MiClase;->miMetodoEstatico(Landroid/content/Context;I)V

 * Métodos de instancia (virtual / públicos / protegidos):
   * Requieren una instancia previa de la clase (objeto).
   * Se invocan con invoke-virtual.
   invoke-virtual {v0, p1}, Lcom/ejemplo/MiClase;->miMetodoVirtual(I)I
move-result v0  # Captura el resultado devuelto (si aplica)

 * Métodos privados o constructores (direct):
   * Se invocan con invoke-direct (usualmente al instanciar con <init>).

2. Firma exacta del método (Method Signature)

Smali exige la sintaxis exacta de la firma completa, incluyendo el descriptor de la clase, el nombre y los tipos de parámetros/retorno. Si falla un solo carácter, la aplicación se cerrará al iniciar (ClassNotFoundException o NoSuchMethodError).
 * Sintaxis: Lnombre/de/paquete/NombreClase;->nombreMetodo(Parámetros)TipoRetorno
 * Mapeo de tipos básicos:
   * V → void
   * Z → boolean
   * I → int
   * J → long
   * Ljava/lang/String; → String
   * Landroid/content/Context; → Context

3. Creación e instanciación de objetos

Si el método no es estático, debes instanciar la clase antes de llamarlo:
# 1. Crear una nueva instancia de la clase
new-instance v0, Lcom/ejemplo/MiClase;

# 2. Inicializar el objeto (llamar al constructor)
invoke-direct {v0}, Lcom/ejemplo/MiClase;-><init>()V

# 3. Llamar al método deseado pasando la instancia en v0
invoke-virtual {v0}, Lcom/ejemplo/MiClase;->miMetodo()V

> Nota sobre el Context: Si la clase objetivo requiere un objeto Context en su constructor o método, pasa p0 desde la MainActivity (ya que una Activity es una subclase de Context).
> 
4. Manejo de registros y espacio (.registers)
Cada método Smali define un número de registros de trabajo al inicio (ej. .registers 4 o .locals 2).
 * Asegúrate de que tu método en MainActivity tenga suficientes registros libres para almacenar las instancias, parámetros y valores devueltos.
 * Si agregas código nuevo, incrementa la directiva .locals al inicio de tu método para evitar un desbordamiento de registros.
5. Captura del valor de retorno
Si el método invocado devuelve un valor, debes extraerlo inmediatamente en la línea siguiente a la invocación:
 * Primitivos (int, boolean, etc.): move-result v0
 * Objetos / Strings: move-result-object v0
 * Primitivos de 64 bits (long, double): move-result-wide v0
Checklist de verificación rápida
 * Ruta completa: Confirma que las carpetas del archivo .smali objetivo coincidan exactamente con la declaración de su paquete.
 * Visibilidad: Comprueba que la clase y el método no sean privados (a menos que uses acceso por reflexión o modifiques los modificadores public en el archivo Smali objetivo).
 * Constructor dex: Asegúrate de recompilar con apktool b para validar que no existan errores sintácticos.

