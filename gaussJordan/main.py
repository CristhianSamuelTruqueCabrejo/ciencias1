import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np

class GaussJordanSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Solver de Ecuaciones Lineales - Gauss-Jordan")
        self.root.geometry("800x600")
        
        # Variables
        self.num_ecuaciones = tk.IntVar(value=2)
        self.num_variables = tk.IntVar(value=2)
        self.matriz_entries = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz gráfica - Complejidad: O(1) (configuración inicial)"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Configuración del sistema
        config_frame = ttk.LabelFrame(main_frame, text="Configuración del Sistema", padding="10")
        config_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(config_frame, text="Número de ecuaciones:").grid(row=0, column=0, sticky=tk.W)
        ttk.Spinbox(config_frame, from_=1, to=10, textvariable=self.num_ecuaciones, 
                   command=self.actualizar_matriz, width=10).grid(row=0, column=1, padx=(10, 20))
        
        ttk.Label(config_frame, text="Número de variables:").grid(row=0, column=2, sticky=tk.W)
        ttk.Spinbox(config_frame, from_=1, to=10, textvariable=self.num_variables, 
                   command=self.actualizar_matriz, width=10).grid(row=0, column=3, padx=(10, 0))
        
        # Matriz de coeficientes
        self.matriz_frame = ttk.LabelFrame(main_frame, text="Matriz de Coeficientes", padding="10")
        self.matriz_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Button(button_frame, text="Resolver", command=self.resolver).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Limpiar", command=self.limpiar).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Ejemplo", command=self.cargar_ejemplo).pack(side=tk.LEFT)
        
        # Resultados
        resultados_frame = ttk.LabelFrame(main_frame, text="Resultados y Proceso", padding="10")
        resultados_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar weights para expansión
        main_frame.rowconfigure(3, weight=1)
        resultados_frame.columnconfigure(0, weight=1)
        resultados_frame.rowconfigure(0, weight=1)
        
        self.texto_resultados = scrolledtext.ScrolledText(resultados_frame, width=80, height=15, wrap=tk.WORD)
        self.texto_resultados.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.actualizar_matriz()
    
    def actualizar_matriz(self):
        """
        PASO 1 y 2: Ver y almacenar cantidad de ecuaciones y variables
        Complejidad: O(n × m) donde n = ecuaciones, m = variables
        """
        # Limpiar frame anterior - O(k) donde k = número de widgets existentes
        for widget in self.matriz_frame.winfo_children():
            widget.destroy()
        
        # Obtener número de ecuaciones y variables - O(1)
        n_ec = self.num_ecuaciones.get()
        n_var = self.num_variables.get()
        self.matriz_entries = []
        
        # Crear encabezados - O(m)
        for j in range(n_var):
            ttk.Label(self.matriz_frame, text=f"x{j+1}").grid(row=0, column=j+1, padx=5, pady=5)
        ttk.Label(self.matriz_frame, text="T.I.").grid(row=0, column=n_var+1, padx=5, pady=5)
        
        # Crear entradas para la matriz - O(n × m)
        for i in range(n_ec):
            ttk.Label(self.matriz_frame, text=f"Ec {i+1}:").grid(row=i+1, column=0, padx=5, pady=2)
            fila_entries = []
            for j in range(n_var + 1):  # +1 para el término independiente
                entry = ttk.Entry(self.matriz_frame, width=8)
                entry.grid(row=i+1, column=j+1, padx=2, pady=2)
                fila_entries.append(entry)
            self.matriz_entries.append(fila_entries)
    
    def obtener_matriz(self):
        """
        PASO 3: Generar la matriz aumentada de tamaño n × (m+1)
        Complejidad: O(n × m) donde n = ecuaciones, m = variables
        """
        n_ec = self.num_ecuaciones.get()  # O(1)
        n_var = self.num_variables.get()  # O(1)
        matriz = []
        
        try:
            # Recorrer todas las celdas de la matriz - O(n × m)
            for i in range(n_ec):
                fila = []
                for j in range(n_var + 1):  # +1 para término independiente
                    valor = self.matriz_entries[i][j].get()  # O(1)
                    if valor == '':
                        raise ValueError(f"Celda vacía en fila {i+1}, columna {j+1}")
                    fila.append(float(valor))  # O(1)
                matriz.append(fila)
            return np.array(matriz)  # O(n × m)
        except ValueError as e:
            messagebox.showerror("Error", f"Dato inválido: {str(e)}")
            return None
    
    def gauss_jordan(self, matriz):
        """
        PASOS 4-9: Algoritmo principal de eliminación Gauss-Jordan
        Complejidad: O(n² × m) donde n = ecuaciones, m = variables
        En sistemas cuadrados (n ≈ m): O(n³)
        """
        n_ec, n_col = matriz.shape  # O(1)
        n_var = n_col - 1  # O(1)
        
        proceso = ["=== PROCESO DE ELIMINACIÓN GAUSS-JORDAN ===\n"]
        proceso.append(f"Matriz inicial:\n{matriz}\n")
        
        # PASO 4: Copiar la matriz para no modificar la original - O(n × m)
        A = matriz.copy().astype(float)
        pivotes = []
        col_actual = 0
        
        # PASO 9: Loop principal - procesar todas las columnas - O(n) iteraciones
        for fila_actual in range(n_ec):
            if col_actual >= n_var:
                break
                
            # PASO 5: Buscar pivote válido en la columna - O(n)
            proceso.append(f"\n--- Paso {len(proceso)}: Buscando pivote en columna {col_actual + 1} ---")
            
            # Buscar fila con pivote no cero - O(n) en peor caso
            fila_pivote = -1
            for i in range(fila_actual, n_ec):
                if abs(A[i, col_actual]) > 1e-10:  # O(1) por comparación
                    fila_pivote = i
                    break
            
            if fila_pivote == -1:
                proceso.append(f"  No se encontró pivote en columna {col_actual + 1}, pasando a siguiente columna")
                col_actual += 1
                continue
            
            # PASO 6: Intercambiar filas si es necesario - O(m)
            if fila_pivote != fila_actual:
                proceso.append(f"  Intercambiando fila {fila_actual + 1} con fila {fila_pivote + 1}")
                A[[fila_actual, fila_pivote]] = A[[fila_pivote, fila_actual]]  # O(m) - intercambia dos filas
                proceso.append(f"  Matriz después del intercambio:\n{A}")
            
            # PASO 7: Normalizar la fila pivote - O(m)
            pivote = A[fila_actual, col_actual]  # O(1)
            proceso.append(f"  Normalizando fila {fila_actual + 1} (dividiendo por {pivote:.6f})")
            A[fila_actual] = A[fila_actual] / pivote  # O(m) - división elemento por elemento
            proceso.append(f"  Matriz después de normalizar:\n{A}")
            
            pivotes.append((fila_actual, col_actual))  # O(1)
            
            # PASO 8: Eliminar los demás elementos de la columna - O(n × m)
            for i in range(n_ec):  # O(n) iteraciones
                if i != fila_actual:
                    factor = A[i, col_actual]  # O(1)
                    if abs(factor) > 1e-10:
                        proceso.append(f"  Eliminando elemento en fila {i + 1}, columna {col_actual + 1} (factor: {factor:.6f})")
                        # O(m) - operación vectorizada
                        A[i] = A[i] - factor * A[fila_actual]
                        proceso.append(f"  Matriz después de eliminar:\n{A}")
            
            col_actual += 1  # O(1)
        
        # PASO 10: Matriz en forma reducida por filas (RREF)
        proceso.append("\n=== MATRIZ FINAL (FORMA ESCALONADA REDUCIDA) ===")
        proceso.append(f"{A}")
        
        return A, pivotes, proceso
    
    def analizar_solucion(self, matriz_reducida, pivotes):
        """
        PASOS 11-12: Verificar tipo de solución y mostrar resultados
        Complejidad: O(n × m) donde n = ecuaciones, m = variables
        """
        n_ec, n_col = matriz_reducida.shape  # O(1)
        n_var = n_col - 1  # O(1)
        proceso = []
        
        proceso.append("\n=== ANÁLISIS DE LA SOLUCIÓN ===")
        
        # PASO 11: Verificar inconsistencias - O(n × m)
        for i in range(n_ec):  # O(n) iteraciones
            # Verificar si toda la fila es cero excepto el término independiente - O(m)
            if all(abs(matriz_reducida[i, j]) < 1e-10 for j in range(n_var)) and abs(matriz_reducida[i, n_var]) > 1e-10:
                proceso.append(f"¡SISTEMA INCONSISTENTE!")
                proceso.append(f"Fila {i + 1}: 0 = {matriz_reducida[i, n_var]:.6f} → Contradicción")
                return "sin_solucion", proceso, None
        
        # Identificar variables libres - O(n × m)
        columnas_pivote = [col for fila, col in pivotes]  # O(n)
        variables_libres = [j for j in range(n_var) if j not in columnas_pivote]  # O(n × m)
        
        if variables_libres:
            # Sistema con infinitas soluciones
            proceso.append(f"SISTEMA CON INFINITAS SOLUCIONES")
            proceso.append(f"Variables libres: {[f'x{j+1}' for j in variables_libres]}")
            proceso.append(f"Variables básicas: {[f'x{col+1}' for fila, col in pivotes]}")
            
            # PASO 12: Construir solución paramétrica - O(n × m)
            solucion = {}
            for var_libre in variables_libres:  # O(m) en peor caso
                solucion[f'x{var_libre + 1}'] = f't{var_libre + 1}'  # Parámetro libre
            
            # Expresar variables básicas en términos de variables libres - O(n × m)
            for fila, col in pivotes:  # O(n) iteraciones
                expr = f"{matriz_reducida[fila, n_var]:.6f}"  # O(1)
                for var_libre in variables_libres:  # O(m) iteraciones
                    coef = -matriz_reducida[fila, var_libre]  # O(1)
                    if abs(coef) > 1e-10:
                        expr += f" + ({coef:.6f})*t{var_libre + 1}"  # O(1)
                solucion[f'x{col + 1}'] = expr  # O(1)
            
            return "infinitas", proceso, solucion
        else:
            # Sistema con solución única - O(n)
            proceso.append("SISTEMA CON SOLUCIÓN ÚNICA")
            solucion = {}
            for fila, col in pivotes:  # O(n) iteraciones
                solucion[f'x{col + 1}'] = matriz_reducida[fila, n_var]  # O(1)
            return "unica", proceso, solucion
    
    def resolver(self):
        """
        Función principal que orquesta todo el proceso de solución
        Complejidad total: O(n³) para sistemas cuadrados
        """
        # Obtener matriz del usuario - O(n × m)
        matriz = self.obtener_matriz()
        if matriz is None:
            return
        
        self.texto_resultados.delete(1.0, tk.END)  # O(1)
        
        try:
            # PASOS 4-9: Aplicar Gauss-Jordan - O(n² × m)
            matriz_reducida, pivotes, proceso_gj = self.gauss_jordan(matriz)
            
            # PASOS 11-12: Analizar solución - O(n × m)
            tipo_solucion, proceso_analisis, solucion = self.analizar_solucion(matriz_reducida, pivotes)
            
            # Mostrar resultados - O(n × m) para imprimir
            for paso in proceso_gj:  # O(n²) pasos en el proceso
                self.texto_resultados.insert(tk.END, paso + "\n")  # O(1) por inserción
            
            for paso in proceso_analisis:  # O(n) pasos
                self.texto_resultados.insert(tk.END, paso + "\n")  # O(1)
            
            # Mostrar solución específica
            if tipo_solucion == "unica":
                self.texto_resultados.insert(tk.END, "\n=== SOLUCIÓN ÚNICA ===\n")  # O(1)
                for variable, valor in solucion.items():  # O(n) iteraciones
                    self.texto_resultados.insert(tk.END, f"{variable} = {valor:.6f}\n")  # O(1)
            
            elif tipo_solucion == "infinitas":
                self.texto_resultados.insert(tk.END, "\n=== SOLUCIÓN PARAMÉTRICA ===\n")  # O(1)
                for variable, expresion in solucion.items():  # O(n) iteraciones
                    self.texto_resultados.insert(tk.END, f"{variable} = {expresion}\n")  # O(1)
                self.texto_resultados.insert(tk.END, "\nDonde t1, t2, ... son parámetros reales libres.\n")  # O(1)
            
            else:  # sin_solucion
                self.texto_resultados.insert(tk.END, "\nEl sistema no tiene solución.\n")  # O(1)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el cálculo: {str(e)}")  # O(1)
    
    def limpiar(self):
        """
        Limpiar todos los campos de entrada y resultados
        Complejidad: O(n × m) donde n = ecuaciones, m = variables
        """
        # Limpiar entradas de la matriz - O(n × m)
        for fila in self.matriz_entries:  # O(n) iteraciones
            for entry in fila:  # O(m) iteraciones
                entry.delete(0, tk.END)  # O(1)
        
        # Limpiar área de resultados - O(1)
        self.texto_resultados.delete(1.0, tk.END)  # O(1)
    
    def cargar_ejemplo(self):
        """
        Cargar un ejemplo predefinido para prueba
        Complejidad: O(n × m) donde n = ecuaciones, m = variables
        """
        # Configurar tamaño del ejemplo - O(1)
        self.num_ecuaciones.set(2)
        self.num_variables.set(2)
        self.actualizar_matriz()  # O(n × m)
        
        # Valores del ejemplo: 2x + 3y = 8, 4x - y = 2
        valores = [
            ['2', '3', '8'],
            ['4', '-1', '2']
        ]
        
        # Llenar la matriz con valores de ejemplo - O(n × m)
        for i, fila in enumerate(valores):  # O(n) iteraciones
            for j, valor in enumerate(fila):  # O(m) iteraciones
                self.matriz_entries[i][j].delete(0, tk.END)  # O(1)
                self.matriz_entries[i][j].insert(0, valor)  # O(1)

def main():
    """
    Función principal - Inicia la aplicación
    Complejidad: O(1) - inicialización básica
    """
    root = tk.Tk()  # O(1)
    app = GaussJordanSolver(root)  # O(1) - la UI se configura en setup_ui()
    root.mainloop()  # O(∞) - loop infinito de la interfaz

if __name__ == "__main__":
    main()