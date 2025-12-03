package modelo;

import java.util.Random;

public class Nodo {
	public int num;
	public Nodo ant;
	public Nodo sig;
	
	public Nodo() {
		num = (int) (Math.random() * 51);
	}

}
