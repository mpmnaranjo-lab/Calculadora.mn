"""Punto de entrada de la aplicación Calculadora Científica.

Este archivo es intencionalmente pequeño: solo configura el tema y
arranca la aplicación. Toda la lógica vive en los módulos
"screens/" y "logic/".
"""

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from screens.calculadora_screen import CalculadoraScreen

Builder.load_file("kv/calculadora.kv")


class CalculadoraApp(MDApp):
    """Aplicación principal de la calculadora científica."""

    def build(self):
        self.title = "Calculadora Científica"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"

        gestor = MDScreenManager()
        gestor.add_widget(CalculadoraScreen(name="calculadora"))
        return gestor


if __name__ == "__main__":
    CalculadoraApp().run()
