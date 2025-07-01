# Gestor de Base de Datos con Árbol AVL

Este proyecto es una aplicación de escritorio en Python que permite gestionar una base de datos simple de productos utilizando un árbol AVL para garantizar búsquedas, inserciones y eliminaciones eficientes.

## Características
- Inserción, búsqueda, eliminación y listado de productos.
- Estructura de datos principal: Árbol AVL auto-balanceado.
- Interfaz gráfica con Tkinter.
- Persistencia de datos en archivo JSON.

## Estructura de los datos
Cada producto tiene los siguientes campos:
- `id` (int): Identificador único
- `nombre` (str): Nombre del producto
- `precio` (float/int): Precio del producto
- `descuento` (float/int): Porcentaje de descuento

## Requisitos
- Python 3.x
- Tkinter (incluido en la mayoría de instalaciones de Python)

## Uso
1. Ejecuta la aplicación principal (por ejemplo, desde un archivo `main.py` o directamente la interfaz):
   ```bash
   python interfaz.py
   ```
2. Utiliza los siguientes comandos en la interfaz:
   - `insertar {"id": 1, "nombre": "Monitor", "precio": 499, "descuento": 15}`
   - `buscar 1`
   - `eliminar 1`
   - `listar`

## Archivos principales
- `arbolavl.py`: Implementación del árbol AVL.
- `gestor.py`: Lógica de gestión de la base de datos.
- `persistencia.py`: Funciones para manejo de archivos JSON.
- `interfaz.py`: Interfaz gráfica de usuario.
- `datos.json`: Archivo de datos persistentes.

---

Proyecto realizado para fines educativos y de práctica de estructuras de datos avanzadas en Python.
