#!/usr/bin/env python3
"""
Launcher Python para InterpretIA
No requiere terminal ni xterm - Ejecuta directamente la GUI
"""

import sys
import os
from pathlib import Path

# Cambiar al directorio del script
script_dir = Path(__file__).parent.absolute()
os.chdir(script_dir)

# Agregar al path para imports
sys.path.insert(0, str(script_dir))

# Verificar que estamos en un entorno virtual o que las dependencias están instaladas
try:
    import customtkinter
    import cv2
    from ultralytics import YOLO
    from PIL import Image
except ImportError as e:
    # Si falta alguna dependencia, mostrar error
    import tkinter as tk
    from tkinter import messagebox

    root = tk.Tk()
    root.withdraw()

    error_msg = f"""Error: Falta instalar dependencias.

Dependencia faltante: {str(e)}

Por favor, ejecuta desde terminal:
    cd {script_dir}
    source venv/bin/activate
    pip install -r requirements.txt

Luego vuelve a intentar."""

    messagebox.showerror("InterpretIA - Error de Dependencias", error_msg)
    sys.exit(1)

# Ejecutar la aplicación principal
if __name__ == "__main__":
    # Importar y ejecutar main
    import main
