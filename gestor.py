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
        self._cargar_datos()

    def _cargar_datos(self):
        """
        Carga los registros desde el archivo JSON y los inserta en el árbol AVL.
        """
        registros = persistencia.cargar_json(self.archivo)
        for obj in registros:
            self.arbol.insertar(obj['id'], obj)

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

    def actualizar(self, clave, nuevos_datos):
        """
        Actualiza los datos de un objeto existente con la clave dada,
        eliminando primero el nodo antiguo del árbol para evitar duplicados.
        """
        objeto_actual = self.arbol.buscar(clave)
        if not objeto_actual:
            raise ValueError("ID no encontrado")

        objeto_actual.update(nuevos_datos)

        self.arbol.eliminar(clave) 
        self.arbol.insertar(clave, objeto_actual) 
        persistencia.actualizar_json(self.archivo, clave, objeto_actual)

    def listar(self):
        """
        Retorna una lista de todos los objetos almacenados en el árbol AVL en orden.
        """
        return self.arbol.inorden()
