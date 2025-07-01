import tkinter as tk
from tkinter import ttk, messagebox
import json
from gestor_multi import GestorMultiBD
from gestor import GestorBD
import os

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

        self.multi_gestor = GestorMultiBD()

        # Carpeta donde se almacenan los archivos JSON
        self.carpetajson = "json_data"
        if not os.path.exists(self.carpetajson):
            os.makedirs(self.carpetajson)

    def ejecutar_comando(self):
        comando = self.entrada.get().strip()
        self.resultado.delete("1.0", tk.END)
        self.tabla.delete(*self.tabla.get_children())

        if comando.startswith("insertar archivo "):
            nombre_archivo = comando[len("insertar archivo "):].strip()
            # Buscar el siguiente id incremental
            archivos = [f for f in os.listdir(self.carpetajson) if f.endswith('.json')]
            ids = []
            for f in archivos:
                try:
                    with open(os.path.join(self.carpetajson, f), 'r', encoding='utf-8') as file:
                        data = file.read()
                    nombre_sin_ext = f[:-5]  # quitar .json
                    partes = nombre_sin_ext.split('_', 1)
                    if partes[0].isdigit():
                        ids.append(int(partes[0]))
                except Exception:
                    continue
            nuevo_id = max(ids) + 1 if ids else 1
            nombre_final = f"{nuevo_id}_{nombre_archivo}.json"
            ruta_archivo = os.path.join(self.carpetajson, nombre_final)
            self.multi_gestor.crear_archivo(ruta_archivo)
            self.resultado.insert(tk.END, f"Archivo {nombre_final} creado y listo para usarse.")
            # Mostrar árbol AVL de archivos en consola
            self.imprimir_arbol_archivos()

        elif comando.startswith("insertar "):
            try:
                if " en " not in comando:
                    raise ValueError("Falta el archivo destino con 'en'")
                partes = comando[len("insertar "):].split(" en ")
                json_texto = partes[0].strip()
                archivo_id = partes[1].strip()
                # Solo aceptar ids numéricos
                if not archivo_id.isdigit():
                    raise ValueError("Debes indicar el id numérico del archivo, no el nombre. Ejemplo: insertar {...} en 1")
                archivos = [f for f in os.listdir(self.carpetajson) if f.endswith('.json')]
                archivo = None
                for f in archivos:
                    nombre_sin_ext = f[:-5]
                    partes_nombre = nombre_sin_ext.split('_', 1)
                    if partes_nombre[0] == archivo_id:
                        archivo = os.path.join(self.carpetajson, f)
                        break
                if not archivo or not os.path.exists(archivo):
                    raise FileNotFoundError(f"No se encontró un archivo con id {archivo_id}.")
                obj = json.loads(json_texto)
                gestor = self.multi_gestor.obtener_gestor(archivo)
                gestor.insertar(obj)
                self.resultado.insert(tk.END, f"Insertado en {archivo}")
            except Exception as e:
                self.resultado.insert(tk.END, f"Error: {str(e)}")

        elif comando.startswith("buscar "):
            try:
                partes = comando[len("buscar "):].split(" en ")
                clave = int(partes[0])
                archivo_id = partes[1].strip()
                archivo = os.path.join(self.carpetajson, f"{archivo_id}.json")
                gestor = self.multi_gestor.obtener_gestor(archivo)
                obj = gestor.buscar(clave)
                if obj:
                    self.mostrar_json(obj)
                else:
                    self.resultado.insert(tk.END, "No encontrado.")
            except Exception as e:
                self.resultado.insert(tk.END, f"Error: {str(e)}")

        elif comando.startswith("listar archivo"):
            # Listar archivos en la carpeta json_data
            archivos = [f for f in os.listdir(self.carpetajson) if f.endswith('.json')]
            if archivos:
                self.resultado.insert(tk.END, "Archivos en json_data:\n" + "\n".join(archivos))
            else:
                self.resultado.insert(tk.END, "No hay archivos en json_data.")

        elif comando.startswith("listar "):
            archivo_id = comando[len("listar "):].strip()
            archivo = os.path.join(self.carpetajson, f"{archivo_id}.json")
            gestor = self.multi_gestor.obtener_gestor(archivo)
            registros = gestor.listar()
            if registros:
                self.mostrar_tabla(registros)
            else:
                self.resultado.insert(tk.END, f"{archivo} está vacío.")

        elif comando.startswith("eliminar "):
            try:
                partes = comando[len("eliminar "):].split(" en ")
                clave = int(partes[0])
                archivo_id = partes[1].strip()
                archivo = os.path.join(self.carpetajson, f"{archivo_id}.json")
                gestor = self.multi_gestor.obtener_gestor(archivo)
                gestor.eliminar(clave)
                self.resultado.insert(tk.END, f"Elemento con id={clave} eliminado de {archivo}.")
            except Exception as e:
                self.resultado.insert(tk.END, f"Error: {str(e)}")

        elif comando.startswith("actualizar "):
            try:
                if " en " not in comando:
                    raise ValueError("Falta el archivo destino con 'en'")
                partes = comando[len("actualizar "):].split(" en ")
                json_texto = partes[0].strip()
                archivo_id = partes[1].strip()
                archivo = os.path.join(self.carpetajson, f"{archivo_id}.json")
                obj = json.loads(json_texto)
                gestor = self.multi_gestor.obtener_gestor(archivo)
                gestor.actualizar(obj)
                self.resultado.insert(tk.END, f"Elemento con id={obj.get('id')} actualizado en {archivo}.")
                registros = gestor.listar()
                if registros:
                    self.mostrar_tabla(registros)
                else:
                    self.resultado.insert(tk.END, f"{archivo} está vacío.")
            except Exception as e:
                self.resultado.insert(tk.END, f"Error: {str(e)}")

        elif comando.startswith("eliminar archivo "):
            id_a_eliminar = comando[len("eliminar archivo "):].strip()
            archivos = [f for f in os.listdir(self.carpetajson) if f.endswith('.json')]
            archivo_a_eliminar = None
            for f in archivos:
                nombre_sin_ext = f[:-5]
                partes = nombre_sin_ext.split('_', 1)
                if partes[0] == id_a_eliminar:
                    archivo_a_eliminar = os.path.join(self.carpetajson, f)
                    break
            if archivo_a_eliminar and os.path.exists(archivo_a_eliminar):
                # Eliminar del sistema de archivos
                os.remove(archivo_a_eliminar)
                # Eliminar del árbol AVL de archivos
                if id_a_eliminar.isdigit():
                    archivo_id = int(id_a_eliminar)
                    self.multi_gestor.arbol_archivos.eliminar(archivo_id)
                self.resultado.insert(tk.END, f"Archivo {archivo_a_eliminar} eliminado.")
                # Mostrar árbol AVL de archivos en consola
                self.imprimir_arbol_archivos()
            else:
                self.resultado.insert(tk.END, f"Archivo con id {id_a_eliminar} no encontrado.")

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

    def imprimir_arbol_archivos(self):
        """
        Imprime en consola el árbol AVL de ids de archivos gestionados.
        """
        print("Árbol AVL archivos actualizado:")
        self.multi_gestor.arbol_archivos.imprimir()
