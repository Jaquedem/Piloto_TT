#!/bin/bash
# Script de instalación para Raspberry Pi

echo "========================================="
echo "  InterpretIA - Setup Raspberry Pi"
echo "========================================="
echo ""

# 1. Verificar que estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    echo "❌ Error: Ejecuta este script desde el directorio InterpretIA/"
    exit 1
fi

# 2. Actualizar sistema
echo "📦 Actualizando sistema..."
sudo apt-get update

# 3. Instalar dependencias del sistema
echo "📥 Instalando dependencias del sistema..."
sudo apt-get install -y python3-pip python3-opencv python3-pil python3-tk

# 4. Instalar librerías adicionales para OpenCV
echo "📥 Instalando librerías de OpenCV..."
sudo apt-get install -y libatlas-base-dev libhdf5-dev libhdf5-serial-dev \
    libatlas-base-dev libjasper-dev libqtgui4 libqt4-test

# 5. Detectar o crear entorno virtual
if [ -d "entornocamara" ]; then
    echo "✅ Entorno virtual 'entornocamara' encontrado"
    VENV_NAME="entornocamara"
elif [ -d "venv" ]; then
    echo "✅ Entorno virtual 'venv' encontrado"
    VENV_NAME="venv"
elif [ -d "env" ]; then
    echo "✅ Entorno virtual 'env' encontrado"
    VENV_NAME="env"
else
    echo "🔧 Creando nuevo entorno virtual 'entornocamara'..."
    python3 -m venv entornocamara
    VENV_NAME="entornocamara"
fi

# 6. Activar entorno virtual
echo "🔌 Activando entorno virtual: $VENV_NAME..."
source $VENV_NAME/bin/activate

# 7. Actualizar pip
echo "⬆️  Actualizando pip..."
pip install --upgrade pip

# 8. Instalar dependencias Python
echo "📥 Instalando dependencias Python..."
pip install customtkinter
pip install opencv-python
pip install Pillow
pip install ultralytics

# 9. Dar permisos al launcher
echo "🚀 Configurando launcher..."
chmod +x run_interpretia.sh

# 10. Crear acceso directo de escritorio
echo "🖥️  Creando acceso directo de escritorio..."
DESKTOP_FILE="$HOME/Desktop/InterpretIA.desktop"
CURRENT_DIR="$(pwd)"

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=InterpretIA
Comment=Intérprete de Lengua de Señas Mexicana
Exec=bash $CURRENT_DIR/run_interpretia.sh
Icon=$CURRENT_DIR/src/Logo.png
Terminal=false
Categories=Application;Education;
EOF

chmod +x "$DESKTOP_FILE"

echo ""
echo "========================================="
echo "✅ Instalación completada!"
echo "========================================="
echo ""
echo "Opciones para ejecutar InterpretIA:"
echo ""
echo "1. Desde terminal:"
echo "   ./run_interpretia.sh"
echo ""
echo "2. Doble clic en el escritorio:"
echo "   'InterpretIA' (icono en el escritorio)"
echo ""
echo "3. Manualmente:"
echo "   source venv/bin/activate"
echo "   python3 main.py"
echo ""
