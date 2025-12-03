import Creacion.Enlace_nodos;
import java.util.Scanner;

public class PruebaGUISimple {
    public static void main(String[] args) {
        Enlace_nodos lista = new Enlace_nodos();
        Scanner sc = new Scanner(System.in);
        
        while (true) {
            System.out.println("\n=== MENU ===");
            System.out.println("1. Insertar al final");
            System.out.println("2. Generar aleatorios");
            System.out.println("3. Mostrar lista");
            System.out.println("4. Añadir después de un valor");
            System.out.println("5. Eliminar");
            System.out.println("0. Salir");
            System.out.print("Opción: ");
            
            int opcion = sc.nextInt();
            
            switch (opcion) {
                case 1:
                    System.out.print("Valor a insertar: ");
                    int valor = sc.nextInt();
                    lista.insertarFinal(valor);
                    System.out.println("Insertado: " + valor);
                    break;
                    
                case 2:
                    lista.generarNodosAleatorios();
                    System.out.println("Nodos aleatorios generados");
                    break;
                    
                case 3:
                    System.out.println("Lista actual:");
                    System.out.println(lista.mostrarLista());
                    break;
                    
                case 4:
                    System.out.print("Después de qué valor: ");
                    int valorObjetivo = sc.nextInt();
                    System.out.print("Nuevo valor a insertar: ");
                    int nuevoValor = sc.nextInt();
                    
                    boolean resultado = lista.añadirDespuesDe(valorObjetivo, nuevoValor);
                    if (resultado) {
                        System.out.println("✅ Insertado " + nuevoValor + " después de " + valorObjetivo);
                    } else {
                        System.out.println("❌ No se encontró el valor " + valorObjetivo);
                    }
                    break;
                    
                case 5:
                    System.out.print("Valor a eliminar: ");
                    int valorEliminar = sc.nextInt();
                    if (lista.eliminar(valorEliminar)) {
                        System.out.println("✅ Eliminado: " + valorEliminar);
                    } else {
                        System.out.println("❌ No se encontró: " + valorEliminar);
                    }
                    break;
                    
                case 0:
                    System.out.println("¡Hasta luego!");
                    return;
                    
                default:
                    System.out.println("Opción inválida");
            }
        }
    }
}