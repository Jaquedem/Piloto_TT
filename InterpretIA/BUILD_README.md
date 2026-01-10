# 📦 Guía para Generar Ejecutable - InterpretIA

Esta guía te ayudará a generar un ejecutable standalone de InterpretIA.

## ⚠️ IMPORTANTE: Raspberry Pi

**Si estás usando Raspberry Pi**, NO uses esta guía. En su lugar, consulta:
📖 **[RASPBERRY_PI_README.md](RASPBERRY_PI_README.md)**

La Raspberry Pi usa arquitectura ARM y requiere un proceso diferente.

---

## 🎯 Opciones de Build

### **Opción 1: Script Automático (Recomendado)**

#### En Linux/Mac:
```bash
cd InterpretIA
chmod +x build_exe.sh
./build_exe.sh
```

#### En Windows:
```cmd
cd InterpretIA
build_exe.bat
```

---

### **Opción 2: Manual**

#### 1. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate.bat  # En Windows
```

#### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

#### 3. Generar ejecutable
```bash
pyinstaller InterpretIA.spec
```

#### 4. Encontrar el ejecutable
- **Linux/Mac**: `dist/InterpretIA`
- **Windows**: `dist/InterpretIA.exe`

---

## 📁 Estructura del Ejecutable

El ejecutable incluye:
- ✅ Código de la aplicación
- ✅ Modelo YOLO (`models/best.pt`)
- ✅ Logo (`src/Logo.png`)
- ✅ Configuración YAML (`data.yaml`)
- ✅ Todas las dependencias Python

---

## 🚀 Ejecutar la Aplicación

### Desde el ejecutable:
```bash
./dist/InterpretIA         # Linux/Mac
dist\InterpretIA.exe       # Windows
```

### Desde código fuente (desarrollo):
```bash
python main.py
```

---

## ⚙️ Configuración del Build

El archivo `InterpretIA.spec` controla la configuración del ejecutable:

- **`console=False`**: No muestra ventana de consola (GUI pura)
- **`upx=True`**: Compresión UPX para reducir tamaño
- **`datas`**: Archivos que se incluyen (modelo, logo, etc.)
- **`hiddenimports`**: Módulos que PyInstaller no detecta automáticamente

---

## 🛠️ Solución de Problemas

### Error: "No module named 'customtkinter'"
```bash
pip install customtkinter
```

### Error: "models/best.pt not found"
Verifica que el archivo `models/best.pt` existe en la carpeta correcta.

### Ejecutable muy grande
El ejecutable incluye todo el runtime de Python y las dependencias. Tamaño típico: 100-300MB.

### Error en Linux: "Permission denied"
```bash
chmod +x dist/InterpretIA
```

---

## 📊 Tamaños Aproximados

| Componente | Tamaño |
|------------|--------|
| Modelo YOLO | ~6 MB |
| Logo | ~4 MB |
| Python + Dependencias | ~100 MB |
| **Total** | **~110-150 MB** |

---

## ✨ Distribución

Para distribuir la aplicación:

1. **Archivo único**: Comparte solo el ejecutable de `dist/`
2. **Con instalador**: Usa herramientas como NSIS (Windows) o crear .deb/.rpm (Linux)
3. **Portable**: El ejecutable es completamente portable

---

## 📝 Notas

- El ejecutable es específico de la plataforma (Linux/Windows/Mac)
- Se recomienda generar el ejecutable en la plataforma destino
- La primera ejecución puede tardar un poco más (descompresión interna)

---

## 🆘 Soporte

Si encuentras problemas:
1. Verifica que todas las dependencias estén instaladas
2. Revisa los logs de PyInstaller en `build/`
3. Ejecuta con consola activada (`console=True` en .spec) para ver errores
