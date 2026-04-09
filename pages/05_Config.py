"""
Configuración del Sistema - Gestión de Datos
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config import UPLOADS_DIR, TEMPLATES_DIR, EXCEL_FILES
from utils.data_loader import validar_carga_datos

st.set_page_config(page_title="Configuración", layout="wide")

st.title("⚙️ Configuración del Sistema")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📥 Cargar Datos", "📋 Validación", "📊 Archivos", "⚙️ Configuración"])

with tab1:
    st.subheader("📥 Cargar Archivos Excel")
    
    st.markdown("""
    Sube los 5 archivos requeridos para que el sistema funcione correctamente.
    Los archivos se guardarán en la carpeta `data/uploads/`
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Archivos Requeridos:")
        st.markdown("""
        1. **PANEL_0_PROTAGONISTAS.xlsx**
           - Pestaña: PROTAGONISTAS_READINESS
           - 5 actores con readiness
        
        2. **DIMENSIONES_COGNITIVAS.xlsx**
           - 8 pestañas (una por dimensión)
           - Encuestas Likert 1-5
        
        3. **CONTEXTO_TERRITORIAL.xlsx**
           - Pestaña: INDICADORES_DANE
           - Pobreza, educación, empleo, etc.
        """)
    
    with col2:
        st.markdown("#### Archivos Opcionales:")
        st.markdown("""
        4. **MEMORIA_TEMPORAL.xlsx**
           - Pestaña: SERIE_TEMPORAL_12M
           - Series de 12 meses
        
        5. **OPERATIVA_MATERIAL.xlsx**
           - Pestaña: INFRAESTRUCTURA
           - Recursos y capacidades
        """)
    
    st.divider()
    
    st.subheader("🔼 Subir Archivos")
    
    uploaded_files = st.file_uploader(
        "Selecciona uno o múltiples archivos Excel",
        type=['xlsx'],
        accept_multiple_files=True,
        key="config_uploader"
    )
    
    if uploaded_files:
        progress_bar = st.progress(0)
        for i, uploaded_file in enumerate(uploaded_files):
            save_path = UPLOADS_DIR / uploaded_file.name
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f"✅ {uploaded_file.name} cargado correctamente")
            progress_bar.progress((i + 1) / len(uploaded_files))
        
        st.info("💾 Los archivos han sido guardados. Actualiza la página o ve a Dashboard para usarlos.")
        st.cache_data.clear()

with tab2:
    st.subheader("✅ Validación de Datos")
    
    archivos_cargados, faltantes = validar_carga_datos()
    
    st.markdown("#### Estado de Archivos:")
    
    # Verificar cada archivo
    archivos_esperados = {
        'PANEL_0_PROTAGONISTAS.xlsx': '👥 Panel 0 - Protagonistas',
        'DIMENSIONES_COGNITIVAS.xlsx': '📊 Dimensiones Cognitivas',
        'CONTEXTO_TERRITORIAL.xlsx': '🌍 Contexto Territorial',
        'MEMORIA_TEMPORAL.xlsx': '⏰ Memoria Temporal',
        'OPERATIVA_MATERIAL.xlsx': '⚙️ Operativa-Material'
    }
    
    for archivo, descripcion in archivos_esperados.items():
        if (UPLOADS_DIR / archivo).exists():
            st.success(f"✅ {descripcion} - Cargado")
        else:
            st.warning(f"⚠️ {descripcion} - Pendiente")
    
    st.divider()
    
    if archivos_cargados:
        st.success("🎉 Todos los archivos requeridos están cargados. ¡Sistema listo para usar!")
    else:
        st.error(f"❌ Faltan {len(faltantes)} archivo(s). El sistema no funcionará completamente.")
        st.markdown(f"**Archivos faltantes:** {', '.join(faltantes)}")

with tab3:
    st.subheader("📊 Archivos en el Sistema")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📥 Archivos Cargados")
        archivos_cargados = list(UPLOADS_DIR.glob("*.xlsx"))
        
        if archivos_cargados:
            for archivo in sorted(archivos_cargados):
                tamaño = archivo.stat().st_size / 1024  # KB
                st.markdown(f"✓ **{archivo.name}** ({tamaño:.0f} KB)")
        else:
            st.info("No hay archivos cargados aún")
    
    with col2:
        st.markdown("#### 📂 Plantillas Disponibles")
        templates = list(TEMPLATES_DIR.glob("*.xlsx"))
        
        if templates:
            for template in sorted(templates):
                tamaño = template.stat().st_size / 1024
                st.markdown(f"📋 **{template.name}** ({tamaño:.0f} KB)")
        else:
            st.info("No hay plantillas disponibles")
    
    st.divider()
    
    st.subheader("🗑️ Gestión de Archivos")
    
    if st.button("🔄 Limpiar caché"):
        st.cache_data.clear()
        st.success("✅ Caché limpiado")
    
    if st.button("🗑️ Eliminar todos los archivos cargados"):
        for archivo in UPLOADS_DIR.glob("*.xlsx"):
            archivo.unlink()
        st.warning("✓ Archivos eliminados")
        st.cache_data.clear()

with tab4:
    st.subheader("⚙️ Configuración Avanzada")
    
    st.markdown("#### Thresholds de Gates")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**ICI Mínimo** (Confianza Institucional)")
        ici_min = st.slider(
            "Valor mínimo para proceder",
            min_value=0,
            max_value=100,
            value=40,
            step=5,
            key="ici_threshold"
        )
        st.caption("Por debajo de este valor, gate = BLOCKED")
    
    with col2:
        st.markdown("**IOM Mínimo** (Operativa-Material)")
        iom_min = st.slider(
            "Valor mínimo para proceder",
            min_value=0,
            max_value=100,
            value=30,
            step=5,
            key="iom_threshold"
        )
        st.caption("Por debajo de este valor, gate = BLOCKED")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Dimensión Crítica**")
        dim_critica = st.slider(
            "Umbral de dimensión crítica",
            min_value=0,
            max_value=100,
            value=25,
            step=5,
            key="dim_critica"
        )
        st.caption("Cualquier dimensión < este valor causa BLOCKED")
    
    with col2:
        st.markdown("**Pobreza Alto Riesgo**")
        pobreza_riesgo = st.slider(
            "Umbral de pobreza para riesgo alto",
            min_value=0,
            max_value=100,
            value=50,
            step=5,
            key="pobreza_riesgo"
        )
        st.caption("Pobreza > este valor puede causar CONDITIONAL")
    
    st.divider()
    
    st.markdown("#### Información del Sistema")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Versión", "2.0")
    
    with col2:
        st.metric("Estado", "Beta")
    
    with col3:
        st.metric("Última Actualización", "Abril 2024")
    
    st.markdown("""
    ---
    
    ### 📞 Soporte
    
    Para reportar problemas o hacer sugerencias:
    - **Email**: soporte@institucion.org
    - **Issues**: [GitHub Issues]
    - **Documentación**: Ver README.md
    """)

# Footer
st.divider()

if st.button("← Volver al Dashboard"):
    st.switch_page("pages/01_Dashboard.py")
