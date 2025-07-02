# Gestor de Base de Datos con Árbol AVL

Aplicación de escritorio en Python para gestionar bases de datos simples usando archivos JSON y árboles AVL para búsquedas eficientes. Incluye interfaz gráfica con Tkinter.

## Características
- Soporte para múltiples archivos de base de datos (cada uno gestionado por un árbol AVL).
- Inserción, búsqueda, actualización, eliminación y listado de registros.
- Creación y eliminación dinámica de archivos de base de datos.
- Persistencia automática en archivos JSON.
- Interfaz gráfica intuitiva.

## Estructura de los datos
Cada registro/producto tiene:
- `id` (int): Identificador único
- `nombre` (str): Nombre
- `precio` (float/int): Precio
- `descuento` (float/int): Porcentaje de descuento

## Comandos principales en la interfaz
- `insertar archivo productos`  
  Crea un nuevo archivo (ej: `1_productos.json`).
- `insertar {"id": 1, "nombre": "Monitor", "precio": 499, "descuento": 15} en 1`  
  Inserta un registro en el archivo con id 1.
- `buscar 1 en 1`  
  Busca el registro con id 1 en el archivo con id 1.
- `actualizar {"id": 1, "nombre": "Monitor HD", "precio": 599, "descuento": 10} en 1`  
  Actualiza el registro con id 1 en el archivo con id 1.
- `eliminar 1 en 1`  
  Elimina el registro con id 1 del archivo con id 1.
- `listar 1`  
  Lista todos los registros del archivo con id 1.
- `eliminar archivo 1`  
  Elimina el archivo con id 1.

## Archivos principales
- `arbolavl.py`: Árbol AVL.
- `gestor.py`: Lógica de gestión de archivos y registros.
- `gestor_multi.py`: Gestión multiarchivo.
- `persistencia.py`: Manejo de archivos JSON.
- `interfaz.py`: Interfaz gráfica.

---
