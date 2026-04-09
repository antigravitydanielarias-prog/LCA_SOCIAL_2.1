"""
MODELO 2.0 - Evaluación Multidimensional por Micro-Redes
Sistemas de Energía Comunitaria en Territorios en Desarrollo

Autor: Equipo de Análisis
Versión: 2.0
"""

import streamlit as st
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Configurar página
st.set_page_config(
    page_title="Modelo 2.0 - Energía Comunitaria",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Importar módulos
from config import PROJECT_ROOT, UPLOADS_DIR
from utils.data_loader import validar_carga_datos, descargar_templates

# Estilo CSS personalizado
st.markdown("""
<style>
    .main { padding: 20px; }
    .header { font-size: 2.5rem; font-weight: bold; color: #667eea; }
    .subheader { font-size: 1.5rem; font-weight: bold; color: #555; }
    .alert-blocked { color: #d62728; font-weight: bold; }
    .alert-conditional { color: #ff7f0e; font-weight: bold; }
    .alert-enabled { color: #2ca02c; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ CONFIGURACIÓN")
    st.divider()
    
    # Verificar archivos
    archivos_cargados, faltantes = validar_carga_datos()
    
    if archivos_cargados:
        st.success("✅ Todos los archivos están cargados")
    else:
        st.warning(f"⚠️ Faltan archivos: {', '.join(faltantes)}")
    
    st.divider()
    st.subheader("📋 Cargar Datos")
    
    uploaded_file = st.file_uploader(
        "Cargar archivo Excel",
        type=['xlsx'],
        help="Carga archivos Excel con los datos requeridos"
    )
    
    if uploaded_file:
        save_path = UPLOADS_DIR / uploaded_file.name
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"✅ {uploaded_file.name} cargado exitosamente")
        st.cache_data.clear()
    
    st.divider()
    st.subheader("📥 Descargar Templates")
    
    st.markdown("""
    Descarga las plantillas Excel para cargar tus datos:
    """)
    
    templates = descargar_templates()
    
    # Mostrar estado de templates
    for nombre, path in templates.items():
        if path.exists():
            st.success(f"✓ {nombre}")
        else:
            st.info(f"⚠️ {nombre} (template no disponible aún)")

# Página principal
st.markdown('<p class="header">⚡ MODELO 2.0</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Evaluación Multidimensional por Micro-Redes</p>', unsafe_allow_html=True)
st.markdown("Sistemas de Energía Comunitaria en Territorios en Desarrollo")

st.divider()

# Secciones principales
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📊 Dashboard")
    st.markdown("Vista general de actores, alertas y gates")
    if st.button("Ir a Dashboard →", key="btn_dashboard"):
        st.switch_page("pages/01_Dashboard.py")

with col2:
    st.markdown("### 👥 Panel 0")
    st.markdown("Protagonistas y readiness comunitaria")
    if st.button("Ir a Panel 0 →", key="btn_panel0"):
        st.switch_page("pages/02_Panel_0.py")

with col3:
    st.markdown("### 🔬 Micro-Red")
    st.markdown("Análisis profundo por actor × fase × subcapa")
    if st.button("Ir a Micro-Red →", key="btn_microred"):
        st.switch_page("pages/03_Micro_Red.py")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📈 Series Temporales")
    st.markdown("Seguimiento de 12 meses de cambios")
    if st.button("Ir a Series →", key="btn_series"):
        st.switch_page("pages/04_Series.py")

with col2:
    st.markdown("### 💾 Export")
    st.markdown("Descargar reportes JSON, CSV, PDF")
    if st.button("Ir a Export →", key="btn_export"):
        st.switch_page("pages/06_Export.py")

with col3:
    st.markdown("### ⚙️ Configuración")
    st.markdown("Datos, validación y umbrales")
    if st.button("Ir a Config →", key="btn_config"):
        st.switch_page("pages/05_Config.py")

st.divider()

# Información
st.markdown("""
## ℹ️ Acerca del Modelo 2.0

El **Modelo 2.0** es un sistema integral de evaluación que integra:

- **Capa Cognitiva**: 8 dimensiones (IA, IAT, ICI, IVC, IME, IIN, IPRA, ICS)
- **Capa Operativa-Material**: Infraestructura, capacidad técnica, recursos
- **Capa Territorial**: Contexto de pobreza, educación, empleo (DANE)
- **Memoria Temporal**: Series de 12 meses con detección de shocks
- **Panel 0**: 5 actores clave con readiness y alertas

### Salidas Principales:
1. **Micro-Redes**: Evaluaciones completas por actor × fase × subcapa
2. **Gates**: Estados (BLOCKED/CONDITIONAL/ENABLED)
3. **JSON Estructurado**: Salidas para integración con sistemas
4. **Costos**: Estimaciones de inversión y transición

---
**Versión**: 2.0 | **Estado**: Beta | **Última actualización**: 2024-04-07
""")

if not archivos_cargados:
    st.warning("""
    ⚠️ **Para usar el sistema, debes cargar los siguientes archivos Excel:**
    1. PANEL_0_PROTAGONISTAS.xlsx
    2. DIMENSIONES_COGNITIVAS.xlsx
    3. CONTEXTO_TERRITORIAL.xlsx
    4. MEMORIA_TEMPORAL.xlsx
    5. OPERATIVA_MATERIAL.xlsx
    
    Usa el panel lateral para cargar los archivos.
    """)
