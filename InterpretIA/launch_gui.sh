#!/bin/bash
# Launcher mejorado para Raspberry Pi - No requiere xterm

# Cambiar al directorio del script
cd "$(dirname "$0")"

# Detectar entorno virtual
if [ -d "venv" ]; then
    VENV="venv"
elif [ -d "entornocamara" ]; then
    VENV="entornocamara"
elif [ -d "env" ]; then
    VENV="env"
else
    # Si no hay entorno, mostrar error
    zenity --error --text="No se encontró entorno virtual.\n\nPor favor, ejecuta desde terminal:\ncd InterpretIA\npython3 -m venv venv\nsource venv/bin/activate\npip install -r requirements.txt" 2>/dev/null || \
    notify-send "Error" "No se encontró entorno virtual" 2>/dev/null || \
    echo "ERROR: No se encontró entorno virtual" > /tmp/interpretia_error.log
    exit 1
fi

# Activar entorno virtual y ejecutar
source "$VENV/bin/activate"
python3 main.py 2>&1 | tee /tmp/interpretia.log

# Si hay error, mostrarlo
if [ $? -ne 0 ]; then
    zenity --error --text="Error al ejecutar InterpretIA.\n\nRevisa el log en /tmp/interpretia.log" 2>/dev/null || \
    notify-send "Error" "Error al ejecutar InterpretIA" 2>/dev/null
fi
