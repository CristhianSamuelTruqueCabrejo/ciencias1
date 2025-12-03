import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
from typing import List, Optional
from math import sin, cos, pi

class Nodo:
    def __init__(self, valor: int):
        self.valor = valor
        self.izquierda: Optional['Nodo'] = None
        self.derecha: Optional['Nodo'] = None
        self.x = 0  # Posición x para dibujo
        self.y = 0  # Posición y para dibujo
        self.radio = 20  # Radio del círculo del nodo

class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz: Optional[Nodo] = None
        self.ancho_canvas = 400
        self.alto_canvas = 300
    
    def insertar(self, valor: int) -> None:
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_recursivo(self.raiz, valor)
    
    def _insertar_recursivo(self, nodo: Nodo, valor: int) -> None:
        if valor < nodo.valor:
            if nodo.izquierda is None:
                nodo.izquierda = Nodo(valor)
            else:
                self._insertar_recursivo(nodo.izquierda, valor)
        else:
            if nodo.derecha is None:
                nodo.derecha = Nodo(valor)
            else:
                self._insertar_recursivo(nodo.derecha, valor)
    
    def limpiar(self):
        """Limpia el árbol completamente"""
        self.raiz = None
    
    def construir_desde_lista(self, lista_numeros: List[int]):
        """Construye el árbol a partir de una lista de números"""
        self.limpiar()
        for num in lista_numeros:
            self.insertar(num)
    
    def preorden(self, nodo: Optional[Nodo] = None) -> List[int]:
        if nodo is None:
            nodo = self.raiz
        resultado = []
        
        def _preorden_recursivo(nodo_actual: Optional[Nodo]):
            if nodo_actual is not None:
                resultado.append(nodo_actual.valor)
                _preorden_recursivo(nodo_actual.izquierda)
                _preorden_recursivo(nodo_actual.derecha)
        
        _preorden_recursivo(nodo)
        return resultado
    
    def inorden(self, nodo: Optional[Nodo] = None) -> List[int]:
        if nodo is None:
            nodo = self.raiz
        resultado = []
        
        def _inorden_recursivo(nodo_actual: Optional[Nodo]):
            if nodo_actual is not None:
                _inorden_recursivo(nodo_actual.izquierda)
                resultado.append(nodo_actual.valor)
                _inorden_recursivo(nodo_actual.derecha)
        
        _inorden_recursivo(nodo)
        return resultado
    
    def posorden(self, nodo: Optional[Nodo] = None) -> List[int]:
        if nodo is None:
            nodo = self.raiz
        resultado = []
        
        def _posorden_recursivo(nodo_actual: Optional[Nodo]):
            if nodo_actual is not None:
                _posorden_recursivo(nodo_actual.izquierda)
                _posorden_recursivo(nodo_actual.derecha)
                resultado.append(nodo_actual.valor)
        
        _posorden_recursivo(nodo)
        return resultado
    
    def obtener_nodos_hoja(self, nodo: Optional[Nodo] = None) -> List[int]:
        if nodo is None:
            nodo = self.raiz
        resultado = []
        
        def _obtener_hojas_recursivo(nodo_actual: Optional[Nodo]):
            if nodo_actual is not None:
                if nodo_actual.izquierda is None and nodo_actual.derecha is None:
                    resultado.append(nodo_actual.valor)
                else:
                    _obtener_hojas_recursivo(nodo_actual.izquierda)
                    _obtener_hojas_recursivo(nodo_actual.derecha)
        
        _obtener_hojas_recursivo(nodo)
        return resultado
    
    def obtener_nodos_no_terminales(self, nodo: Optional[Nodo] = None) -> List[int]:
        if nodo is None:
            nodo = self.raiz
        resultado = []
        
        def _obtener_no_terminales_recursivo(nodo_actual: Optional[Nodo]):
            if nodo_actual is not None:
                if nodo_actual.izquierda is not None or nodo_actual.derecha is not None:
                    resultado.append(nodo_actual.valor)
                _obtener_no_terminales_recursivo(nodo_actual.izquierda)
                _obtener_no_terminales_recursivo(nodo_actual.derecha)
        
        _obtener_no_terminales_recursivo(nodo)
        return resultado
    
    def altura(self, nodo: Optional[Nodo] = None) -> int:
        if nodo is None:
            nodo = self.raiz
        
        def _altura_recursivo(nodo_actual: Optional[Nodo]) -> int:
            if nodo_actual is None:
                return 0
            return 1 + max(_altura_recursivo(nodo_actual.izquierda),
                          _altura_recursivo(nodo_actual.derecha))
        
        return _altura_recursivo(nodo)
    
    def tipo_arbol(self) -> str:
        es_perfecto = self._es_perfecto(self.raiz)
        es_completo = self._es_completo(self.raiz)
        es_degenerado = self._es_degenerado(self.raiz)
        es_balanceado = self._es_balanceado(self.raiz)
        
        if es_perfecto:
            return "Perfecto"
        elif es_completo:
            return "Completo"
        elif es_degenerado:
            return "Degenerado"
        elif es_balanceado:
            return "Balanceado"
        else:
            return "Común"
    
    def _contar_nodos(self, nodo: Optional[Nodo] = None) -> int:
        if nodo is None:
            nodo = self.raiz
        
        def _contar_recursivo(nodo_actual: Optional[Nodo]) -> int:
            if nodo_actual is None:
                return 0
            return 1 + _contar_recursivo(nodo_actual.izquierda) + _contar_recursivo(nodo_actual.derecha)
        
        return _contar_recursivo(nodo)
    
    def _es_completo(self, nodo: Optional[Nodo]) -> bool:
        from collections import deque
        if not nodo:
            return True
        
        queue = deque([nodo])
        nivel_vacio = False
        
        while queue:
            actual = queue.popleft()
            
            if actual is None:
                nivel_vacio = True
            else:
                if nivel_vacio:
                    return False
                queue.append(actual.izquierda)
                queue.append(actual.derecha)
        return True
    
    def _es_perfecto(self, nodo: Optional[Nodo]) -> bool:
        altura = self.altura(nodo)
        total_nodos = self._contar_nodos(nodo)
        return total_nodos == (2 ** altura - 1)
    
    def _es_degenerado(self, nodo: Optional[Nodo]) -> bool:
        if nodo is None:
            return True
        if nodo.izquierda and nodo.derecha:
            return False
        if nodo.izquierda:
            return self._es_degenerado(nodo.izquierda)
        if nodo.derecha:
            return self._es_degenerado(nodo.derecha)
        return True
    
    def _es_balanceado(self, nodo: Optional[Nodo]) -> bool:
        def _check_balance(nodo_actual: Optional[Nodo]) -> int:
            if nodo_actual is None:
                return 0
            
            altura_izq = _check_balance(nodo_actual.izquierda)
            if altura_izq == -1:
                return -1
            
            altura_der = _check_balance(nodo_actual.derecha)
            if altura_der == -1:
                return -1
            
            if abs(altura_izq - altura_der) > 1:
                return -1
            
            return max(altura_izq, altura_der) + 1
        
        return _check_balance(nodo) != -1
    
    def calcular_posiciones(self, canvas_ancho: int, canvas_alto: int):
        """Calcula las posiciones de todos los nodos para el dibujo"""
        if not self.raiz:
            return
        
        altura = self.altura()
        if altura == 0:
            return
        
        # Configurar dimensiones del canvas
        self.ancho_canvas = canvas_ancho
        self.alto_canvas = canvas_alto
        
        # Espaciado entre niveles
        espacio_y = (canvas_alto - 100) / max(altura, 1)
        
        # Calcular posiciones usando BFS
        from collections import deque
        queue = deque([(self.raiz, canvas_ancho // 2, 50, canvas_ancho // 2)])
        
        while queue:
            nodo, x, y, ancho_seccion = queue.popleft()
            nodo.x = x
            nodo.y = y
            
            if nodo.izquierda:
                nuevo_x = x - ancho_seccion // 2
                queue.append((nodo.izquierda, nuevo_x, y + espacio_y, ancho_seccion // 2))
            
            if nodo.derecha:
                nuevo_x = x + ancho_seccion // 2
                queue.append((nodo.derecha, nuevo_x, y + espacio_y, ancho_seccion // 2))
    
    def dibujar_en_canvas(self, canvas: tk.Canvas):
        """Dibuja el árbol completo en el canvas proporcionado"""
        if not self.raiz:
            canvas.create_text(self.ancho_canvas // 2, self.alto_canvas // 2, 
                             text="Árbol vacío", font=("Arial", 14))
            return
        
        # Limpiar canvas
        canvas.delete("all")
        
        # Calcular posiciones primero
        self.calcular_posiciones(self.ancho_canvas, self.alto_canvas)
        
        # Dibujar conexiones primero (para que queden detrás de los nodos)
        self._dibujar_conexiones(canvas, self.raiz)
        
        # Dibujar nodos después
        self._dibujar_nodos(canvas, self.raiz)
    
    def _dibujar_conexiones(self, canvas: tk.Canvas, nodo: Optional[Nodo]):
        """Dibuja las líneas que conectan los nodos"""
        if nodo is None:
            return
        
        # Dibujar conexión con hijo izquierdo
        if nodo.izquierda:
            canvas.create_line(nodo.x, nodo.y, 
                             nodo.izquierda.x, nodo.izquierda.y,
                             width=2, fill="blue")
            self._dibujar_conexiones(canvas, nodo.izquierda)
        
        # Dibujar conexión con hijo derecho
        if nodo.derecha:
            canvas.create_line(nodo.x, nodo.y,
                             nodo.derecha.x, nodo.derecha.y,
                             width=2, fill="blue")
            self._dibujar_conexiones(canvas, nodo.derecha)
    
    def _dibujar_nodos(self, canvas: tk.Canvas, nodo: Optional[Nodo]):
        """Dibuja los nodos del árbol"""
        if nodo is None:
            return
        
        # Determinar color del nodo
        color = "lightgreen" if nodo.izquierda is None and nodo.derecha is None else "lightblue"
        
        # Dibujar círculo del nodo
        canvas.create_oval(nodo.x - nodo.radio, nodo.y - nodo.radio,
                          nodo.x + nodo.radio, nodo.y + nodo.radio,
                          fill=color, outline="black", width=2)
        
        # Dibujar texto del valor
        canvas.create_text(nodo.x, nodo.y, text=str(nodo.valor),
                          font=("Arial", 10, "bold"))
        
        # Dibujar hijos recursivamente
        self._dibujar_nodos(canvas, nodo.izquierda)
        self._dibujar_nodos(canvas, nodo.derecha)

def son_iguales(arbol1: ArbolBinarioBusqueda, arbol2: ArbolBinarioBusqueda) -> bool:
    def _iguales_recursivo(nodo1: Optional[Nodo], nodo2: Optional[Nodo]) -> bool:
        if nodo1 is None and nodo2 is None:
            return True
        if nodo1 is None or nodo2 is None:
            return False
        return (nodo1.valor == nodo2.valor and
                _iguales_recursivo(nodo1.izquierda, nodo2.izquierda) and
                _iguales_recursivo(nodo1.derecha, nodo2.derecha))
    return _iguales_recursivo(arbol1.raiz, arbol2.raiz)

def son_isomorfos(arbol1: ArbolBinarioBusqueda, arbol2: ArbolBinarioBusqueda) -> bool:
    def _isomorfos_recursivo(nodo1: Optional[Nodo], nodo2: Optional[Nodo]) -> bool:
        if nodo1 is None and nodo2 is None:
            return True
        if nodo1 is None or nodo2 is None:
            return False
        return (_isomorfos_recursivo(nodo1.izquierda, nodo2.izquierda) and
                _isomorfos_recursivo(nodo1.derecha, nodo2.derecha))
    return _isomorfos_recursivo(arbol1.raiz, arbol2.raiz)

def validar_serie_numeros(entrada: str) -> List[int]:
    """Valida y convierte una cadena de números separados por comas en una lista"""
    try:
        # Limpiar espacios y dividir por comas
        numeros_str = entrada.strip().split(',')
        numeros = []
        
        for num_str in numeros_str:
            if num_str.strip():  # Ignorar cadenas vacías
                num = int(num_str.strip())
                if num < 0:
                    raise ValueError("Los números no pueden ser negativos")
                numeros.append(num)
        
        return numeros
    except ValueError as e:
        raise ValueError(f"Entrada inválida: {e}. Use números enteros separados por comas.")

class VentanaManual:
    """Ventana para ingresar árboles manualmente"""
    def __init__(self, parent, app_principal):
        self.parent = parent
        self.app = app_principal
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Ingresar Árboles Manualmente")
        self.ventana.geometry("600x400")
        self.ventana.configure(bg='#2c3e50')
        
        # Hacer la ventana modal
        self.ventana.transient(parent)
        self.ventana.grab_set()
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.ventana, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar pesos
        self.ventana.columnconfigure(0, weight=1)
        self.ventana.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        titulo = tk.Label(main_frame, text="📝 Ingresar Árboles Manualmente", 
                         font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white')
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Instrucciones
        instrucciones = tk.Label(main_frame, 
                                text="Ingrese números enteros separados por comas.\nEjemplo: 50, 30, 70, 20, 40, 60, 80",
                                font=('Arial', 10), bg='#2c3e50', fg='white')
        instrucciones.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Frame para Árbol 1
        frame_arbol1 = ttk.LabelFrame(main_frame, text="🌳 Árbol 1", padding="10")
        frame_arbol1.grid(row=2, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        tk.Label(frame_arbol1, text="Serie de números:", font=('Arial', 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_arbol1 = tk.Entry(frame_arbol1, width=30, font=('Arial', 10))
        self.entry_arbol1.grid(row=1, column=0, pady=5)
        
        # Ejemplo para Árbol 1
        ejemplo1 = tk.Button(frame_arbol1, text="Ejemplo 1", command=lambda: self.cargar_ejemplo(1),
                           font=('Arial', 9))
        ejemplo1.grid(row=2, column=0, pady=5)
        
        # Frame para Árbol 2
        frame_arbol2 = ttk.LabelFrame(main_frame, text="🌳 Árbol 2", padding="10")
        frame_arbol2.grid(row=2, column=1, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        tk.Label(frame_arbol2, text="Serie de números:", font=('Arial', 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_arbol2 = tk.Entry(frame_arbol2, width=30, font=('Arial', 10))
        self.entry_arbol2.grid(row=1, column=0, pady=5)
        
        # Ejemplo para Árbol 2
        ejemplo2 = tk.Button(frame_arbol2, text="Ejemplo 2", command=lambda: self.cargar_ejemplo(2),
                           font=('Arial', 9))
        ejemplo2.grid(row=2, column=0, pady=5)
        
        # Frame para botones
        frame_botones = ttk.Frame(main_frame)
        frame_botones.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Botón para generar árboles aleatorios
        btn_aleatorio = ttk.Button(frame_botones, text="🎲 Aleatorio para ambos",
                                  command=self.generar_aleatorios)
        btn_aleatorio.grid(row=0, column=0, padx=10)
        
        # Botón para aplicar
        btn_aplicar = ttk.Button(frame_botones, text="✅ Aplicar y Cerrar",
                                command=self.aplicar_cambios)
        btn_aplicar.grid(row=0, column=1, padx=10)
        
        # Botón para cancelar
        btn_cancelar = ttk.Button(frame_botones, text="❌ Cancelar",
                                 command=self.ventana.destroy)
        btn_cancelar.grid(row=0, column=2, padx=10)
        
        # Área de información
        self.label_info = tk.Label(main_frame, text="", font=('Arial', 10), 
                                  fg='yellow', bg='#2c3e50')
        self.label_info.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Cargar valores actuales si existen
        if self.app.serie1:
            self.entry_arbol1.insert(0, ', '.join(map(str, self.app.serie1)))
        if self.app.serie2:
            self.entry_arbol2.insert(0, ', '.join(map(str, self.app.serie2)))
    
    def cargar_ejemplo(self, arbol_num: int):
        """Carga ejemplos predefinidos"""
        ejemplos = {
            1: "50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45",
            2: "100, 50, 150, 25, 75, 125, 175, 12, 37, 63, 88"
        }
        
        if arbol_num == 1:
            self.entry_arbol1.delete(0, tk.END)
            self.entry_arbol1.insert(0, ejemplos[1])
        else:
            self.entry_arbol2.delete(0, tk.END)
            self.entry_arbol2.insert(0, ejemplos[2])
    
    def generar_aleatorios(self):
        """Genera series aleatorias para ambos árboles"""
        serie1 = self.app.generar_serie_aleatoria()
        serie2 = self.app.generar_serie_aleatoria()
        
        self.entry_arbol1.delete(0, tk.END)
        self.entry_arbol1.insert(0, ', '.join(map(str, serie1)))
        
        self.entry_arbol2.delete(0, tk.END)
        self.entry_arbol2.insert(0, ', '.join(map(str, serie2)))
        
        self.label_info.config(text="✅ Series aleatorias generadas", fg="green")
    
    def aplicar_cambios(self):
        """Aplica los cambios y cierra la ventana"""
        try:
            # Validar y obtener serie del árbol 1
            texto_arbol1 = self.entry_arbol1.get().strip()
            serie1 = []
            if texto_arbol1:
                serie1 = validar_serie_numeros(texto_arbol1)
            
            # Validar y obtener serie del árbol 2
            texto_arbol2 = self.entry_arbol2.get().strip()
            serie2 = []
            if texto_arbol2:
                serie2 = validar_serie_numeros(texto_arbol2)
            
            # Verificar que al menos un árbol tenga datos
            if not serie1 and not serie2:
                messagebox.showwarning("Advertencia", "Ingrese al menos un árbol")
                return
            
            # Actualizar series en la aplicación principal
            self.app.serie1 = serie1
            self.app.serie2 = serie2
            
            # Reconstruir árboles
            self.app.arbol1.construir_desde_lista(serie1)
            self.app.arbol2.construir_desde_lista(serie2)
            
            # Actualizar interfaz
            self.app.actualizar_informacion()
            self.app.dibujar_arboles()
            
            # Mostrar mensaje de éxito
            mensaje = f"✅ Árboles actualizados correctamente\n"
            mensaje += f"🌳 Árbol 1: {len(serie1)} nodos\n"
            mensaje += f"🌳 Árbol 2: {len(serie2)} nodos"
            
            messagebox.showinfo("Éxito", mensaje)
            
            # Cerrar ventana
            self.ventana.destroy()
            
        except ValueError as e:
            self.label_info.config(text=f"❌ Error: {str(e)}", fg="red")
        except Exception as e:
            self.label_info.config(text=f"❌ Error inesperado: {str(e)}", fg="red")

class AplicacionArboles:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto Final - Árboles Binarios de Búsqueda")
        self.root.geometry("1400x900")
        
        # Variables para los árboles
        self.arbol1 = ArbolBinarioBusqueda()
        self.arbol2 = ArbolBinarioBusqueda()
        self.serie1 = []
        self.serie2 = []
        
        # Configurar estilo
        self.setup_estilos()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Generar árboles iniciales
        self.generar_arboles()
        
    def setup_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores
        self.root.configure(bg='#2c3e50')
        
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar pesos
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        titulo = tk.Label(main_frame, text="🌳 PROYECTO FINAL - ÁRBOLES BINARIOS DE BÚSQUEDA 🌳", 
                         font=('Arial', 20, 'bold'), bg='#2c3e50', fg='white')
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frame para controles
        controles_frame = ttk.LabelFrame(main_frame, text="🎮 Controles", padding="10")
        controles_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Botones de control
        btn_generar = ttk.Button(controles_frame, text="🎲 Generar Árboles Aleatorios", 
                                command=self.generar_arboles)
        btn_generar.grid(row=0, column=0, padx=5, pady=5)
        
        btn_manual = ttk.Button(controles_frame, text="📝 Ingresar Árboles Manualmente",
                               command=self.abrir_ventana_manual)
        btn_manual.grid(row=0, column=1, padx=5, pady=5)
        
        btn_mostrar_info = ttk.Button(controles_frame, text="📊 Mostrar Información Completa",
                                     command=self.mostrar_informacion_completa)
        btn_mostrar_info.grid(row=0, column=2, padx=5, pady=5)
        
        btn_comparar = ttk.Button(controles_frame, text="⚖️ Comparar Árboles",
                                 command=self.comparar_arboles)
        btn_comparar.grid(row=0, column=3, padx=5, pady=5)
        
        # Frame para visualización de árboles
        visual_frame = ttk.LabelFrame(main_frame, text="🌿 Visualización de Árboles", padding="10")
        visual_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Configurar pesos para visual_frame
        visual_frame.columnconfigure(0, weight=1)
        visual_frame.columnconfigure(1, weight=1)
        visual_frame.rowconfigure(0, weight=1)
        
        # Canvas para Árbol 1
        arbol1_canvas_frame = ttk.LabelFrame(visual_frame, text="Árbol 1", padding="5")
        arbol1_canvas_frame.grid(row=0, column=0, padx=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        arbol1_canvas_frame.columnconfigure(0, weight=1)
        arbol1_canvas_frame.rowconfigure(0, weight=1)
        
        self.canvas_arbol1 = tk.Canvas(arbol1_canvas_frame, width=400, height=300, 
                                      bg='white', relief=tk.SUNKEN, bd=2)
        self.canvas_arbol1.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Canvas para Árbol 2
        arbol2_canvas_frame = ttk.LabelFrame(visual_frame, text="Árbol 2", padding="5")
        arbol2_canvas_frame.grid(row=0, column=1, padx=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        arbol2_canvas_frame.columnconfigure(0, weight=1)
        arbol2_canvas_frame.rowconfigure(0, weight=1)
        
        self.canvas_arbol2 = tk.Canvas(arbol2_canvas_frame, width=400, height=300, 
                                      bg='white', relief=tk.SUNKEN, bd=2)
        self.canvas_arbol2.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame para información de árboles
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Frame para información del Árbol 1
        info_arbol1_frame = ttk.LabelFrame(info_frame, text="📋 Información Árbol 1", padding="10")
        info_arbol1_frame.grid(row=0, column=0, padx=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame para información del Árbol 2
        info_arbol2_frame = ttk.LabelFrame(info_frame, text="📋 Información Árbol 2", padding="10")
        info_arbol2_frame.grid(row=0, column=1, padx=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar pesos para info_frame
        info_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(1, weight=1)
        
        # Información del Árbol 1
        self.lbl_serie1 = tk.Label(info_arbol1_frame, text="🔢 Serie 1: ", anchor="w", justify=tk.LEFT)
        self.lbl_serie1.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.lbl_preorden1 = tk.Label(info_arbol1_frame, text="⬇️ Preorden: ", anchor="w", justify=tk.LEFT)
        self.lbl_preorden1.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.lbl_inorden1 = tk.Label(info_arbol1_frame, text="↔️ Inorden: ", anchor="w", justify=tk.LEFT)
        self.lbl_inorden1.grid(row=2, column=0, sticky=tk.W, pady=2)
        
        self.lbl_posorden1 = tk.Label(info_arbol1_frame, text="⬆️ Posorden: ", anchor="w", justify=tk.LEFT)
        self.lbl_posorden1.grid(row=3, column=0, sticky=tk.W, pady=2)
        
        self.lbl_tipo1 = tk.Label(info_arbol1_frame, text="🏷️ Tipo: ", anchor="w", justify=tk.LEFT)
        self.lbl_tipo1.grid(row=4, column=0, sticky=tk.W, pady=2)
        
        self.lbl_hojas1 = tk.Label(info_arbol1_frame, text="🍃 Nodos Hoja: ", anchor="w", justify=tk.LEFT)
        self.lbl_hojas1.grid(row=5, column=0, sticky=tk.W, pady=2)
        
        self.lbl_no_terminales1 = tk.Label(info_arbol1_frame, text="🌿 Nodos No Terminales: ", anchor="w", justify=tk.LEFT)
        self.lbl_no_terminales1.grid(row=6, column=0, sticky=tk.W, pady=2)
        
        self.lbl_altura1 = tk.Label(info_arbol1_frame, text="📏 Altura: ", anchor="w", justify=tk.LEFT)
        self.lbl_altura1.grid(row=7, column=0, sticky=tk.W, pady=2)
        
        # Botón para limpiar árbol 1
        self.btn_limpiar1 = ttk.Button(info_arbol1_frame, text="🗑️ Limpiar Árbol 1",
                                      command=lambda: self.limpiar_arbol(1))
        self.btn_limpiar1.grid(row=8, column=0, pady=10, sticky=tk.W)
        
        # Información del Árbol 2
        self.lbl_serie2 = tk.Label(info_arbol2_frame, text="🔢 Serie 2: ", anchor="w", justify=tk.LEFT)
        self.lbl_serie2.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.lbl_preorden2 = tk.Label(info_arbol2_frame, text="⬇️ Preorden: ", anchor="w", justify=tk.LEFT)
        self.lbl_preorden2.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.lbl_inorden2 = tk.Label(info_arbol2_frame, text="↔️ Inorden: ", anchor="w", justify=tk.LEFT)
        self.lbl_inorden2.grid(row=2, column=0, sticky=tk.W, pady=2)
        
        self.lbl_posorden2 = tk.Label(info_arbol2_frame, text="⬆️ Posorden: ", anchor="w", justify=tk.LEFT)
        self.lbl_posorden2.grid(row=3, column=0, sticky=tk.W, pady=2)
        
        self.lbl_tipo2 = tk.Label(info_arbol2_frame, text="🏷️ Tipo: ", anchor="w", justify=tk.LEFT)
        self.lbl_tipo2.grid(row=4, column=0, sticky=tk.W, pady=2)
        
        self.lbl_hojas2 = tk.Label(info_arbol2_frame, text="🍃 Nodos Hoja: ", anchor="w", justify=tk.LEFT)
        self.lbl_hojas2.grid(row=5, column=0, sticky=tk.W, pady=2)
        
        self.lbl_no_terminales2 = tk.Label(info_arbol2_frame, text="🌿 Nodos No Terminales: ", anchor="w", justify=tk.LEFT)
        self.lbl_no_terminales2.grid(row=6, column=0, sticky=tk.W, pady=2)
        
        self.lbl_altura2 = tk.Label(info_arbol2_frame, text="📏 Altura: ", anchor="w", justify=tk.LEFT)
        self.lbl_altura2.grid(row=7, column=0, sticky=tk.W, pady=2)
        
        # Botón para limpiar árbol 2
        self.btn_limpiar2 = ttk.Button(info_arbol2_frame, text="🗑️ Limpiar Árbol 2",
                                      command=lambda: self.limpiar_arbol(2))
        self.btn_limpiar2.grid(row=8, column=0, pady=10, sticky=tk.W)
        
        # Área de texto para resultados detallados
        resultados_frame = ttk.LabelFrame(main_frame, text="📄 Resultados Detallados", padding="10")
        resultados_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        resultados_frame.columnconfigure(0, weight=1)
        resultados_frame.rowconfigure(0, weight=1)
        
        self.txt_resultados = scrolledtext.ScrolledText(resultados_frame, width=100, height=10,
                                                       font=("Consolas", 10))
        self.txt_resultados.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Leyenda
        leyenda_frame = ttk.Frame(main_frame)
        leyenda_frame.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        tk.Label(leyenda_frame, text="🎨 Leyenda: ", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        tk.Label(leyenda_frame, text="● Nodo hoja", fg="darkgreen", font=("Arial", 9)).grid(row=0, column=1, padx=5)
        tk.Label(leyenda_frame, text="● Nodo interno", fg="darkblue", font=("Arial", 9)).grid(row=0, column=2, padx=5)
        tk.Label(leyenda_frame, text="--- Conexión", fg="blue", font=("Arial", 9)).grid(row=0, column=3, padx=5)
    
    def abrir_ventana_manual(self):
        """Abre la ventana para ingresar árboles manualmente"""
        VentanaManual(self.root, self)
    
    def generar_serie_aleatoria(self, n: int = 10, rango_min: int = 1, rango_max: int = 100) -> List[int]:
        """Genera una serie aleatoria de números únicos"""
        if rango_max - rango_min + 1 < n:
            # Si el rango es muy pequeño, permitir duplicados
            return [random.randint(rango_min, rango_max) for _ in range(n)]
        return random.sample(range(rango_min, rango_max + 1), n)
    
    def generar_arboles(self):
        """Genera árboles aleatorios"""
        # Generar series aleatorias
        self.serie1 = self.generar_serie_aleatoria()
        self.serie2 = self.generar_serie_aleatoria()
        
        # Construir árboles
        self.arbol1 = ArbolBinarioBusqueda()
        self.arbol2 = ArbolBinarioBusqueda()
        
        for num in self.serie1:
            self.arbol1.insertar(num)
        
        for num in self.serie2:
            self.arbol2.insertar(num)
        
        # Actualizar interfaz
        self.actualizar_informacion()
        self.dibujar_arboles()
        
        # Mostrar mensaje
        self.txt_resultados.delete(1.0, tk.END)
        self.txt_resultados.insert(tk.END, "✅ Árboles aleatorios generados correctamente\n")
    
    def dibujar_arboles(self):
        """Dibuja los árboles en los canvases"""
        # Dibujar árbol 1
        self.arbol1.dibujar_en_canvas(self.canvas_arbol1)
        
        # Dibujar árbol 2
        self.arbol2.dibujar_en_canvas(self.canvas_arbol2)
    
    def actualizar_informacion(self):
        """Actualiza toda la información mostrada en la interfaz"""
        # Actualizar información del árbol 1
        self.lbl_serie1.config(text=f"🔢 Serie 1: {self.serie1 if self.serie1 else 'Vacío'}")
        self.lbl_preorden1.config(text=f"⬇️ Preorden: {self.arbol1.preorden() if self.serie1 else 'Vacío'}")
        self.lbl_inorden1.config(text=f"↔️ Inorden: {self.arbol1.inorden() if self.serie1 else 'Vacío'}")
        self.lbl_posorden1.config(text=f"⬆️ Posorden: {self.arbol1.posorden() if self.serie1 else 'Vacío'}")
        self.lbl_tipo1.config(text=f"🏷️ Tipo: {self.arbol1.tipo_arbol() if self.serie1 else 'Vacío'}")
        self.lbl_hojas1.config(text=f"🍃 Nodos Hoja: {self.arbol1.obtener_nodos_hoja() if self.serie1 else 'Vacío'}")
        self.lbl_no_terminales1.config(text=f"🌿 Nodos No Terminales: {self.arbol1.obtener_nodos_no_terminales() if self.serie1 else 'Vacío'}")
        self.lbl_altura1.config(text=f"📏 Altura: {self.arbol1.altura() if self.serie1 else '0'}")
        
        # Actualizar información del árbol 2
        self.lbl_serie2.config(text=f"🔢 Serie 2: {self.serie2 if self.serie2 else 'Vacío'}")
        self.lbl_preorden2.config(text=f"⬇️ Preorden: {self.arbol2.preorden() if self.serie2 else 'Vacío'}")
        self.lbl_inorden2.config(text=f"↔️ Inorden: {self.arbol2.inorden() if self.serie2 else 'Vacío'}")
        self.lbl_posorden2.config(text=f"⬆️ Posorden: {self.arbol2.posorden() if self.serie2 else 'Vacío'}")
        self.lbl_tipo2.config(text=f"🏷️ Tipo: {self.arbol2.tipo_arbol() if self.serie2 else 'Vacío'}")
        self.lbl_hojas2.config(text=f"🍃 Nodos Hoja: {self.arbol2.obtener_nodos_hoja() if self.serie2 else 'Vacío'}")
        self.lbl_no_terminales2.config(text=f"🌿 Nodos No Terminales: {self.arbol2.obtener_nodos_no_terminales() if self.serie2 else 'Vacío'}")
        self.lbl_altura2.config(text=f"📏 Altura: {self.arbol2.altura() if self.serie2 else '0'}")
    
    def limpiar_arbol(self, numero_arbol: int):
        """Limpia un árbol específico"""
        if numero_arbol == 1:
            self.arbol1.limpiar()
            self.serie1 = []
            self.txt_resultados.insert(tk.END, "🗑️ Árbol 1 limpiado\n")
        else:
            self.arbol2.limpiar()
            self.serie2 = []
            self.txt_resultados.insert(tk.END, "🗑️ Árbol 2 limpiado\n")
        
        self.actualizar_informacion()
        self.dibujar_arboles()
    
    def mostrar_informacion_completa(self):
        """Muestra toda la información detallada de los árboles"""
        texto = "=" * 70 + "\n"
        texto += "📊 INFORMACIÓN COMPLETA DE LOS ÁRBOLES\n"
        texto += "=" * 70 + "\n\n"
        
        # Información Árbol 1
        texto += "🌳 ÁRBOL 1:\n"
        texto += "-" * 40 + "\n"
        texto += f"🔢 Serie de números: {self.serie1 if self.serie1 else 'Árbol vacío'}\n"
        if self.serie1:
            texto += f"⬇️  Preorden: {self.arbol1.preorden()}\n"
            texto += f"↔️  Inorden: {self.arbol1.inorden()}\n"
            texto += f"⬆️  Posorden: {self.arbol1.posorden()}\n"
            texto += f"🏷️  Tipo de árbol: {self.arbol1.tipo_arbol()}\n"
            texto += f"🍃 Nodos hoja: {self.arbol1.obtener_nodos_hoja()}\n"
            texto += f"🌿 Nodos no terminales: {self.arbol1.obtener_nodos_no_terminales()}\n"
            texto += f"📏 Altura: {self.arbol1.altura()}\n"
            texto += f"🔢 Total nodos: {self.arbol1._contar_nodos()}\n"
        texto += "\n"
        
        # Información Árbol 2
        texto += "🌳 ÁRBOL 2:\n"
        texto += "-" * 40 + "\n"
        texto += f"🔢 Serie de números: {self.serie2 if self.serie2 else 'Árbol vacío'}\n"
        if self.serie2:
            texto += f"⬇️  Preorden: {self.arbol2.preorden()}\n"
            texto += f"↔️  Inorden: {self.arbol2.inorden()}\n"
            texto += f"⬆️  Posorden: {self.arbol2.posorden()}\n"
            texto += f"🏷️  Tipo de árbol: {self.arbol2.tipo_arbol()}\n"
            texto += f"🍃 Nodos hoja: {self.arbol2.obtener_nodos_hoja()}\n"
            texto += f"🌿 Nodos no terminales: {self.arbol2.obtener_nodos_no_terminales()}\n"
            texto += f"📏 Altura: {self.arbol2.altura()}\n"
            texto += f"🔢 Total nodos: {self.arbol2._contar_nodos()}\n"
        
        self.txt_resultados.delete(1.0, tk.END)
        self.txt_resultados.insert(tk.END, texto)
    
    def comparar_arboles(self):
        """Compara los dos árboles y muestra los resultados"""
        iguales = son_iguales(self.arbol1, self.arbol2)
        isomorfos = son_isomorfos(self.arbol1, self.arbol2)
        
        texto = "\n" + "=" * 70 + "\n"
        texto += "⚖️ COMPARACIÓN DE ÁRBOLES\n"
        texto += "=" * 70 + "\n\n"
        
        # Verificar si algún árbol está vacío
        arbol1_vacio = not self.serie1
        arbol2_vacio = not self.serie2
        
        if arbol1_vacio or arbol2_vacio:
            texto += "⚠️  Advertencia: Uno o ambos árboles están vacíos\n\n"
        
        if arbol1_vacio and arbol2_vacio:
            texto += "Ambos árboles están vacíos → Son iguales e isomorfos\n"
        elif arbol1_vacio or arbol2_vacio:
            texto += "No se pueden comparar árboles vacíos con no vacíos\n"
        else:
            if iguales:
                texto += "✅ Los árboles son IGUALES\n"
                texto += "   (Misma estructura y mismos valores en los nodos)\n"
            else:
                texto += "❌ Los árboles NO son iguales\n"
            
            texto += "\n"
            
            if isomorfos:
                texto += "✅ Los árboles son ISOMORFOS\n"
                texto += "   (Misma estructura, valores pueden ser diferentes)\n"
            else:
                texto += "❌ Los árboles NO son isomorfos\n"
                texto += "   (Estructura diferente)\n"
        
        texto += "\n" + "-" * 40 + "\n"
        texto += "📋 RESUMEN:\n"
        texto += f"🌳 Árbol 1: {self.arbol1.tipo_arbol() if self.serie1 else 'Vacío'} "
        texto += f"(Altura: {self.arbol1.altura() if self.serie1 else '0'})\n"
        texto += f"🌳 Árbol 2: {self.arbol2.tipo_arbol() if self.serie2 else 'Vacío'} "
        texto += f"(Altura: {self.arbol2.altura() if self.serie2 else '0'})\n"
        
        if not (arbol1_vacio or arbol2_vacio):
            texto += f"🔗 Son iguales: {'✅ Sí' if iguales else '❌ No'}\n"
            texto += f"🔄 Son isomorfos: {'✅ Sí' if isomorfos else '❌ No'}\n"
        
        # Mostrar en el área de texto
        self.txt_resultados.delete(1.0, tk.END)
        self.txt_resultados.insert(tk.END, texto)
        
        # Mostrar mensaje emergente solo si ambos árboles tienen datos
        if not arbol1_vacio and not arbol2_vacio:
            mensaje = f"🌳 Árbol 1: {self.arbol1.tipo_arbol()}\n"
            mensaje += f"🌳 Árbol 2: {self.arbol2.tipo_arbol()}\n\n"
            mensaje += f"🔗 Iguales: {'✅ Sí' if iguales else '❌ No'}\n"
            mensaje += f"🔄 Isomorfos: {'✅ Sí' if isomorfos else '❌ No'}"
            
            messagebox.showinfo("⚖️ Resultado de Comparación", mensaje)

def main():
    root = tk.Tk()
    app = AplicacionArboles(root)
    root.mainloop()

if __name__ == "__main__":
    main()