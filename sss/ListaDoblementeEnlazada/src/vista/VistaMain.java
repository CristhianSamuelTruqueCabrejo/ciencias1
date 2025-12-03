package vista;

import java.awt.*;
import javax.swing.*;
import javax.swing.border.EmptyBorder;

public class VistaMain extends JFrame {

    // Componentes accesibles para el controlador
    public JTextField txtCantidad, txtBuscar, txtEliminar;
    public JButton btnCrear, btnMostrar, btnBuscar, btnEliminar, btnTamaño;
    public JTextArea txtSalida;
    public JTextField txtInsertarValor, txtInsertarPos;
    public JButton btnInsertar;

    public VistaMain() {
        setTitle("Gestor de Lista Aleatoria (MVC)");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(750, 600);
        setMinimumSize(new Dimension(650, 550));
        setLocationRelativeTo(null);
        setLayout(new BorderLayout(15, 15));
        ((JPanel) getContentPane()).setBorder(new EmptyBorder(10, 10, 10, 10));

        // 1. PANEL SUPERIOR: CREAR LISTA
        add(crearPanelSuperior(), BorderLayout.NORTH);

        // 2. PANEL CENTRAL: ACCIONES
        add(crearPanelCentral(), BorderLayout.CENTER);

        // 3. PANEL INFERIOR: SALIDA
        add(crearPanelInferior(), BorderLayout.SOUTH);

        pack();
        setVisible(true);
    }
    
    // --- Métodos para crear Paneles ---

    private JPanel crearPanelSuperior() {
        JPanel panelSuperior = new JPanel(new GridBagLayout());
        panelSuperior.setBorder(BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(Color.GRAY), "📋 Generación y Visualización"));
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5); // Espaciado interno
        gbc.fill = GridBagConstraints.HORIZONTAL;

        // Etiqueta
        gbc.gridx = 0;
        gbc.gridy = 0;
        panelSuperior.add(new JLabel("Cantidad de nodos:"), gbc);

        // Campo de texto
        gbc.gridx = 1;
        gbc.gridy = 0;
        txtCantidad = new JTextField(8);
        panelSuperior.add(txtCantidad, gbc);

        // Botón Crear
        gbc.gridx = 2;
        gbc.gridy = 0;
        btnCrear = new JButton("Crear lista aleatoria");
        panelSuperior.add(btnCrear, gbc);

        // Botón Mostrar
        gbc.gridx = 3;
        gbc.gridy = 0;
        btnMostrar = new JButton("Mostrar lista actual");
        panelSuperior.add(btnMostrar, gbc);
        
        // Espaciador para centrar
        gbc.gridx = 4;
        gbc.weightx = 1.0; // Hace que esta columna tome el espacio extra
        panelSuperior.add(new JLabel(""), gbc);

        return panelSuperior;
    }

    private JPanel crearPanelCentral() {
        JPanel panelCentral = new JPanel(new GridLayout(1, 2, 15, 0)); // 1 fila, 2 columnas para división principal
        panelCentral.setBorder(BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(Color.GRAY), "⚙️ Operaciones Principales"));

        // --- PANEL IZQUIERDO: Buscar, Eliminar, Tamaño ---
        JPanel panelIzquierdo = new JPanel(new GridLayout(3, 1, 10, 10)); // 3 filas para las acciones
        panelIzquierdo.setBorder(new EmptyBorder(10, 10, 10, 10));

        // Buscar
        JPanel buscarPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        buscarPanel.add(new JLabel("Buscar valor:"));
        txtBuscar = new JTextField(8);
        buscarPanel.add(txtBuscar);
        btnBuscar = new JButton("Buscar nodo");
        buscarPanel.add(btnBuscar);
        panelIzquierdo.add(buscarPanel);

        // Eliminar
        JPanel eliminarPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        eliminarPanel.add(new JLabel("Eliminar valor:"));
        txtEliminar = new JTextField(8);
        eliminarPanel.add(txtEliminar);
        btnEliminar = new JButton("Eliminar nodo");
        eliminarPanel.add(btnEliminar);
        panelIzquierdo.add(eliminarPanel);

        // Tamaño
        JPanel tamañoPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        btnTamaño = new JButton("Mostrar tamaño de la lista");
        tamañoPanel.add(btnTamaño);
        panelIzquierdo.add(tamañoPanel);

        panelCentral.add(panelIzquierdo);

        // --- PANEL DERECHO: Insertar nodo ---
        JPanel panelInsertar = new JPanel(new GridBagLayout());
        panelInsertar.setBorder(BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(Color.LIGHT_GRAY), "➕ Insertar Nodo por Posición"));

        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5);
        gbc.fill = GridBagConstraints.HORIZONTAL;
        
        // Fila 1: Valor
        gbc.gridx = 0;
        gbc.gridy = 0;
        panelInsertar.add(new JLabel("Valor a insertar:"), gbc);
        gbc.gridx = 1;
        txtInsertarValor = new JTextField(8);
        panelInsertar.add(txtInsertarValor, gbc);
        
        // Fila 2: Posición
        gbc.gridx = 0;
        gbc.gridy = 1;
        panelInsertar.add(new JLabel("Posición (índice):"), gbc);
        gbc.gridx = 1;
        txtInsertarPos = new JTextField(8);
        panelInsertar.add(txtInsertarPos, gbc);
        
        // Fila 3: Botón
        gbc.gridx = 0;
        gbc.gridy = 2;
        gbc.gridwidth = 2; // Ocupa ambas columnas
        btnInsertar = new JButton("Insertar nodo");
        panelInsertar.add(btnInsertar, gbc);
        
        // Espaciador para alinear el título
        gbc.gridx = 0;
        gbc.gridy = 3;
        gbc.weighty = 1.0;
        panelInsertar.add(new JLabel(""), gbc);
        
        panelCentral.add(panelInsertar);

        return panelCentral;
    }

    private JPanel crearPanelInferior() {
        JPanel panelInferior = new JPanel(new BorderLayout());
        panelInferior.setBorder(BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(Color.GRAY), "📝 Salida de Resultados"));

        txtSalida = new JTextArea(10, 50); 
        txtSalida.setFont(new Font("Monospaced", Font.PLAIN, 14)); // Usar Monospaced para mejor lectura de listas
        txtSalida.setEditable(false);
        txtSalida.setLineWrap(true);
        txtSalida.setWrapStyleWord(true);

        JScrollPane scrollSalida = new JScrollPane(txtSalida);

        panelInferior.add(scrollSalida, BorderLayout.CENTER);
        
        return panelInferior;
    }
}