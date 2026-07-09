"""Módulo encargado de guardar y recuperar el historial de operaciones.

El historial se guarda en un archivo "historial.json" ubicado en la
raíz del proyecto, para que las operaciones no se pierdan aunque la
aplicación se cierre.
"""

import json
import os
from datetime import datetime

# Ruta absoluta al archivo historial.json, en la raíz del proyecto
# (un nivel arriba de la carpeta "logic").
ARCHIVO_HISTORIAL = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "historial.json",
)


def cargar_historial():
    """Carga el historial almacenado en el archivo JSON.

    Si el archivo no existe o está dañado, devuelve una lista vacía
    en lugar de detener la aplicación.
    """
    if not os.path.exists(ARCHIVO_HISTORIAL):
        return []

    try:
        with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, OSError):
        return []


def guardar_operacion(expresion, resultado):
    """Agrega una nueva operación al historial y la guarda en disco."""
    historial = cargar_historial()

    historial.append(
        {
            "expresion": expresion,
            "resultado": resultado,
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }
    )

    try:
        with open(ARCHIVO_HISTORIAL, "w", encoding="utf-8") as archivo:
            json.dump(historial, archivo, ensure_ascii=False, indent=2)
    except OSError:
        # Si por alguna razón no se puede escribir en disco (permisos,
        # espacio, etc.) la app sigue funcionando, solo no se guarda.
        pass


def obtener_historial():
    """Devuelve la lista completa del historial, la más reciente al final."""
    return cargar_historial()


def borrar_historial():
    """Elimina todo el historial guardado."""
    try:
        with open(ARCHIVO_HISTORIAL, "w", encoding="utf-8") as archivo:
            json.dump([], archivo)
    except OSError:
        pass
