package vista;

import modelo.NodoArbol;
import javax.swing.*;
import java.awt.*;

public class PanelArbol extends JPanel {
    private NodoArbol raiz;
    
    // --- CONSTANTES PARA LA VISUALIZACIÓN DEL NODO ---
    private static final int DIAMETRO_NODO = 45; // Tamaño del círculo (antes 40)
    private static final int RADIO = DIAMETRO_NODO / 2;
    private static final int DISTANCIA_VERTICAL = 80; // Espacio entre niveles (antes 70)
    private static final int DISTANCIA_HORIZONTAL_INICIAL = 450; // Ancho inicial para los hijos de la raíz (antes 400)

    public PanelArbol(NodoArbol raiz) {
        this.raiz = raiz;
        setBackground(Color.WHITE);
        // Ajustamos el tamaño preferido del panel para acomodar un árbol grande y espaciado
        setPreferredSize(new Dimension(1500, 1000)); 
    }

    public void setRaiz(NodoArbol raiz) {
        this.raiz = raiz;
        repaint(); // Redibuja el panel cuando el árbol cambia (al insertar un nodo)
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;
        // Habilita el antialiasing para líneas y texto más suaves
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        if (raiz != null) {
            // Inicia el dibujo en el centro superior del panel
            dibujarArbol(g2d, getWidth() / 2, 30, raiz, DISTANCIA_HORIZONTAL_INICIAL);
        }
    }

    private void dibujarArbol(Graphics2D g, int x, int y, NodoArbol nodo, int anchoHorizontal) {
        if (nodo == null) {
            return;
        }

        // Reducción del espaciado horizontal (para que los hijos estén más cerca)
        int siguienteAncho = (int) (anchoHorizontal * 0.5); 

        int xIzquierda = x - anchoHorizontal;
        int xDerecha = x + anchoHorizontal;

        // 1. Dibujar conexiones (Líneas)
        g.setColor(new Color(150, 150, 150)); // Gris
        g.setStroke(new BasicStroke(2)); // Grosor de línea
        
        if (nodo.izquierda != null) {
            // Conecta el centro inferior del nodo actual al centro superior del hijo izquierdo
            g.drawLine(x, y + RADIO, xIzquierda, y + DISTANCIA_VERTICAL + RADIO);
        }
        if (nodo.derecha != null) {
            // Conecta el centro inferior del nodo actual al centro superior del hijo derecho
            g.drawLine(x, y + RADIO, xDerecha, y + DISTANCIA_VERTICAL + RADIO);
        }
        
        g.setStroke(new BasicStroke(1)); // Restaura el grosor por defecto

        // 2. Dibujar el nodo (Círculo)
        g.setColor(new Color(50, 100, 200)); // Azul oscuro
        // Las coordenadas (x, y) representan el centro del nodo, restamos RADIO para obtener la esquina superior izquierda
        g.fillOval(x - RADIO, y, DIAMETRO_NODO, DIAMETRO_NODO); 
        g.setColor(Color.BLACK);
        g.drawOval(x - RADIO, y, DIAMETRO_NODO, DIAMETRO_NODO);

        // 3. Dibujar el valor del nodo (Texto)
        g.setColor(Color.WHITE);
        g.setFont(new Font("SansSerif", Font.BOLD, 16)); // Letra más grande
        String texto = String.valueOf(nodo.valor);
        FontMetrics fm = g.getFontMetrics();
        
        // CÁLCULO DE CENTRADO DEL TEXTO:
        int textoX = x - (fm.stringWidth(texto) / 2); // Centrado horizontal
        
        // Ajuste vertical para centrar: (y + la mitad del diámetro) - (la mitad de la altura de la fuente) + ajuste
        int textoY = y + RADIO + (fm.getAscent() - fm.getDescent()) / 2;
        
        g.drawString(texto, textoX, textoY);

        // 4. Llamadas recursivas
        int siguienteY = y + DISTANCIA_VERTICAL;

        dibujarArbol(g, xIzquierda, siguienteY, nodo.izquierda, siguienteAncho);
        dibujarArbol(g, xDerecha, siguienteY, nodo.derecha, siguienteAncho);
    }
}