from arbolavl import ArbolAVL
import persistencia

class GestorBD:
    def __init__(self, archivo_datos='datos.json'):
        """
        Inicializa el gestor de base de datos, cargando los datos desde el archivo especificado
        y creando una instancia del árbol AVL.
        """
        
        self.archivo = archivo_datos
        self.arbol = ArbolAVL()
        for obj in persistencia.cargar_json(archivo_datos):
            self.arbol.insertar(obj["id"], obj)

    def insertar(self, obj_json):
        """
        Inserta un nuevo objeto en el árbol AVL y en el archivo JSON.
        Lanza un error si el id ya existe.
        """
        clave = obj_json.get('id')
        if self.arbol.buscar(clave):
            raise ValueError(f"Ya existe un objeto con id={clave}")
        self.arbol.insertar(clave, obj_json)
        persistencia.agregar_json(self.archivo, obj_json)
        print("\nÁrbol AVL actualizado:")
        self.arbol.imprimir()

    def buscar(self, clave):
        """
        Busca y retorna el objeto con la clave dada en el árbol AVL.
        Si no existe, retorna None.
        """
        return self.arbol.buscar(clave)

    def eliminar(self, clave):
        """
        Elimina el objeto con la clave dada del árbol AVL y del archivo JSON.
        Lanza un error si el id no existe.
        """
        if not self.arbol.buscar(clave):
            raise ValueError("ID no encontrado")
        self.arbol.eliminar(clave)  
        persistencia.eliminar_json(self.archivo, clave)
        print("\nÁrbol AVL actualizado:")
        self.arbol.imprimir()

    def actualizar(self, obj_json):
        """
        Actualiza los datos de un objeto existente con la clave dada,
        eliminando primero el nodo antiguo del árbol para evitar duplicados.
        """
        clave = obj_json.get('id')
        if not self.arbol.buscar(clave):
            raise ValueError("ID no encontrado")
        self.arbol.eliminar(clave)
        self.arbol.insertar(clave, obj_json)
        persistencia.actualizar_json(self.archivo, clave, obj_json)
        print(f"\nProducto con id={clave} actualizado.")
        self.arbol.imprimir()

    def listar(self):
        """
        Retorna una lista de todos los objetos almacenados en el árbol AVL en orden.
        """
        return self.arbol.inorden()

class GestorMultiBD:
    """
    Permite gestionar múltiples archivos y sus árboles AVL asociados.
    Además, mantiene un árbol AVL de los ids de los archivos creados.
    """
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
        Además, inserta el id del archivo en el árbol AVL de archivos y lo imprime.
        """
        import os
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
            print("Árbol AVL archivos actualizado:")
            self.arbol_archivos.imprimir()
        except Exception:
            pass
