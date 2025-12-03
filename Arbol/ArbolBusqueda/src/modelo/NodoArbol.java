package modelo;

public class NodoArbol {
    public int valor;
    public NodoArbol izquierda;
    public NodoArbol derecha;

    // Constructor
    public NodoArbol(int valor) {
        this.valor = valor;
        this.izquierda = null;
        this.derecha = null;
    }
}
