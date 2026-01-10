# 🚀 Inicio Rápido - InterpretIA en Raspberry Pi

## ⚠️ ¿Error "Failed to execute child process 'xterm'"?

**Solución rápida:** NO hagas doble clic en archivos `.sh`. Usa desde **terminal** o el nuevo `start.py`.

Ver guía completa: **[SOLUCION_XTERM.md](SOLUCION_XTERM.md)**

---

## Métodos de Ejecución

### Opción 1: Python Directo (✅ Recomendado - Sin error xterm)

```bash
cd InterpretIA
python3 start.py
```

**Ventaja:** Funciona desde terminal Y con doble clic en el explorador de archivos.

### Opción 2: Launcher Bash (Desde terminal)

```bash
cd InterpretIA
./run_interpretia.sh
```

El launcher detecta automáticamente tu entorno (`venv`, `entornocamara`, `env`).

---

### Opción 2: Manual

```bash
cd InterpretIA
source entornocamara/bin/activate
python3 main.py
```

---

## Si necesitas instalar dependencias

### Instalar solo las dependencias faltantes:

```bash
cd InterpretIA
source entornocamara/bin/activate
pip install -r requirements.txt
```

---

### Instalación completa con setup automático:

```bash
cd InterpretIA
chmod +x setup_raspberry_pi.sh
./setup_raspberry_pi.sh
```

**Nota:** El script detectará que ya tienes `entornocamara` y lo usará automáticamente.

---

## Crear acceso directo en el escritorio

Crea el archivo `~/Desktop/InterpretIA.desktop`:

```bash
nano ~/Desktop/InterpretIA.desktop
```

Pega esto (ajusta la ruta si es necesario):

```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=InterpretIA
Comment=Intérprete de Lengua de Señas Mexicana
Exec=bash /home/pi/Piloto_TT/InterpretIA/run_interpretia.sh
Icon=/home/pi/Piloto_TT/InterpretIA/src/Logo.png
Terminal=false
Categories=Application;Education;
```

Dale permisos:

```bash
chmod +x ~/Desktop/InterpretIA.desktop
```

¡Ahora puedes hacer doble clic en el escritorio para ejecutar InterpretIA!

---

## ¿Problemas?

Consulta la guía completa: [RASPBERRY_PI_README.md](RASPBERRY_PI_README.md)
