#!/bin/bash
# Script para generar el ejecutable de InterpretIA

echo "========================================="
echo "  InterpretIA - Build Ejecutable"
echo "========================================="
echo ""

# 1. Verificar que estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    echo "❌ Error: Ejecuta este script desde el directorio InterpretIA/"
    exit 1
fi

# 2. Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# 3. Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# 4. Instalar dependencias
echo "📥 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# 5. Limpiar builds anteriores
echo "🧹 Limpiando builds anteriores..."
rm -rf build/ dist/

# 6. Generar ejecutable con PyInstaller
echo "🚀 Generando ejecutable..."
pyinstaller InterpretIA.spec

# 7. Verificar que se generó correctamente
if [ -f "dist/InterpretIA" ]; then
    echo ""
    echo "========================================="
    echo "✅ Ejecutable generado exitosamente!"
    echo "========================================="
    echo ""
    echo "📁 Ubicación: dist/InterpretIA"
    echo ""
    echo "Para ejecutar:"
    echo "  ./dist/InterpretIA"
    echo ""
else
    echo ""
    echo "❌ Error: No se pudo generar el ejecutable"
    exit 1
fi
