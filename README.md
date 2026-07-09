# Calculadora Científica (KivyMD)

Calculadora de escritorio y Android construida con **Kivy** + **KivyMD**,
con modo básico y modo científico, historial persistente en JSON y un
diseño oscuro moderno.

## Características

- **Modo básico**: suma, resta, multiplicación, división, punto decimal,
  igual, limpiar y borrar un carácter.
- **Modo científico**: se activa con el ícono 🧮 en la barra superior y
  despliega, con una animación, funciones como `sin`, `cos`, `tan`,
  `log`, `ln`, `√`, `x²`, `xʸ`, `π`, `e`, `n!`, `|x|`, `±` y paréntesis,
  sin ocultar el teclado básico.
- **Historial**: cada operación válida se guarda automáticamente con su
  expresión, resultado y fecha/hora en `historial.json`. Se consulta
  desde el ícono de historial en la barra superior.
- **Manejo de errores**: expresiones inválidas o divisiones entre cero
  muestran `Error` en pantalla en vez de cerrar la aplicación.

## Estructura del proyecto

```
calculadora/
├── main.py                    # Punto de entrada de la app
├── historial.json             # Historial guardado (se crea/actualiza solo)
├── requirements.txt
├── README.md
├── screens/
│   └── calculadora_screen.py  # Lógica de interacción (UI <-> lógica)
├── kv/
│   └── calculadora.kv         # Diseño visual (colores, botones, layout)
└── logic/
    ├── operaciones.py         # Evaluación segura de expresiones
    └── historial.py           # Guardado/lectura del historial en JSON
```

Esta separación permite modificar el diseño visual (`kv/`), la lógica
matemática (`logic/operaciones.py`) o el historial (`logic/historial.py`)
de forma independiente, sin afectar el resto del proyecto.

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

## Empaquetado como APK (Android)

El proyecto está preparado para compilarse con **Buildozer**:

```bash
pip install buildozer
buildozer init
buildozer -v android debug
```

## Colores del diseño

- Fondo principal: negro.
- Botones numéricos: gris (plomo).
- Botones de operación (+, −, ×, ÷, =): tomate.
- Botones científicos: gris oscuro.
- Pantalla de resultados: tarjeta con bordes redondeados y letras grandes.
