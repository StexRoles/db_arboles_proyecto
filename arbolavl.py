class NodoAVL:
    def __init__(self, clave, objeto):
        self.clave = clave
        self.objeto = objeto
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def _altura(self, nodo):
        return nodo.altura if nodo else 0

    def _factor_balanceo(self, nodo):
        return self._altura(nodo.izquierda) - self._altura(nodo.derecha)

    def _rotar_derecha(self, y):
        x = y.izquierda
        T2 = x.derecha
        x.derecha = y
        y.izquierda = T2
        y.altura = 1 + max(self._altura(y.izquierda), self._altura(y.derecha))
        x.altura = 1 + max(self._altura(x.izquierda), self._altura(x.derecha))
        return x

    def _rotar_izquierda(self, x):
        y = x.derecha
        T2 = y.izquierda
        y.izquierda = x
        x.derecha = T2
        x.altura = 1 + max(self._altura(x.izquierda), self._altura(x.derecha))
        y.altura = 1 + max(self._altura(y.izquierda), self._altura(y.derecha))
        return y

    def insertar(self, clave, objeto):
        self.raiz = self._insertar(self.raiz, clave, objeto)

    def _insertar(self, nodo, clave, objeto):
        if not nodo:
            return NodoAVL(clave, objeto)

        if clave <= nodo.clave: 
            nodo.izquierda = self._insertar(nodo.izquierda, clave, objeto)
        else:
            nodo.derecha = self._insertar(nodo.derecha, clave, objeto)

        nodo.altura = 1 + max(self._altura(nodo.izquierda), self._altura(nodo.derecha))
        balance = self._factor_balanceo(nodo)

        # Rotaciones
        if balance > 1 and clave < nodo.izquierda.clave:
            return self._rotar_derecha(nodo)
        if balance < -1 and clave > nodo.derecha.clave:
            return self._rotar_izquierda(nodo)
        if balance > 1 and clave > nodo.izquierda.clave:
            nodo.izquierda = self._rotar_izquierda(nodo.izquierda)
            return self._rotar_derecha(nodo)
        if balance < -1 and clave < nodo.derecha.clave:
            nodo.derecha = self._rotar_derecha(nodo.derecha)
            return self._rotar_izquierda(nodo)

        return nodo

    def buscar(self, clave):
        return self._buscar(self.raiz, clave)

    def _buscar(self, nodo, clave):
        if not nodo:
            return None
        if clave == nodo.clave:
            return nodo.objeto
        elif clave < nodo.clave:
            return self._buscar(nodo.izquierda, clave)
        else:
            return self._buscar(nodo.derecha, clave)

    def eliminar(self, clave):
        self.raiz = self._eliminar(self.raiz, clave)

    def _eliminar(self, nodo, clave):
        if not nodo:
            return None

        if clave < nodo.clave:
            nodo.izquierda = self._eliminar(nodo.izquierda, clave)
        elif clave > nodo.clave:
            nodo.derecha = self._eliminar(nodo.derecha, clave)
        else:
            if not nodo.izquierda:
                return nodo.derecha
            elif not nodo.derecha:
                return nodo.izquierda

            temp = self._max_nodo(nodo.izquierda)
            nodo.clave = temp.clave
            nodo.objeto = temp.objeto
            nodo.izquierda = self._eliminar(nodo.izquierda, temp.clave)

        nodo.altura = 1 + max(self._altura(nodo.izquierda), self._altura(nodo.derecha))
        balance = self._factor_balanceo(nodo)

        # Rotaciones de rebalanceo
        if balance > 1 and self._factor_balanceo(nodo.izquierda) >= 0:
            return self._rotar_derecha(nodo)
        if balance > 1 and self._factor_balanceo(nodo.izquierda) < 0:
            nodo.izquierda = self._rotar_izquierda(nodo.izquierda)
            return self._rotar_derecha(nodo)
        if balance < -1 and self._factor_balanceo(nodo.derecha) <= 0:
            return self._rotar_izquierda(nodo)
        if balance < -1 and self._factor_balanceo(nodo.derecha) > 0:
            nodo.derecha = self._rotar_derecha(nodo.derecha)
            return self._rotar_izquierda(nodo)

        return nodo

    def _min_nodo(self, nodo):
        actual = nodo
        while actual.izquierda:
            actual = actual.izquierda
        return actual
    
    def _max_nodo(self, nodo):
        actual = nodo
        while actual.derecha:
            actual = actual.derecha
        return actual

    def inorden(self):
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(self, nodo, resultado):
        if nodo:
            self._inorden(nodo.izquierda, resultado)
            resultado.append(nodo.objeto)
            self._inorden(nodo.derecha, resultado)

    # En arbol_avl.py
    def imprimir(self, nodo=None, nivel=0, prefijo="Raíz: "):
        if nodo is None:
            nodo = self.raiz
        if nodo is not None:
            print(" " * (4 * nivel) + prefijo + f"[{nodo.clave}]")
            if nodo.izquierda:
                self.imprimir(nodo.izquierda, nivel + 1, "Izq:  ")
            if nodo.derecha:
                self.imprimir(nodo.derecha, nivel + 1, "Der:  ")

