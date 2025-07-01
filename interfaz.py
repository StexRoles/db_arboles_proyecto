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

        elif comando.startswith("actualizar "):
            try:
                partes = comando.split(" ", 2)
                if len(partes) < 3:
                    self.resultado.insert(tk.END, "Error: Debes indicar el id y los nuevos datos en formato JSON.")
                else:
                    clave = int(partes[1])
                    nuevos_datos = json.loads(partes[2])
                    self.gestor.actualizar(clave, nuevos_datos)
                    self.resultado.insert(tk.END, f"Elemento con id={clave} actualizado.")
            except json.JSONDecodeError:
                self.resultado.insert(tk.END, "Error: JSON mal formado.")
            except Exception as e:
                self.resultado.insert(tk.END, str(e))

        else:
            self.resultado.insert(tk.END, "Comando no reconocido.")

    def mostrar_json(self, obj):
        self.resultado.insert(tk.END, json.dumps(obj, indent=2, ensure_ascii=False))

    def mostrar_tabla(self, registros):
        # Limpiar filas existentes
        self.tabla.delete(*self.tabla.get_children())
        # Detectar todas las claves únicas presentes en los registros
        columnas = set()
        for obj in registros:
            columnas.update(obj.keys())
        columnas = list(columnas)
        # Opcional: ordenar columnas para que 'id' vaya primero si existe
        if 'id' in columnas:
            columnas.remove('id')
            columnas = ['id'] + columnas
        self.tabla['columns'] = columnas
        # Configurar encabezados y columnas
        self.tabla.heading('#0', text='')
        self.tabla.column('#0', width=0, stretch=tk.NO)
        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=120)
        # Insertar los datos
        for obj in registros:
            values = [obj.get(col, '') for col in columnas]
            self.tabla.insert('', tk.END, values=values)

