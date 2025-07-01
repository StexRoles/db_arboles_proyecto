import tkinter as tk
from tkinter import ttk, messagebox
import json
from gestor import GestorBD

class InterfazBD:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestor de BD con Árbol AVL")
        self.master.geometry("600x500")

        self.gestor = GestorBD()

        self.entrada = tk.Entry(master, font=("Consolas", 12))
        self.entrada.pack(fill="x", padx=10, pady=5)

        self.boton = tk.Button(master, text="Ejecutar comando", command=self.ejecutar_comando)
        self.boton.pack(pady=5)

        # Área de resultados
        self.resultado = tk.Text(master, height=10, wrap="word")
        self.resultado.pack(fill="both", expand=True, padx=10, pady=5)

        # Tabla para mostrar múltiples registros
        self.tabla = ttk.Treeview(master)
        self.tabla.pack(fill="both", expand=True, padx=10, pady=5)

    def ejecutar_comando(self):
        comando = self.entrada.get().strip()
        self.resultado.delete("1.0", tk.END)
        self.tabla.delete(*self.tabla.get_children())

        if comando.startswith("buscar "):
            clave = int(comando.split(" ")[1])
            resultado = self.gestor.buscar(clave)
            if resultado:
                self.mostrar_json(resultado)
            else:
                self.resultado.insert(tk.END, "No se encontró el elemento.")
        elif comando.startswith("eliminar "):
            clave = int(comando.split(" ")[1])
            try:
                self.gestor.eliminar(clave)
                self.resultado.insert(tk.END, f"Elemento con id={clave} eliminado.")
            except Exception as e:
                self.resultado.insert(tk.END, str(e))
        elif comando == "listar":
            registros = self.gestor.listar()
            if registros:
                self.mostrar_tabla(registros)
            else:
                self.resultado.insert(tk.END, "No hay datos.")
        elif comando.startswith("insertar "):
            try:
                json_texto = comando[len("insertar "):].strip()
                nuevo_obj = json.loads(json_texto)
                self.gestor.insertar(nuevo_obj)
                self.resultado.insert(tk.END, f"Objeto insertado con id={nuevo_obj.get('id')}")
            except json.JSONDecodeError:
                self.resultado.insert(tk.END, "Error: JSON mal formado.")
            except Exception as e:
                self.resultado.insert(tk.END, str(e))

        else:
            self.resultado.insert(tk.END, "Comando no reconocido.")

    def mostrar_json(self, obj):
        self.resultado.insert(tk.END, json.dumps(obj, indent=2, ensure_ascii=False))

    def mostrar_tabla(self, registros):
        # Limpiar columnas existentes
        self.tabla.delete(*self.tabla.get_children())
        self.tabla['columns'] = ('id', 'nombre', 'precio', 'descuento')
        self.tabla.heading('#0', text='')
        self.tabla.column('#0', width=0, stretch=tk.NO)
        self.tabla.heading('id', text='ID')
        self.tabla.heading('nombre', text='Nombre')
        self.tabla.heading('precio', text='Precio')
        self.tabla.heading('descuento', text='Descuento')
        self.tabla.column('id', width=60)
        self.tabla.column('nombre', width=180)
        self.tabla.column('precio', width=100)
        self.tabla.column('descuento', width=100)
        for obj in registros:
            self.tabla.insert('', tk.END, values=(obj.get('id'), obj.get('nombre'), obj.get('precio'), obj.get('descuento')))

