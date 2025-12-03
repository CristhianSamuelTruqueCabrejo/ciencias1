package controlador;

import controlador.Controlador;
import modelo.Lista;
import vista.VistaMain;

public class Launcher {
    public static void main(String[] args) {
        Lista lista = new Lista();
        VistaMain vista = new VistaMain();
        new Controlador(vista, lista);
        vista.setVisible(true);
    }
}
