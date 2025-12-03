package controlador;

import modelo.ArbolBusqueda;
import vista.VentanaPrincipal;
import controlador.ControladorArbol;

public class SimulacionArbol {
    public static void main(String[] args) {
        // Ejecutar la GUI en el hilo de despacho de eventos de Swing (es la buena práctica)
        javax.swing.SwingUtilities.invokeLater(() -> {
            // 1. Crear el Modelo
        	ArbolBusqueda modelo = new ArbolBusqueda();
            
            // 2. Crear la Vista
            VentanaPrincipal vista = new VentanaPrincipal();
            
            // 3. Crear el Controlador y conectarlo al Modelo y la Vista
            new ControladorArbol(modelo, vista);
        });
    }
}