package Nodo;

public class Definicion {
    public int num;
    public Definicion sig;

    public Definicion(int num) {
        this.num = num;
        this.sig = null;
    }

    @Override
    public String toString() {
        return String.valueOf(num);
    }
}
