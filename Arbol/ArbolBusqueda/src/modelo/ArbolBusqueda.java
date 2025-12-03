package modelo;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public class ArbolBusqueda {
    private NodoArbol raiz;
    private List<Integer> listaAleatoria;

    public ArbolBusqueda() {
        this.raiz = null;
        this.listaAleatoria = new ArrayList<>();
    }
    
    // Getter para la vista
    public NodoArbol getRaiz() {
        return raiz;
    }

    public List<Integer> getListaAleatoria() {
        return listaAleatoria;
    }

    // Método para generar la lista (movido desde el main)
    public List<Integer> generarListaAleatoria(int cantidad, int min, int max) {
        Random rand = new Random();
        listaAleatoria.clear();

        while (listaAleatoria.size() < cantidad) {
            int numero = rand.nextInt(max - min + 1) + min;
            if (!listaAleatoria.contains(numero)) {
                listaAleatoria.add(numero);
            }
        }
        return listaAleatoria;
    }

    // Método para construir el árbol a partir de la lista
    public void construirArbol(List<Integer> numeros) {
        this.raiz = null;
        for (int numero : numeros) {
            insertar(numero);
        }
    }

    // Lógica de inserción (igual que antes)
    private void insertar(int valor) {
        raiz = insertarRecursivo(raiz, valor);
    }

    private NodoArbol insertarRecursivo(NodoArbol actual, int valor) {
        if (actual == null) {
            return new NodoArbol(valor);
        }

        if (valor < actual.valor) {
            actual.izquierda = insertarRecursivo(actual.izquierda, valor);
        } else if (valor > actual.valor) {
            actual.derecha = insertarRecursivo(actual.derecha, valor);
        }
        return actual;
    }
    /**
     * Inserta un valor y notifica al 'observador' (el controlador/vista)
     * para que pueda redibujar la GUI.
     * @param valor El valor a insertar.
     * @param notificador Objeto que implementa un método para la notificación.
     */
    public void insertarConNotificacion(int valor, NotificadorArbol notificador) {
        raiz = insertarRecursivoConNotificacion(raiz, valor, notificador);
    }

    private NodoArbol insertarRecursivoConNotificacion(NodoArbol actual, int valor, NotificadorArbol notificador) {
        if (actual == null) {
            NodoArbol nuevoNodo = new NodoArbol(valor);
            // ¡Notificación! Se insertó un nuevo nodo.
            if (notificador != null) {
                notificador.notificarInsercion();
            }
            return nuevoNodo;
        }

        // ... (Lógica de inserción normal: izquierda/derecha) ...
        if (valor < actual.valor) {
            actual.izquierda = insertarRecursivoConNotificacion(actual.izquierda, valor, notificador);
        } else if (valor > actual.valor) {
            actual.derecha = insertarRecursivoConNotificacion(actual.derecha, valor, notificador);
        }
        return actual;
    }
}