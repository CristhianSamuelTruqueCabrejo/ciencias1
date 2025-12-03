package Creacion;

import Nodo.Definicion;
import java.util.Random;

public class Enlace_nodos {
    private Definicion cabeza;

    // Insertar al inicio
    public void insertarInicio(int valor) {
        Definicion nuevo = new Definicion(valor);
        nuevo.sig = cabeza;
        cabeza = nuevo;
    }

    // Insertar al final
    public void insertarFinal(int valor) {
        Definicion nuevo = new Definicion(valor);
        if (cabeza == null) {
            cabeza = nuevo;
            return;
        }
        Definicion aux = cabeza;
        while (aux.sig != null) {
            aux = aux.sig;
        }
        aux.sig = nuevo;
    }

    // Generar una lista aleatoria de nodos (SIN BORRAR LOS EXISTENTES)
    public void generarNodosAleatorios() {
        Random r = new Random();
        int cantidad = r.nextInt(6) + 5; // entre 5 y 10 nodos nuevos
        for (int i = 0; i < cantidad; i++) {
            insertarFinal(r.nextInt(25) + 1); // valores entre 1 y 25
        }
    }

    // Añadir un nuevo nodo después del primer nodo cuyo valor sea valorObjetivo
    // Retorna true si se insertó; false si no se encontró el valorObjetivo
    public boolean añadirDespuesDe(int valorObjetivo, int nuevoDato) {
        if (cabeza == null) return false;

        Definicion aux = cabeza;
        // Buscar el primer nodo que tenga el valor objetivo
        while (aux != null && aux.num != valorObjetivo) {
            aux = aux.sig;
        }

        if (aux == null) {
            return false; // No se encontró el valor objetivo
        }

        // Insertar el nuevo nodo después de aux
        Definicion nuevo = new Definicion(nuevoDato);
        nuevo.sig = aux.sig;
        aux.sig = nuevo;
        return true;
    }

    // Eliminar nodo por valor
    public boolean eliminar(int valor) {
        if (cabeza == null) return false;

        if (cabeza.num == valor) {
            cabeza = cabeza.sig;
            return true;
        }

        Definicion aux = cabeza;
        while (aux.sig != null && aux.sig.num != valor) {
            aux = aux.sig;
        }

        if (aux.sig != null) {
            aux.sig = aux.sig.sig;
            return true;
        }
        return false;
    }

    // Mostrar lista como cadena
    public String mostrarLista() {
        StringBuilder sb = new StringBuilder();
        Definicion aux = cabeza;
        while (aux != null) {
            sb.append(aux.num).append(" → ");
            aux = aux.sig;
        }
        sb.append("NULL");
        return sb.toString();
    }

    public boolean estaVacia() {
        return cabeza == null;
    }
}
