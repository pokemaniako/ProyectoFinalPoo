import sys
import os
# Añadir la carpeta 'src' al sys.path para que los imports tipo 'from Csv.graficos import ...' funcionen
SrcPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if SrcPath not in sys.path:
    sys.path.insert(0, SrcPath)

import menu

if __name__ == "__main__":
    menu.MenuDeInicio()