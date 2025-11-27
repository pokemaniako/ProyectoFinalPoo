import sys

# construir ruta src sin usar os ni pathlib
# __file__ ejemplo: c:\...\ProyectoFinalPoo\src\Codigo\main.py
file_path = __file__
# normalizar separadores a slash para procesamiento simple
normalized = file_path.replace('\\', '/')
parts = normalized.split('/')
# quitar los ultimos dos componentes (Codigo/main.py) para obtener la carpeta src
if len(parts) >= 3:
    src_path = '/'.join(parts[:-2])
else:
    src_path = normalized
if src_path not in sys.path:
    sys.path.insert(0, src_path)

import menu

if __name__ == "__main__":
    menu.MenuDeInicio()