"""Pantalla principal de la calculadora.

Aquí vive toda la lógica de interacción con el usuario: escribir la
expresión, calcular el resultado, alternar entre modo básico y modo
científico (con animación), y mostrar el historial de operaciones.

La lógica matemática pura y el manejo del historial NO están aquí:
viven en "logic/operaciones.py" y "logic/historial.py" para mantener
la interfaz separada de la lógica de negocio.
"""

from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem
from kivymd.uix.dialog import MDDialog

from logic.operaciones import evaluar
from logic.historial import guardar_operacion, obtener_historial

# Altura que ocupa el panel científico cuando está desplegado.
# IMPORTANTE: Animation() necesita un número en píxeles, no un texto
# como "230dp" (eso solo funciona dentro de archivos .kv). Por eso se
# usa dp(...) para convertir el valor antes de animarlo.
# El valor corresponde a 3 filas de 40dp + espaciados de 4dp entre
# filas (ver row_default_height y spacing en kv/calculadora.kv), más
# un pequeño margen de seguridad.
ALTURA_PANEL_CIENTIFICO = dp(140)


class CalculadoraScreen(Screen):
    """Pantalla única de la aplicación."""

    modo_cientifico_activo = False
    dialogo_historial = None

    # ------------------------------------------------------------------
    # Entrada de datos
    # ------------------------------------------------------------------
    def agregar(self, valor):
        """Agrega un carácter, número o función a la pantalla."""
        pantalla = self.ids.pantalla
        if pantalla.text == "Error":
            pantalla.text = ""
        pantalla.text += valor

    def borrar_ultimo(self):
        """Elimina únicamente el último carácter ingresado."""
        pantalla = self.ids.pantalla
        pantalla.text = pantalla.text[:-1]

    def limpiar(self):
        """Limpia completamente la pantalla."""
        self.ids.pantalla.text = ""

    def cambiar_signo(self):
        """Invierte el signo del número/expresión actual (±)."""
        pantalla = self.ids.pantalla
        texto = pantalla.text
        if not texto:
            return
        if texto.startswith("-"):
            pantalla.text = texto[1:]
        else:
            pantalla.text = "-" + texto

    # ------------------------------------------------------------------
    # Cálculo
    # ------------------------------------------------------------------
    def calcular(self):
        """Evalúa la expresión actual, muestra el resultado y lo guarda."""
        expresion = self.ids.pantalla.text
        if not expresion:
            return

        resultado = evaluar(expresion)
        self.ids.pantalla.text = resultado

        # Solo se guardan en el historial las operaciones válidas.
        if resultado != "Error":
            guardar_operacion(expresion, resultado)

    # ------------------------------------------------------------------
    # Modo científico
    # ------------------------------------------------------------------
    def alternar_modo_cientifico(self):
        """Muestra u oculta el panel científico con una animación suave.

        Los botones básicos (números y +, -, *, /) nunca se ocultan;
        solo se agrega o se quita el panel de funciones científicas.
        """
        panel = self.ids.panel_cientifico
        boton = self.ids.btn_modo

        self.modo_cientifico_activo = not self.modo_cientifico_activo

        if self.modo_cientifico_activo:
            Animation(
                height=ALTURA_PANEL_CIENTIFICO, opacity=1, duration=0.25, t="out_quad"
            ).start(panel)
            boton.icon = "calculator"
        else:
            Animation(height=0, opacity=0, duration=0.25, t="out_quad").start(panel)
            boton.icon = "calculator-variant"

    # ------------------------------------------------------------------
    # Historial
    # ------------------------------------------------------------------
    def mostrar_historial(self):
        """Abre un cuadro de diálogo con el historial completo de operaciones."""
        historial = obtener_historial()

        contenedor = MDList()

        if not historial:
            contenedor.add_widget(
                OneLineListItem(text="Aún no hay operaciones registradas")
            )
        else:
            # Se muestra primero lo más reciente.
            for operacion in reversed(historial):
                texto_superior = f"{operacion['expresion']} = {operacion['resultado']}"
                texto_inferior = operacion["fecha"]
                contenedor.add_widget(
                    TwoLineListItem(text=texto_superior, secondary_text=texto_inferior)
                )

        scroll = ScrollView(size_hint=(1, None), size=("300dp", "400dp"))
        scroll.add_widget(contenedor)

        self.dialogo_historial = MDDialog(
            title="Historial de operaciones",
            type="custom",
            content_cls=scroll,
        )
        self.dialogo_historial.open()
