# ⚡ Quick Start - Modelo 2.0

**¡Comienza en 5 minutos!**

## 1️⃣ Descarga el Proyecto

```bash
git clone <URL-REPO>
cd modelo-2-0-energia
```

## 2️⃣ Instalación Rápida

### Opción A: Windows
```bash
SETUP_WINDOWS.bat
```
Luego abre PowerShell en la carpeta y ejecuta:
```bash
streamlit run streamlit_app.py
```

### Opción B: macOS / Linux
```bash
chmod +x SETUP_LINUX_MAC.sh
./SETUP_LINUX_MAC.sh
source venv/bin/activate
streamlit run streamlit_app.py
```

### Opción C: Docker
```bash
docker-compose up
```

## 3️⃣ Acceso a la Aplicación

Abre en tu navegador:
```
http://localhost:8501
```

## 4️⃣ Cargar Datos

1. Ve a **Sidebar → ⚙️ CONFIGURACIÓN**
2. En la pestaña **📥 Cargar Datos**, sube los 5 archivos Excel:
   - `PANEL_0_PROTAGONISTAS.xlsx`
   - `DIMENSIONES_COGNITIVAS.xlsx`
   - `CONTEXTO_TERRITORIAL.xlsx`
   - `MEMORIA_TEMPORAL.xlsx`
   - `OPERATIVA_MATERIAL.xlsx`

> 💡 **Plantillas disponibles en:** `data/templates/`

## 5️⃣ Usar el Sistema

### Dashboard
```
[📊 Dashboard] → Vista general, alertas, matriz de gates
```

### Analizar Actor × Fase × Subcapa
```
[🔬 Micro-Red] → Selector de actor, fase, subcapa
              → [🔄 Calcular Micro-Red]
              → Ver resultados en 6 tabs
```

### Exportar Resultados
```
[💾 Export] → Descargar JSON, CSV, Resúmenes
```

---

## 📋 Archivos de Ejemplo

Se incluyen **plantillas Excel con datos de ejemplo**:

```
data/templates/
├── PANEL_0_PROTAGONISTAS.xlsx          ← 5 actores + readiness
├── DIMENSIONES_COGNITIVAS.xlsx         ← 8 dimensiones + encuestas
├── CONTEXTO_TERRITORIAL.xlsx           ← Indicadores DANE
├── MEMORIA_TEMPORAL.xlsx               ← Series 12 meses
└── OPERATIVA_MATERIAL.xlsx             ← Infraestructura
```

**Para pruebas rápidas:** Copia estos archivos a `data/uploads/`

---

## 🎯 Flujo Típico

1. **Cargar datos** → Sidebar
2. **Ver Dashboard** → Estado general
3. **Ir a Micro-Red** → Seleccionar actor/fase/subcapa
4. **Calcular** → Obtener análisis completo
5. **Ver resultados** → 6 tabs con información
6. **Exportar** → Descargar JSON/CSV

---

## ❓ Preguntas Frecuentes

### ¿Dónde están las plantillas Excel?
```
data/templates/
```
Copia cualquiera a `data/uploads/` para usarla.

### ¿Cómo actualizo datos sin reinstalar?
```
[⚙️ Configuración] → [📥 Cargar Datos] → Sube archivo nuevo
```
Automáticamente reemplaza el anterior.

### ¿Cómo exporto los resultados?
```
[💾 Export] → Selecciona formato (JSON/CSV/TXT)
          → [📥 Descargar]
```

### ¿Los datos se guardan?
Sí, en:
- `data/uploads/` - Archivos cargados
- `outputs/` - Descargas

### ¿Puedo usar en múltiples computadoras?
Sí, instala en cada máquina o usa **Streamlit Cloud** (gratuito).

---

## 🚀 Próximos Pasos

### Desarrollo Local
```bash
source venv/bin/activate              # Activar entorno
pip install -r requirements.txt       # Instalar deps
streamlit run streamlit_app.py       # Ejecutar
```

### Servidor (Linux)
Ver `INSTALL.md` para:
- Instalación con systemd
- Nginx reverse proxy
- SSL/HTTPS
- Backups automáticos

### Docker
```bash
docker-compose up -d      # Ejecutar en background
docker-compose logs -f    # Ver logs
docker-compose down       # Detener
```

---

## 📞 Soporte

- **Documentación completa:** Ver `README.md`
- **Instalación en servidor:** Ver `INSTALL.md`
- **Guía técnica:** Ver `/documentos/`
- **Email:** soporte@institucion.org
- **Issues:** GitHub Issues

---

## ✅ Checklist Post-Setup

- [ ] Archivo `requirements.txt` instalado
- [ ] Directorios creados (`data/uploads`, `outputs`)
- [ ] Aplicación ejecutándose en `http://localhost:8501`
- [ ] Archivos Excel cargados en `data/uploads/`
- [ ] Dashboard muestra datos
- [ ] Micro-Red calcula sin errores
- [ ] Exportación funciona

---

**¡Listo! Ahora puedes comenzar a usar Modelo 2.0** 🎉

**Versión**: 2.0 | **Última actualización**: Abril 2024
