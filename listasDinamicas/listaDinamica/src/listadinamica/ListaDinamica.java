package listadinamica;

import Creacion.Enlace_nodos;
import java.awt.*;
import javax.swing.*;

public class ListaDinamica extends JFrame {
    private final Enlace_nodos lista = new Enlace_nodos();
    private final JTextArea areaLista;
    private final JTextField campoValor;
    private final JTextField campoValorObjetivo;

    public ListaDinamica() {
        setTitle("Lista Dinámica - Ejemplo");
        setSize(500, 400);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        // Panel principal
        JPanel panel = new JPanel();
        panel.setLayout(new BorderLayout());

        // Área de texto
        areaLista = new JTextArea();
        areaLista.setEditable(false);
        areaLista.setFont(new Font("Monospaced", Font.PLAIN, 16));
        panel.add(new JScrollPane(areaLista), BorderLayout.CENTER);

        // Panel inferior con dos filas para que todos los controles se vean
        JPanel panelControles = new JPanel(new GridLayout(2, 1));

        JPanel fila1 = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JPanel fila2 = new JPanel(new FlowLayout(FlowLayout.LEFT));

        campoValor = new JTextField(5);
        campoValorObjetivo = new JTextField(5);
        JButton btnInsertar = new JButton("Insertar");
        JButton btnEliminar = new JButton("Eliminar");
        JButton btnAnadirDespues = new JButton("Añadir Después");
        JButton btnAleatorio = new JButton("Generar Aleatoria");
        JButton btnMostrar = new JButton("Mostrar");

        // Fila 1: valor, insertar, eliminar, mostrar
        fila1.add(new JLabel("Valor:"));
        fila1.add(campoValor);
        fila1.add(btnInsertar);
        fila1.add(btnEliminar);
        fila1.add(btnMostrar);

        // Fila 2: después de, campo, añadir después, generar aleatoria
        fila2.add(new JLabel("Después de:"));
        fila2.add(campoValorObjetivo);
        fila2.add(btnAnadirDespues);
        fila2.add(btnAleatorio);

        panelControles.add(fila1);
        panelControles.add(fila2);

        panel.add(panelControles, BorderLayout.SOUTH);
        add(panel);

        // Acciones de botones
        btnInsertar.addActionListener(e -> {
            try {
                int valor = Integer.parseInt(campoValor.getText());
                lista.insertarFinal(valor);
                mostrarLista();
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Ingrese un número válido.");
            }
        });

        btnEliminar.addActionListener(e -> {
            try {
                int valor = Integer.parseInt(campoValor.getText());
                if (lista.eliminar(valor))
                    JOptionPane.showMessageDialog(this, "Nodo eliminado: " + valor);
                else
                    JOptionPane.showMessageDialog(this, "No se encontró el valor en la lista.");
                mostrarLista();
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Ingrese un número válido.");
            }
        });

        btnAleatorio.addActionListener(e -> {
            lista.generarNodosAleatorios();
            mostrarLista();
        });

        btnAnadirDespues.addActionListener(e -> {
            try {
                int valorNuevo = Integer.parseInt(campoValor.getText());
                int valorObjetivo = Integer.parseInt(campoValorObjetivo.getText());
                boolean ok = lista.añadirDespuesDe(valorObjetivo, valorNuevo);
                if (ok) {
                    JOptionPane.showMessageDialog(this, "Se añadió " + valorNuevo + " después de " + valorObjetivo);
                } else {
                    JOptionPane.showMessageDialog(this, "No se encontró el valor " + valorObjetivo + " en la lista.");
                }
                mostrarLista();
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Ingrese números válidos en ambos campos.");
            }
        });

        btnMostrar.addActionListener(e -> mostrarLista());
    }

    private void mostrarLista() {
        areaLista.setText(lista.mostrarLista());
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new ListaDinamica().setVisible(true));
    }
}
