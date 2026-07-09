"""Módulo encargado de interpretar y resolver expresiones matemáticas.

Toda la lógica de cálculo vive aquí, separada por completo de la
interfaz gráfica, para que se pueda modificar o probar de forma
independiente.
"""

import re
from math import sin, cos, tan, log, log10, sqrt, factorial, pi, e

# Espacio de nombres seguro: solo se permiten las funciones y constantes
# matemáticas necesarias. Se bloquea el acceso a "__builtins__" para
# evitar que la expresión ingresada por el usuario pueda ejecutar
# código peligroso a través de eval().
_CONTEXTO_SEGURO = {
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "log": log,
    "log10": log10,
    "sqrt": sqrt,
    "factorial": factorial,
    "abs": abs,
    "pi": pi,
    "e": e,
    "__builtins__": {},
}

# Detecta patrones como "5!" o "12!" para convertirlos en "factorial(5)".
_PATRON_FACTORIAL = re.compile(r"(\d+)\s*!")


def _preparar_expresion(expresion):
    """Normaliza la expresión antes de evaluarla.

    - Convierte "n!" en "factorial(n)".
    - Reemplaza el símbolo de porcentaje "%" por una división entre 100.
    """
    expresion = _PATRON_FACTORIAL.sub(r"factorial(\1)", expresion)
    expresion = expresion.replace("%", "/100")
    return expresion


def evaluar(expresion):
    """Evalúa una expresión matemática de forma segura.

    Devuelve el resultado como texto, o la cadena "Error" si la
    expresión está mal formada o no se puede calcular (por ejemplo,
    una división entre cero o paréntesis sin cerrar).
    """
    if not expresion:
        return "Error"

    try:
        expresion_preparada = _preparar_expresion(expresion)
        resultado = eval(expresion_preparada, _CONTEXTO_SEGURO)
        return str(resultado)
    except ZeroDivisionError:
        return "Error"
    except Exception:
        return "Error"
