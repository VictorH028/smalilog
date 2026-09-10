import java.nio.charset.StandardCharsets;
import java.util.Arrays;

public class Main {

    // Método que convierte String a byte[]
    public static byte[] textoABytes(String texto) {
        if (texto == null) {
            return new byte[0];
        }
        return texto.getBytes(StandardCharsets.UTF_8);
    }

    // Punto de entrada para la consola
    public static void main(String[] args) {
        String textoPrueba = "Hola Mundo desde Java!";
        
        // 1. Llamamos a la función
        byte[] resultado = textoABytes(textoPrueba);

        // 2. Mostramos los datos reales en pantalla
        System.out.println("Texto original: " + textoPrueba);
        System.out.println("Bytes devueltos (formato decimal): " + Arrays.toString(resultado));
        System.out.println("Cantidad de bytes: " + resultado.length);
    }
}

