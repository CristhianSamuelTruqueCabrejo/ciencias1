package vista;

import java.awt.*;
import javax.swing.*;
import java.awt.event.ActionListener;
import modelo.NodoArbol;

public class VentanaPrincipal extends JFrame {
    private JButton btnGenerar;
    private JTextArea areaLista;
    private PanelArbol panelArbol;

    public VentanaPrincipal() {
        setTitle("Simulación de Árbol de Búsqueda Binaria (ABB)");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(1000, 700);
        setLocationRelativeTo(null); // Centrar ventana
        setLayout(new BorderLayout(10, 10));

        // --- Panel de Control Superior (Lista y Botón) ---
        JPanel panelControl = new JPanel(new BorderLayout(5, 5));
        
        areaLista = new JTextArea(3, 40);
        areaLista.setEditable(false);
        JScrollPane scrollLista = new JScrollPane(areaLista);
        scrollLista.setBorder(BorderFactory.createTitledBorder("Lista Aleatoria Generada"));
        
        btnGenerar = new JButton("Generar y Construir Árbol");
        btnGenerar.setFont(new Font("SansSerif", Font.BOLD, 14));
        
        panelControl.add(scrollLista, BorderLayout.CENTER);
        panelControl.add(btnGenerar, BorderLayout.SOUTH);
        add(panelControl, BorderLayout.NORTH);

        // --- Panel Central (Visualización del Árbol) ---
        panelArbol = new PanelArbol(null);
        JScrollPane scrollArbol = new JScrollPane(panelArbol);
        scrollArbol.setBorder(BorderFactory.createTitledBorder("Visualización del ABB"));
        add(scrollArbol, BorderLayout.CENTER);

        setVisible(true);
    }

    // Getters para que el controlador acceda a los componentes
    public JButton getBtnGenerar() {
        return btnGenerar;
    }

    // Métodos para actualizar la vista
    public void actualizarLista(String lista) {
        areaLista.setText(lista);
    }

    public void actualizarArbol(NodoArbol raiz) {
        panelArbol.setRaiz(raiz);
        // Asegurar que el panel se redimensione para ver todo el árbol
        panelArbol.revalidate();
    }
    
    // Método para registrar el controlador
    public void agregarListenerGenerar(ActionListener listener) {
        btnGenerar.addActionListener(listener);
    }
}