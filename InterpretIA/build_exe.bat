@echo off
REM Script para generar el ejecutable de InterpretIA en Windows

echo =========================================
echo   InterpretIA - Build Ejecutable
echo =========================================
echo.

REM 1. Verificar que estamos en el directorio correcto
if not exist "main.py" (
    echo ERROR: Ejecuta este script desde el directorio InterpretIA\
    pause
    exit /b 1
)

REM 2. Crear entorno virtual si no existe
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
)

REM 3. Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat

REM 4. Instalar dependencias
echo Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt

REM 5. Limpiar builds anteriores
echo Limpiando builds anteriores...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM 6. Generar ejecutable con PyInstaller
echo Generando ejecutable...
pyinstaller InterpretIA.spec

REM 7. Verificar que se generó correctamente
if exist "dist\InterpretIA.exe" (
    echo.
    echo =========================================
    echo Ejecutable generado exitosamente!
    echo =========================================
    echo.
    echo Ubicacion: dist\InterpretIA.exe
    echo.
    echo Para ejecutar: dist\InterpretIA.exe
    echo.
) else (
    echo.
    echo ERROR: No se pudo generar el ejecutable
    pause
    exit /b 1
)

pause
