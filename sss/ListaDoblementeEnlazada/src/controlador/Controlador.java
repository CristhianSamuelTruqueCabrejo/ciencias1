package controlador;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import modelo.Lista;
import modelo.Nodo;
import vista.VistaMain;

public class Controlador implements ActionListener {
	private Lista lista;
    private VistaMain vista;

    public Controlador(VistaMain vista, Lista lista) {
        this.vista = vista;
        this.lista = lista;

        // Registrar listeners
        this.vista.btnCrear.addActionListener(this);
        this.vista.btnMostrar.addActionListener(this);
        this.vista.btnBuscar.addActionListener(this);
        this.vista.btnEliminar.addActionListener(this);
        this.vista.btnTamaño.addActionListener(this);
        this.vista.btnInsertar.addActionListener(this);
    }

    @Override
    public void actionPerformed(ActionEvent e) {

        // --- CREAR LISTA ---
        if (e.getSource() == vista.btnCrear) {
            try {
                int cantidad = Integer.parseInt(vista.txtCantidad.getText());
                if (cantidad <= 0) {
                    vista.txtSalida.setText("⚠️ Ingresa una cantidad mayor que 0.\n");
                    return;
                }
                lista = new Lista(); // reinicia la lista
                lista.crearLista(cantidad);
                vista.txtSalida.setText("✅ Lista creada con " + cantidad + " nodos aleatorios.\n");
            } catch (NumberFormatException ex) {
                vista.txtSalida.setText("❌ Error: ingresa un número válido.\n");
            }
        }

        // --- MOSTRAR LISTA ---
        if (e.getSource() == vista.btnMostrar) {
            if (lista.p == null) {
                vista.txtSalida.setText("⚠️ La lista está vacía.\n");
                return;
            }
            StringBuilder sb = new StringBuilder();
            Nodo temp = lista.p;
            while (temp != null) {
                sb.append(temp.num).append(" ");
                temp = temp.sig;
            }
            vista.txtSalida.setText("📋 Contenido de la lista:\n" + sb.toString() + "\n");
        }
     // --- INSERTAR EN POSICIÓN ---
        if (e.getSource() == vista.btnInsertar) {
            try {
                int valor = Integer.parseInt(vista.txtInsertarValor.getText());
                int posicion = Integer.parseInt(vista.txtInsertarPos.getText());

                if (posicion < 1) {
                    vista.txtSalida.setText("⚠️ La posición debe ser mayor o igual a 1.\n");
                    return;
                }

                lista.insertarEnPosicion(valor, posicion);
                vista.txtSalida.setText("✅ Se insertó el valor " + valor + " en la posición " + posicion + ".\n");

            } catch (NumberFormatException ex) {
                vista.txtSalida.setText("❌ Ingresa números válidos para valor y posición.\n");
            }
        }


        // --- BUSCAR NÚMERO ---
        if (e.getSource() == vista.btnBuscar) {
            try {
                int valor = Integer.parseInt(vista.txtBuscar.getText());
                if (lista.p == null) {
                    vista.txtSalida.setText("⚠️ La lista está vacía.\n");
                    return;
                }
                boolean encontrado = false;
                Nodo temp = lista.p;
                while (temp != null) {
                    if (temp.num == valor) {
                        encontrado = true;
                        break;
                    }
                    temp = temp.sig;
                }
                vista.txtSalida.setText(encontrado
                        ? "✅ El número " + valor + " SÍ está en la lista.\n"
                        : "❌ El número " + valor + " NO se encuentra.\n");
            } catch (NumberFormatException ex) {
                vista.txtSalida.setText("❌ Ingresa un número válido para buscar.\n");
            }
        }

        // --- ELIMINAR NÚMERO ---
        if (e.getSource() == vista.btnEliminar) {
            try {
                int valor = Integer.parseInt(vista.txtEliminar.getText());
                if (lista.p == null) {
                    vista.txtSalida.setText("⚠️ No hay lista para eliminar.\n");
                    return;
                }
                eliminarValor(valor);
            } catch (NumberFormatException ex) {
                vista.txtSalida.setText("❌ Ingresa un número válido para eliminar.\n");
            }
        }

        // --- MOSTRAR TAMAÑO ---
        if (e.getSource() == vista.btnTamaño) {
            int contador = 0;
            Nodo temp = lista.p;
            while (temp != null) {
                contador++;
                temp = temp.sig;
            }
            vista.txtSalida.setText("📏 Tamaño actual de la lista: " + contador + " nodos.\n");
        }
    }

    // --- Método auxiliar para eliminar un nodo ---
    private void eliminarValor(int valor) {
        Nodo temp = lista.p;
        while (temp != null) {
            if (temp.num == valor) {
                if (temp.ant != null)
                    temp.ant.sig = temp.sig;
                else
                    lista.p = temp.sig; // era el primero

                if (temp.sig != null)
                    temp.sig.ant = temp.ant;
                vista.txtSalida.setText("✅ Nodo con valor " + valor + " eliminado correctamente.\n");
                return;
            }
            temp = temp.sig;
        }
        vista.txtSalida.setText("❌ El valor " + valor + " no se encontró en la lista.\n");
    }
}
