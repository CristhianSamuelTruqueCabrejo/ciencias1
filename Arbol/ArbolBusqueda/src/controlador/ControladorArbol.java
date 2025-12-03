package controlador;

import modelo.ArbolBusqueda;
import modelo.NotificadorArbol;
import vista.VentanaPrincipal;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.List;
import javax.swing.SwingUtilities;
import javax.swing.JOptionPane;

public class ControladorArbol implements ActionListener, NotificadorArbol {
    private ArbolBusqueda modelo;
    private VentanaPrincipal vista;
    
    // --- VARIABLE CLAVE PARA ASIGNAR EL TIEMPO DE SIMULACIÓN ---
    private static final int TIEMPO_RETRASO_MS = 500; // 500 milisegundos (0.5 segundos) de pausa por inserción
    // ------------------------------------------------------------

    public ControladorArbol(ArbolBusqueda modelo, VentanaPrincipal vista) {
        this.modelo = modelo;
        this.vista = vista;
        
        // Conectar el botón de la vista a este controlador
        this.vista.agregarListenerGenerar(this);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == vista.getBtnGenerar()) {
            vista.getBtnGenerar().setEnabled(false); // Deshabilita el botón

            // 1. Generar la lista aleatoria
            // Se puede ajustar la cantidad de nodos aquí:
            List<Integer> numeros = modelo.generarListaAleatoria(12, 10, 99); 
            vista.actualizarLista(numeros.toString());
            
            // 2. Reiniciar el árbol y la vista para empezar desde cero
            modelo.construirArbol(List.of()); 
            vista.actualizarArbol(modelo.getRaiz());

            // 3. Iniciar el Hilo de Simulación (para evitar congelar la GUI)
            new Thread(() -> {
                simularConstruccion(numeros);
                
                // Vuelve a habilitar el botón una vez terminada la simulación
                SwingUtilities.invokeLater(() -> vista.getBtnGenerar().setEnabled(true));
            }).start();
        }
    }

    /**
     * Lógica de simulación ejecutada en un hilo separado.
     */
    private void simularConstruccion(List<Integer> numeros) {
        for (int numero : numeros) {
            try {
                // Insertamos un valor y, si se crea un nodo, se llama a notificarInsercion()
                modelo.insertarConNotificacion(numero, this); 
                
                // Pausa la ejecución para ver el cambio
                Thread.sleep(TIEMPO_RETRASO_MS); 
            } catch (InterruptedException ex) {
                // Manejo de interrupción del hilo
                Thread.currentThread().interrupt();
                JOptionPane.showMessageDialog(vista, "Simulación interrumpida.", "Error", JOptionPane.ERROR_MESSAGE);
                break;
            } catch (Exception ex) {
                // Captura otros errores del modelo
                JOptionPane.showMessageDialog(vista, "Error: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
                break;
            }
        }
    }

    /**
     * Implementación del NotificadorArbol. 
     * Se llama desde el Modelo cuando se añade un nuevo nodo.
     */
    @Override
    public void notificarInsercion() {
        // Obliga a que la actualización de la interfaz gráfica se haga en el hilo seguro de Swing
        SwingUtilities.invokeLater(() -> {
            vista.actualizarArbol(modelo.getRaiz());
            vista.revalidate(); // Asegura el redibujo
        });
    }
}