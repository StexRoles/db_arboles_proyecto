from gestor import GestorBD
from arbolavl import ArbolAVL
import os

class GestorMultiBD:
    def __init__(self):
        self.gestores = {}
        self.arbol_archivos = ArbolAVL()  # AVL para ids de archivos

    def obtener_gestor(self, archivo):
        if archivo not in self.gestores:
            self.gestores[archivo] = GestorBD(archivo)
        return self.gestores[archivo]

    def crear_archivo(self, archivo):
        """
        Crea un nuevo archivo JSON vacío y su árbol AVL asociado.
        Si el archivo ya existe, no lo sobrescribe.
        Además, inserta el id del archivo en el árbol AVL de archivos.
        """
        if not os.path.exists(archivo):
            with open(archivo, 'w', encoding='utf-8') as f:
                f.write('[]')
        self.gestores[archivo] = GestorBD(archivo)
        # Extraer id del nombre del archivo (formato: id_nombre.json o id.json)
        nombre = os.path.basename(archivo)
        nombre_sin_ext = nombre[:-5]  # quitar .json
        partes = nombre_sin_ext.split('_', 1)
        try:
            archivo_id = int(partes[0])
            self.arbol_archivos.insertar(archivo_id, archivo)
        except Exception:
            pass
