import tkinter as tk
from tkinter import messagebox, simpledialog


class Definicion:
    """Nodo de la lista enlazada"""
    def __init__(self, num: int):
        self.num: int = num
        self.sig: 'Definicion' | None = None


class EnlaceNodos:
    """Manejo de la lista enlazada"""
    def __init__(self):
        self.p: Definicion | None = None
        self.cab: Definicion | None = None

    def captura(self):
        """Crea automáticamente una lista de 6 nodos (0 a 5)"""
        self.p = None
        self.cab = None
        for i in range(6):
            q = Definicion(i)
            if self.p is None:
                self.p = q
                self.cab = q
            else:
                self.cab.sig = q
                self.cab = q

    def agregar(self, valor: int):
        """Agrega un nodo al final"""
        nuevo = Definicion(valor)
        if self.p is None:
            self.p = nuevo
            self.cab = nuevo
        else:
            self.cab.sig = nuevo
            self.cab = nuevo

    def mostrar(self) -> str:
        """Devuelve una representación de la lista"""
        actual = self.p
        nodos = []
        while actual is not None:
            nodos.append(str(actual.num))
            actual = actual.sig
        return " → ".join(nodos) if nodos else "(lista vacía)"

    def retiro(self, valor: int):
        """Elimina un nodo con un valor específico"""
        actual = self.p
        anterior = None
        while actual is not None:
            if actual.num == valor:
                if anterior is None:  # eliminar cabeza
                    self.p = actual.sig
                else:
                    anterior.sig = actual.sig
                return True
            anterior = actual
            actual = actual.sig
        return False


# ------------------ Interfaz gráfica ------------------

class ListaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista Dinámica Enlazada")
        self.root.geometry("400x350")
        self.root.configure(bg="#f0f0f0")

        self.lista = EnlaceNodos()

        # Etiqueta
        tk.Label(root, text="Lista dinámica enlazada", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)

        # Botones
        btn_frame = tk.Frame(root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Capturar (0-5)", width=15, command=self.captura).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Agregar nodo", width=15, command=self.agregar).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Retirar nodo", width=15, command=self.retirar).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Mostrar lista", width=15, command=self.mostrar).grid(row=1, column=1, padx=5, pady=5)

        # Área de salida
        tk.Label(root, text="Lista actual:", bg="#f0f0f0").pack()
        self.text_area = tk.Text(root, height=8, width=40, state="disabled", bg="white", font=("Consolas", 11))
        self.text_area.pack(pady=5)

    def mostrar_mensaje(self, msg: str):
        messagebox.showinfo("Resultado", msg)

    def actualizar_texto(self):
        self.text_area.config(state="normal")
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, self.lista.mostrar())
        self.text_area.config(state="disabled")

    def captura(self):
        self.lista.captura()
        self.actualizar_texto()
        self.mostrar_mensaje("Se han creado los nodos del 0 al 5")

    def agregar(self):
        val = tk.simpledialog.askinteger("Agregar nodo", "Digite el número del nuevo nodo:")
        if val is not None:
            self.lista.agregar(val)
            self.actualizar_texto()
            self.mostrar_mensaje(f"Nodo {val} agregado")

    def retirar(self):
        val = tk.simpledialog.askinteger("Retirar nodo", "Digite el número del nodo a eliminar:")
        if val is not None:
            ok = self.lista.retiro(val)
            if ok:
                self.actualizar_texto()
                self.mostrar_mensaje(f"Nodo {val} eliminado")
            else:
                self.mostrar_mensaje(f"No se encontró el nodo {val}")

    def mostrar(self):
        self.actualizar_texto()
        self.mostrar_mensaje("Lista mostrada en el panel inferior")


# ------------------ Ejecución ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ListaGUI(root)
    root.mainloop()
