package modelo;

public class Lista {
	public Nodo p;
	public Nodo q;
	public Nodo cab;
	
	public Lista() {
		p = null;
		q = null;
		cab = null;
	}
	
	public void crearLista(int cantidadNodos) {
		for (int i = 0; i < cantidadNodos; i++) {
			if(i == 0) {
				p = new Nodo();
				p.ant = null;
				p.sig = null;
				cab = p;
			}
			else {
				q = new Nodo();
				q.ant = cab;
				q.sig = null;
				cab.sig = q;
				cab = q;
			}
		}
	}
	
	public void mostrarLista() {
	    Nodo temp = p; // empieza desde el primero
	    while (temp != null) {
	        System.out.print(temp.num + " ");
	        temp = temp.sig;
	    }
	    System.out.println();
	}

	public boolean buscar(int valor) {
	    Nodo temp = p;
	    while (temp != null) {
	        if (temp.num == valor) {
	            return true;
	        }
	        temp = temp.sig;
	    }
	    return false;
	}

	public void eliminar(int valor) {
	    Nodo temp = p;

	    while (temp != null) {
	        if (temp.num == valor) {
	            if (temp.ant != null)
	                temp.ant.sig = temp.sig;
	            else
	                p = temp.sig; // era el primero

	            if (temp.sig != null)
	                temp.sig.ant = temp.ant;
	            else
	                cab = temp.ant; // era el último

	            return;
	        }
	        temp = temp.sig;
	    }
	}

	public int tamaño() {
	    int contador = 0;
	    Nodo temp = p;
	    while (temp != null) {
	        contador++;
	        temp = temp.sig;
	    }
	    return contador;
	}
	
	public void insertarEnPosicion(int valor, int posicion) {
        Nodo nuevo = new Nodo();
        nuevo.num = valor;

        if (p == null) {
            // Si la lista está vacía
            p = nuevo;
            cab = nuevo;
            return;
        }

        if (posicion <= 1) {
            // Insertar al inicio
            nuevo.sig = p;
            p.ant = nuevo;
            p = nuevo;
            return;
        }

        Nodo temp = p;
        int contador = 1;

        while (temp != null && contador < posicion - 1) {
            temp = temp.sig;
            contador++;
        }

        if (temp == null || temp.sig == null) {
            // Insertar al final si la posición supera el tamaño
            cab.sig = nuevo;
            nuevo.ant = cab;
            cab = nuevo;
        } else {
            // Insertar en medio
            nuevo.sig = temp.sig;
            nuevo.ant = temp;
            temp.sig.ant = nuevo;
            temp.sig = nuevo;
        }
    }

}
