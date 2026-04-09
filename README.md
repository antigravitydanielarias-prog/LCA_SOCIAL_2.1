# MODELO 2.0 - Evaluación Multidimensional por Micro-Redes

**Sistemas de Energía Comunitaria en Territorios en Desarrollo**

## 🎯 Descripción

El **Modelo 2.0** es un sistema integral de evaluación que integra múltiples capas de análisis para evaluar la viabilidad y progreso de proyectos de energía comunitaria en territorios con desarrollo limitado.

### Características Principales

- **8 Dimensiones Cognitivas**: IA, IAT, ICI, IVC, IME, IIN, IPRA, ICS
- **Capa Operativa-Material**: Infraestructura, capacidad técnica, recursos
- **Contexto Territorial**: Indicadores DANE y proxies administrativos
- **Memoria Temporal**: Series de 12 meses con detección de shocks
- **Panel 0**: 5 actores clave con readiness y alertas
- **Gates Inteligentes**: Estados BLOCKED / CONDITIONAL / ENABLED

### Salidas

Cada análisis genera:
- **JSON Estructurado**: Completo y compatible con sistemas
- **Diagn óstico Narrativo**: Interpretación contextualizada
- **Costos de Transición**: Estimaciones de inversión
- **Recomendaciones Priorizadas**: Acciones específicas
- **Reportes Visuales**: Gráficos interactivos con Plotly

## 📋 Requisitos

- Python 3.9+
- pip (gestor de paquetes Python)
- Archivo Excel con estructura específica

## 🚀 Instalación Rápida

### Opción 1: Instalación Local

```bash
# Clonar repositorio
git clone <repo-url>
cd modelo-2-0-energia

# Crear entorno virtual
python -m venv venv

# Activar entorno
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
streamlit run streamlit_app.py
```

### Opción 2: Docker (Recomendado para servidor)

```bash
docker build -t modelo-2-0 .
docker run -p 8501:8501 modelo-2-0
```

### Opción 3: Streamlit Cloud (Gratuito)

1. Push a GitHub
2. Conectar con Streamlit Cloud
3. Desplegar automáticamente

## 📊 Estructura de Datos Requerida

### 5 Archivos Excel necesarios:

1. **PANEL_0_PROTAGONISTAS.xlsx**
   - Pestaña: `PROTAGONISTAS_READINESS`
   - Columnas: Actor, Readiness_Actual, Readiness_Requerido, Historial_12m, Tendencia, Alertas

2. **DIMENSIONES_COGNITIVAS.xlsx**
   - 8 pestañas (una por dimensión)
   - Preguntas Likert 1-5
   - Pestaña de resumen

3. **CONTEXTO_TERRITORIAL.xlsx**
   - Pestaña: `INDICADORES_DANE`
   - Indicadores: pobreza, informalidad, educación, internet, desempleo, participación

4. **MEMORIA_TEMPORAL.xlsx**
   - Pestaña: `SERIE_TEMPORAL_12M`
   - Series mensuales de 8 dimensiones
   - Registro de shocks/eventos

5. **OPERATIVA_MATERIAL.xlsx**
   - Pestaña: `INFRAESTRUCTURA`
   - Inventario de recursos físicos
   - Capacidades técnicas instaladas

## 🎮 Cómo Usar

### 1. Cargar Datos
```
Sidebar → Cargar Datos → Seleccionar archivo Excel
```

### 2. Navegar a Dashboard
```
Página principal → [📊 Dashboard]
```

### 3. Analizar Micro-Red
```
[🔬 Micro-Red] → Seleccionar Actor × Fase × Subcapa → [Calcular]
```

### 4. Exportar Resultados
```
[💾 Export] → Seleccionar formato (JSON/CSV/PDF) → [Descargar]
```

## 📚 Documentación Completa

Ver documentos:
- `MODELO_2_0_DOCUMENTACION_COMPLETA.txt` - Especificaciones técnicas
- `PLANTILLAS_EXCEL_ESTRUCTURA.txt` - Cómo llenar los Excel
- `STREAMLIT_INTEGRACION_ARQUITECTURA.txt` - Detalles técnicos
- `CHECKLIST_IMPLEMENTACION_MODELO_2_0.txt` - Timeline e implementación

## 🛠️ Instalación en Servidor

Ver `INSTALL.md` para:
- Instalación en Linux
- Configuración de Nginx
- SSL certificates
- Backup automático

## 📞 Soporte

- Reportar bugs: [Issues en GitHub]
- Preguntas: [Email de soporte]
- Documentación: Ver carpeta `/docs`

## 📄 Licencia

Este proyecto está bajo licencia [MIT/Propietaria]

## ✍️ Autores

- Equipo de Análisis de Energía Comunitaria
- Institución: [Nombre]
- Año: 2024

---

**Versión**: 2.0 | **Estado**: Beta | **Última actualización**: Abril 2024
