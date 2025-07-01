import json
import os

def cargar_json(ruta):
    if not os.path.exists(ruta):
        return []
    with open(ruta, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def guardar_todo_json(ruta, lista_objetos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(lista_objetos, f, indent=2, ensure_ascii=False)

def agregar_json(ruta, nuevo_objeto):
    registros = cargar_json(ruta)
    registros.append(nuevo_objeto)
    guardar_todo_json(ruta, registros)

def eliminar_json(ruta, clave):
    registros = cargar_json(ruta)
    nueva_lista = [obj for obj in registros if obj.get("id") != clave]
    guardar_todo_json(ruta, nueva_lista)

def actualizar_json(ruta, clave, objeto_actualizado):
    registros = cargar_json(ruta)
    for i, obj in enumerate(registros):
        if obj.get("id") == clave:
            registros[i] = objeto_actualizado
            break
    guardar_todo_json(ruta, registros)
