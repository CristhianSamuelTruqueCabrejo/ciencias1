import tkinter as tk
from tkinter import ttk, messagebox
import random
import threading
import time
from queue import Queue
import math

class Nodo:
    def __init__(self, dato, es_cajero=False):
        self.dato = dato
        self.es_cajero = es_cajero
        self.siguiente = None

class ColaBancoCircular:
    def __init__(self):
        self.cabeza = None
        self.cajero = None
        self.clientes_atendidos = 0
        self.clientes_en_cola = 0
        self.inicializar_cajero()
        
    def inicializar_cajero(self):
        self.cajero = Nodo("CAJERO #1", es_cajero=True)
        self.cabeza = self.cajero
        self.cajero.siguiente = self.cajero
    
    def agregar_cliente(self, id_cliente, transacciones=None):
        if transacciones is None:
            transacciones = random.randint(1, 15)  # 1-15 transacciones aleatorias
        
        nuevo_cliente = Nodo(f"ID: {id_cliente} - T: {transacciones}")
        
        if self.cabeza == self.cajero and self.cajero.siguiente == self.cajero:
            self.cajero.siguiente = nuevo_cliente
            nuevo_cliente.siguiente = self.cajero
        else:
            actual = self.cajero
            while actual.siguiente != self.cajero:
                actual = actual.siguiente
            actual.siguiente = nuevo_cliente
            nuevo_cliente.siguiente = self.cajero
        
        self.clientes_en_cola += 1
        return f"Cliente ID:{id_cliente} agregado con {transacciones} transacciones"
    
    def atender_cliente(self):
        if self.cajero.siguiente == self.cajero:
            return None, "No hay clientes en la cola"
        
        cliente_actual = self.cajero.siguiente
        transacciones = int(cliente_actual.dato.split(":")[-1])
        atendidas = min(transacciones, 5)
        nuevas_transacciones = transacciones - atendidas
        
        if nuevas_transacciones > 0:
            cliente_actual.dato = f"{cliente_actual.dato.split(':')[0]}:{cliente_actual.dato.split(':')[1]}: {nuevas_transacciones}"
            self.mover_al_final(cliente_actual)
            mensaje = f"Atendido ID: {cliente_actual.dato.split(':')[1].strip()} - {atendidas} transacciones (vuelve a cola)"
        else:
            self.eliminar_cliente(cliente_actual)
            self.clientes_atendidos += 1
            self.clientes_en_cola -= 1
            mensaje = f"Atendido ID: {cliente_actual.dato.split(':')[1].strip()} - {atendidas} transacciones (completado)"
        
        return cliente_actual, mensaje
    
    def mover_al_final(self, cliente):
        if cliente.siguiente == self.cajero:
            return
        
        anterior = self.cajero
        while anterior.siguiente != cliente:
            anterior = anterior.siguiente
        
        anterior.siguiente = cliente.siguiente
        ultimo = self.cajero
        while ultimo.siguiente != self.cajero:
            ultimo = ultimo.siguiente
        ultimo.siguiente = cliente
        cliente.siguiente = self.cajero
    
    def eliminar_cliente(self, cliente):
        if self.cajero.siguiente == cliente:
            self.cajero.siguiente = cliente.siguiente
    
    def obtener_cola(self):
        cola = []
        if self.cajero.siguiente == self.cajero:
            return cola
        
        actual = self.cajero.siguiente
        while actual != self.cajero:
            cola.append(actual.dato)
            actual = actual.siguiente
        return cola

