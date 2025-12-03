import Creacion.Enlace_nodos;

public class PruebaAñadir {
    public static void main(String[] args) {
        Enlace_nodos lista = new Enlace_nodos();
        
        // Crear una lista inicial: 1 → 2 → 3 → NULL
        lista.insertarFinal(1);
        lista.insertarFinal(2);
        lista.insertarFinal(3);
        
        System.out.println("Lista inicial:");
        System.out.println(lista.mostrarLista());
        
        // Probar añadir después del valor 2
        boolean resultado = lista.añadirDespuesDe(2, 99);
        System.out.println("\nAñadir 99 después de 2: " + resultado);
        System.out.println("Lista después de añadir:");
        System.out.println(lista.mostrarLista());
        
        // Probar añadir después del valor 1 (al inicio)
        resultado = lista.añadirDespuesDe(1, 88);
        System.out.println("\nAñadir 88 después de 1: " + resultado);
        System.out.println("Lista después de añadir:");
        System.out.println(lista.mostrarLista());
        
        // Probar añadir después de un valor que no existe
        resultado = lista.añadirDespuesDe(100, 77);
        System.out.println("\nAñadir 77 después de 100 (no existe): " + resultado);
        System.out.println("Lista final:");
        System.out.println(lista.mostrarLista());
    }
}