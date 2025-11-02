package listadinamica;

import Creacion.Enlace_nodos;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class ListaDinamica extends JFrame {
    private final Enlace_nodos lista = new Enlace_nodos();
    private final JTextArea areaLista;
    private final JTextField campoValor;

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

        // Panel inferior con botones
        JPanel controles = new JPanel();
        controles.setLayout(new FlowLayout());

        campoValor = new JTextField(5);
        JButton btnInsertar = new JButton("Insertar");
        JButton btnEliminar = new JButton("Eliminar");
        JButton btnAleatorio = new JButton("Generar Aleatoria");
        JButton btnMostrar = new JButton("Mostrar");

        controles.add(new JLabel("Valor:"));
        controles.add(campoValor);
        controles.add(btnInsertar);
        controles.add(btnEliminar);
        controles.add(btnAleatorio);
        controles.add(btnMostrar);

        panel.add(controles, BorderLayout.SOUTH);
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

        btnMostrar.addActionListener(e -> mostrarLista());
    }

    private void mostrarLista() {
        areaLista.setText(lista.mostrarLista());
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new ListaDinamica().setVisible(true));
    }
}