class VisualizadorColaCircular:
    def __init__(self, root, cola_banco, event_queue):
        self.root = root
        self.root.title("Visualización Interactiva - Cola Circular del Banco")
        self.root.geometry("900x700")
        
        self.cola_banco = cola_banco
        self.event_queue = event_queue
        self.running = True
        
        self.canvas = tk.Canvas(self.root, width=880, height=600, bg="white")
        self.canvas.pack(pady=10)
        
        # Frame para controles
        frame_controles = ttk.Frame(self.root)
        frame_controles.pack(pady=10)
        
        ttk.Button(frame_controles, text="Actualizar Vista", 
                  command=self.dibujar_cola).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_controles, text="Agregar Cliente Manual", 
                  command=self.agregar_cliente_manual).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_controles, text="Atender Cliente", 
                  command=self.atender_cliente_manual).pack(side=tk.LEFT, padx=5)
        
        # Información
        self.info_label = ttk.Label(self.root, text="", font=("Arial", 10))
        self.info_label.pack(pady=5)
        
        # Iniciar thread de actualización automática
        self.update_thread = threading.Thread(target=self.actualizacion_automatica, daemon=True)
        self.update_thread.start()
        
        self.dibujar_cola()
        
        # Procesar cola de eventos
        self.process_queue()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def actualizacion_automatica(self):
        """Thread para actualizar la visualización automáticamente"""
        while self.running:
            time.sleep(0.5)  # Actualizar cada 500ms
            if not self.running:
                break
                
            # Forzar actualización en el hilo principal de Tkinter
            self.root.after(0, self.dibujar_cola)
    
    def process_queue(self):
        """Procesar eventos de la cola para actualizaciones en tiempo real"""
        try:
            while not self.event_queue.empty():
                event_type, message = self.event_queue.get_nowait()
                
                if event_type == "actualizar_visualizacion":
                    self.dibujar_cola()
                
        except:
            pass
        
        # Programar siguiente verificación
        if self.running:
            self.root.after(100, self.process_queue)
    
    def dibujar_cola(self):
        self.canvas.delete("all")
        
        centro_x, centro_y = 440, 300
        radio = 200
        
        # Dibujar círculo base
        self.canvas.create_oval(centro_x - radio, centro_y - radio, 
                               centro_x + radio, centro_y + radio, 
                               outline="gray", dash=(2, 2), width=2)
        
        # Obtener elementos de la cola
        elementos = ["CAJERO"] + self.cola_banco.obtener_cola()
        
        if len(elementos) == 1:  # Solo el cajero
            self.dibujar_nodo(centro_x, centro_y, elementos[0], es_cajero=True)
            self.info_label.config(text="Solo hay cajero en la cola")
            return
        
        # Calcular posiciones en círculo
        angulo_paso = 2 * math.pi / len(elementos)
        
        for i, elemento in enumerate(elementos):
            angulo = i * angulo_paso
            x = centro_x + radio * math.cos(angulo)
            y = centro_y + radio * math.sin(angulo)
            
            es_cajero = (elemento == "CAJERO")
            self.dibujar_nodo(x, y, elemento, es_cajero)
            
            # Dibujar flecha al siguiente nodo
            if i < len(elementos) - 1:
                angulo_sig = (i + 1) * angulo_paso
                x_sig = centro_x + radio * math.cos(angulo_sig)
                y_sig = centro_y + radio * math.sin(angulo_sig)
                self.dibujar_flecha(x, y, x_sig, y_sig)
            elif len(elementos) > 1:  # Flecha del último al primero (cajero)
                angulo_sig = 0
                x_sig = centro_x + radio * math.cos(angulo_sig)
                y_sig = centro_y + radio * math.sin(angulo_sig)
                self.dibujar_flecha(x, y, x_sig, y_sig)
        
        self.info_label.config(text=f"Elementos en cola: {len(elementos) - 1} | Total: {len(elementos)} | Atendidos: {self.cola_banco.clientes_atendidos}")
    
    def dibujar_nodo(self, x, y, texto, es_cajero=False):
        ancho, alto = 120, 60
        
        if es_cajero:
            color = "lightgreen"
            texto = "CAJERO"
        else:
            color = "lightblue"
            # Acortar texto para que quepa
            if len(texto) > 20:
                texto = texto[:17] + "..."
        
        # Dibujar rectángulo del nodo
        self.canvas.create_rectangle(x - ancho/2, y - alto/2, 
                                   x + ancho/2, y + alto/2, 
                                   fill=color, outline="black", width=2)
        
        # Dibujar texto
        self.canvas.create_text(x, y, text=texto, font=("Arial", 8), width=ancho - 10)
        
        # Indicador especial para cajero
        if es_cajero:
            self.canvas.create_text(x, y - alto/2 - 10, text="INICIO", 
                                  font=("Arial", 9, "bold"), fill="red")
    
    def dibujar_flecha(self, x1, y1, x2, y2):
        # Calcular dirección y ajustar puntos para que salgan del borde del nodo
        dx, dy = x2 - x1, y2 - y1
        distancia = math.sqrt(dx*dx + dy*dy)
        
        if distancia == 0:
            return
            
        # Puntos ajustados para que conecten en los bordes
        factor1 = 60 / distancia  # Radio del nodo
        factor2 = 60 / distancia
        
        x1_adj = x1 + dx * factor1
        y1_adj = y1 + dy * factor1
        x2_adj = x2 - dx * factor2
        y2_adj = y2 - dy * factor2
        
        # Dibujar línea
        self.canvas.create_line(x1_adj, y1_adj, x2_adj, y2_adj, 
                               arrow=tk.LAST, width=2, fill="red")
    
    def agregar_cliente_manual(self):
        # Ventana simple para agregar cliente
        dialogo = tk.Toplevel(self.root)
        dialogo.title("Agregar Cliente")
        dialogo.geometry("300x150")
        dialogo.transient(self.root)
        dialogo.grab_set()
        
        ttk.Label(dialogo, text="ID del Cliente:").pack(pady=5)
        id_entry = ttk.Entry(dialogo)
        id_entry.pack(pady=5)
        
        ttk.Label(dialogo, text="Transacciones:").pack(pady=5)
        trans_entry = ttk.Entry(dialogo)
        trans_entry.pack(pady=5)
        
        def agregar():
            try:
                id_cliente = int(id_entry.get())
                transacciones = int(trans_entry.get())
                mensaje = self.cola_banco.agregar_cliente(id_cliente, transacciones)
                self.event_queue.put(("nuevo_cliente", mensaje))
                self.event_queue.put(("actualizar_visualizacion", ""))
                self.dibujar_cola()
                dialogo.destroy()
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese números válidos")
        
        ttk.Button(dialogo, text="Agregar", command=agregar).pack(pady=10)
    
    def atender_cliente_manual(self):
        cliente, mensaje = self.cola_banco.atender_cliente()
        if cliente:
            self.event_queue.put(("atencion", mensaje))
            self.event_queue.put(("actualizar_visualizacion", ""))
            messagebox.showinfo("Atención", mensaje)
        else:
            messagebox.showinfo("Atención", mensaje)
        self.dibujar_cola()
    
    def on_close(self):
        self.running = False
        self.root.destroy()

class BancoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Banco Automatizado")
        self.root.geometry("750x600")
        
        self.cola = ColaBancoCircular()
        self.id_cliente = 1
        self.event_queue = Queue()
        self.running = True
        
        # Frame para controles
        frame_controles = ttk.LabelFrame(root, text="Controles", padding=10)
        frame_controles.pack(pady=10, padx=10, fill=tk.X)
        
        self.start_btn = ttk.Button(frame_controles, text="Iniciar Simulación", command=self.iniciar_simulacion)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(frame_controles, text="Detener Simulación", command=self.detener_simulacion, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Botón para abrir visualización
        self.viz_btn = ttk.Button(frame_controles, text="Abrir Visualización", command=self.abrir_visualizacion)
        self.viz_btn.pack(side=tk.LEFT, padx=5)
        
        # Frame para estadísticas
        frame_stats = ttk.LabelFrame(root, text="Estadísticas", padding=10)
        frame_stats.pack(pady=10, padx=10, fill=tk.X)
        
        ttk.Label(frame_stats, text="Clientes en cola:").pack(side=tk.LEFT, padx=5)
        self.lbl_en_cola = ttk.Label(frame_stats, text="0")
        self.lbl_en_cola.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(frame_stats, text="Clientes atendidos:").pack(side=tk.LEFT, padx=5)
        self.lbl_atendidos = ttk.Label(frame_stats, text="0")
        self.lbl_atendidos.pack(side=tk.LEFT, padx=5)
        
        # Frame para mensajes
        frame_mensajes = ttk.LabelFrame(root, text="Registro de Eventos", padding=10)
        frame_mensajes.pack(pady=10, padx=10, fill=tk.X)
        
        self.mensaje_text = tk.Text(frame_mensajes, height=5, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(frame_mensajes, orient=tk.VERTICAL, command=self.mensaje_text.yview)
        self.mensaje_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.mensaje_text.pack(fill=tk.BOTH, expand=True)
        
        # Frame para mostrar la cola
        frame_cola = ttk.LabelFrame(root, text="Cola del Banco", padding=10)
        frame_cola.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.cola_tree = ttk.Treeview(frame_cola, columns=('item',), show='headings')
        self.cola_tree.heading('item', text='Elemento en la cola')
        self.cola_tree.column('item', width=700)
        
        scrollbar_cola = ttk.Scrollbar(frame_cola, orient=tk.VERTICAL, command=self.cola_tree.yview)
        self.cola_tree.configure(yscrollcommand=scrollbar_cola.set)
        
        scrollbar_cola.pack(side=tk.RIGHT, fill=tk.Y)
        self.cola_tree.pack(fill=tk.BOTH, expand=True)
        
        # Mostrar cajero al inicio
        self.actualizar_cola()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.process_queue()
        
        # Referencia a la ventana de visualización
        self.ventana_visualizacion = None
    
    def abrir_visualizacion(self):
        if self.ventana_visualizacion is None or not self.ventana_visualizacion.winfo_exists():
            nueva_ventana = tk.Toplevel(self.root)
            self.ventana_visualizacion = VisualizadorColaCircular(nueva_ventana, self.cola, self.event_queue)
            nueva_ventana.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_visualizacion())
        else:
            self.ventana_visualizacion.root.lift()
    
    def cerrar_visualizacion(self):
        self.ventana_visualizacion = None
    
    def iniciar_simulacion(self):
        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        # Thread para llegada de clientes
        threading.Thread(target=self.llegada_clientes, daemon=True).start()
        
        # Thread para atención de clientes
        threading.Thread(target=self.atencion_clientes, daemon=True).start()
    
    def detener_simulacion(self):
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
    
    def llegada_clientes(self):
        while self.running:
            time.sleep(2)  # Cada 2 segundos
            if not self.running:
                break
                
            mensaje = self.cola.agregar_cliente(self.id_cliente)
            self.event_queue.put(("nuevo_cliente", mensaje))
            self.event_queue.put(("actualizar_visualizacion", ""))
            self.id_cliente += 1
    
    def atencion_clientes(self):
        while self.running:
            time.sleep(5)  # Cada 5 segundos
            if not self.running:
                break
                
            cliente, mensaje = self.cola.atender_cliente()
            self.event_queue.put(("atencion", mensaje))
            self.event_queue.put(("actualizar_visualizacion", ""))
    
    def process_queue(self):
        while not self.event_queue.empty():
            event_type, message = self.event_queue.get()
            
            if event_type == "nuevo_cliente":
                self.mensaje_text.insert(tk.END, f"Nuevo cliente: {message}\n")
            elif event_type == "atencion":
                self.mensaje_text.insert(tk.END, f"Atención: {message}\n")
            
            self.mensaje_text.see(tk.END)
            self.actualizar_cola()
            self.actualizar_estadisticas()
        
        self.root.after(100, self.process_queue)
    
    def actualizar_cola(self):
        for item in self.cola_tree.get_children():
            self.cola_tree.delete(item)
        
        self.cola_tree.insert('', tk.END, values=("=== CAJERO PRINCIPAL ===",))
        
        for cliente in self.cola.obtener_cola():
            self.cola_tree.insert('', tk.END, values=(cliente,))
    
    def actualizar_estadisticas(self):
        self.lbl_en_cola.config(text=str(self.cola.clientes_en_cola))
        self.lbl_atendidos.config(text=str(self.cola.clientes_atendidos))
    
    def on_close(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BancoApp(root)
    root.mainloop()