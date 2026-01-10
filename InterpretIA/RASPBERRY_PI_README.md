# 🥧 Guía de Instalación para Raspberry Pi

Esta guía te ayudará a ejecutar InterpretIA en tu Raspberry Pi.

## ⚠️ IMPORTANTE: Arquitectura ARM

**NO puedes usar un ejecutable compilado en otra computadora.** La Raspberry Pi usa arquitectura ARM, no x86_64. Por eso, ejecutaremos directamente con Python.

---

## 🚀 Instalación Rápida (Recomendado)

### Paso 1: Navegar al directorio
```bash
cd InterpretIA
```

### Paso 2: Ejecutar el script de instalación
```bash
chmod +x setup_raspberry_pi.sh
./setup_raspberry_pi.sh
```

**Esto instalará:**
- ✅ Dependencias del sistema (OpenCV, Pillow, etc.)
- ✅ Detecta tu entorno virtual existente (entornocamara, venv, env)
- ✅ O crea uno nuevo si no existe
- ✅ Todas las librerías necesarias
- ✅ Launcher ejecutable (`run_interpretia.sh`)
- ✅ Acceso directo en el escritorio

**Nota:** Si ya tienes un entorno virtual (como `entornocamara`), el script lo detectará automáticamente y lo usará.

**Tiempo estimado:** 10-15 minutos (dependiendo de la conexión)

---

## 🎯 Ejecutar InterpretIA

Después de la instalación, tienes 3 opciones:

### **Opción 1: Doble clic en el escritorio**
1. Ve al escritorio de tu Raspberry Pi
2. Busca el ícono "InterpretIA"
3. Haz doble clic
4. ¡Listo!

### **Opción 2: Desde terminal**
```bash
cd InterpretIA
./run_interpretia.sh
```

### **Opción 3: Manualmente**
```bash
cd InterpretIA
source venv/bin/activate
python3 main.py
```

---

## 🔧 Instalación Manual (Si prefieres hacerlo paso a paso)

### 1. Actualizar sistema
```bash
sudo apt-get update
sudo apt-get upgrade
```

### 2. Instalar dependencias del sistema
```bash
sudo apt-get install -y python3-pip python3-opencv python3-pil python3-tk
sudo apt-get install -y libatlas-base-dev libhdf5-dev libhdf5-serial-dev
```

### 3. Crear o activar entorno virtual

**Si ya tienes un entorno (como `entornocamara`):**
```bash
cd InterpretIA
source entornocamara/bin/activate
```

**Si necesitas crear uno nuevo:**
```bash
cd InterpretIA
python3 -m venv entornocamara  # O usa 'venv' si prefieres
source entornocamara/bin/activate
```

### 4. Instalar dependencias Python
```bash
pip install --upgrade pip
pip install customtkinter opencv-python Pillow ultralytics
```

### 5. Ejecutar
```bash
python3 main.py
```

---

## 🛠️ Solución de Problemas

### Ya tengo un entorno virtual con otro nombre
No hay problema. El launcher `run_interpretia.sh` detecta automáticamente estos nombres:
- `entornocamara`
- `venv`
- `env`

Si tu entorno tiene otro nombre, edita `run_interpretia.sh` y agrega tu nombre en la detección.

### Error: "Failed to execute child process 'xterm'"
Este error ocurre cuando intentas ejecutar un archivo .sh sin permisos. **Solución:**
```bash
chmod +x setup_raspberry_pi.sh
chmod +x run_interpretia.sh
```

### Error: "No module named 'customtkinter'"
Las dependencias no están instaladas. **Solución:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "Camera not found"
Verifica que la cámara esté conectada:
```bash
vcgencmd get_camera
# Debe mostrar: supported=1 detected=1
```

### La aplicación va lenta
Raspberry Pi tiene recursos limitados. **Optimizaciones:**
1. Cierra otras aplicaciones
2. Usa Raspberry Pi 4 (mínimo 2GB RAM recomendado)
3. Considera reducir la resolución de la cámara en `gui.py`

### Error: "cv2.imshow() not working"
Asegúrate de tener instalado el backend de display:
```bash
sudo apt-get install python3-tk
```

---

## 📊 Requisitos de Sistema

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| **Modelo** | Raspberry Pi 3B+ | Raspberry Pi 4 |
| **RAM** | 1 GB | 2-4 GB |
| **Cámara** | USB Webcam / Pi Camera | USB Webcam HD |
| **SO** | Raspberry Pi OS (32-bit) | Raspberry Pi OS (64-bit) |
| **Espacio** | 2 GB libre | 5 GB libre |

---

## ⚡ Optimizaciones para Raspberry Pi

### Reducir uso de CPU
En `gui.py`, puedes cambiar:
```python
self.frame_count % 3 == 0  # Procesa cada 3 frames
```
A:
```python
self.frame_count % 5 == 0  # Procesa cada 5 frames (más lento pero menos CPU)
```

### Reducir resolución
En `gui.py`, encuentra:
```python
results = self.model(frame, verbose=False, conf=0.6, imgsz=320)
```
Puedes cambiar `imgsz=320` a `imgsz=224` para mayor velocidad.

---

## 🎥 Configuración de Cámara

### Habilitar Pi Camera
```bash
sudo raspi-config
# Interfacing Options → Camera → Enable
```

### Verificar cámaras USB
```bash
v4l2-ctl --list-devices
```

### Cambiar índice de cámara
Si tienes múltiples cámaras, en `gui.py` cambia:
```python
self.cap = cv2.VideoCapture(0)  # 0 = primera cámara
# Prueba con: 1, 2, etc.
```

---

## 📝 Crear Acceso Directo Manualmente

Si el script no creó el acceso directo, hazlo así:

1. Crear archivo `InterpretIA.desktop` en el escritorio:
```bash
nano ~/Desktop/InterpretIA.desktop
```

2. Pegar este contenido:
```
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

3. Dar permisos:
```bash
chmod +x ~/Desktop/InterpretIA.desktop
```

---

## 🔄 Actualizar la Aplicación

```bash
cd /home/pi/Piloto_TT
git pull origin claude/review-project-glNtE
cd InterpretIA
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

---

## 📞 Soporte

### Verificar instalación
```bash
cd InterpretIA
source venv/bin/activate
python3 -c "import cv2, customtkinter, ultralytics; print('✅ Todo OK')"
```

### Ver logs de ejecución
```bash
cd InterpretIA
./run_interpretia.sh 2>&1 | tee debug.log
```

---

## 💡 Notas Importantes

- 🚫 **NO uses PyInstaller en Raspberry Pi** - Es mejor ejecutar directamente con Python
- 🎥 **Prueba tu cámara primero** con `InterpretIA/pruebacam.py`
- ⚡ **Raspberry Pi 3 o inferior será lento** - Considera reducir FPS
- 🌡️ **Monitorea la temperatura** - `vcgencmd measure_temp`
- 🔌 **Usa fuente de 3A** - Modelos 4 requieren más potencia

---

## ✅ Checklist de Instalación

- [ ] Sistema actualizado (`sudo apt-get update`)
- [ ] Dependencias del sistema instaladas
- [ ] Entorno virtual creado
- [ ] Dependencias Python instaladas
- [ ] Cámara conectada y funcionando
- [ ] `run_interpretia.sh` tiene permisos de ejecución
- [ ] Acceso directo creado en escritorio
- [ ] Aplicación ejecuta correctamente

---

¡Disfruta usando InterpretIA en tu Raspberry Pi! 🥧🎉
