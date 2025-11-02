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
