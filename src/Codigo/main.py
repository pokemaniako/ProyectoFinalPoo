import sys
import os

SrcPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if SrcPath not in sys.path:
    sys.path.insert(0, SrcPath)

import menu

if __name__ == "__main__":
    menu.MenuDeInicio()