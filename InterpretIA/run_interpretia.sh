#!/bin/bash
# Launcher para InterpretIA - Compatible con diferentes nombres de entorno virtual

cd "$(dirname "$0")"

# Detectar qué entorno virtual existe
if [ -d "entornocamara" ]; then
    echo "🔧 Usando entorno virtual: entornocamara"
    source entornocamara/bin/activate
elif [ -d "venv" ]; then
    echo "🔧 Usando entorno virtual: venv"
    source venv/bin/activate
elif [ -d "env" ]; then
    echo "🔧 Usando entorno virtual: env"
    source env/bin/activate
else
    echo "❌ Error: No se encontró ningún entorno virtual"
    echo ""
    echo "Por favor, crea uno primero:"
    echo "  python3 -m venv entornocamara"
    echo "  source entornocamara/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Ejecutar la aplicación
echo "🚀 Iniciando InterpretIA..."
python3 main.py
