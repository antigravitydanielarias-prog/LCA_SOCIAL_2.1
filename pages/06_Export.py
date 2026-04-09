"""
Export - Descargas y Reportes
"""

import streamlit as st
import sys
from pathlib import Path
import json
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config import OUTPUTS_DIR
from utils.data_loader import cargar_todos_datos

st.set_page_config(page_title="Export", layout="wide")

st.title("💾 Export - Descargas y Reportes")

st.markdown("""
Descarga tus análisis en múltiples formatos para integración con otros sistemas.
""")

st.divider()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📄 JSON", "📊 CSV", "📋 Resúmenes", "🗂️ Archivos"])

with tab1:
    st.subheader("📄 Exportar JSON Estructurado")
    
    st.markdown("""
    JSON completo y validado para integración con sistemas externos.
    Compatible con APIs REST y pipelines de datos.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Opciones de Exportación")
        
        export_option = st.radio(
            "¿Qué deseas exportar?",
            ["Último análisis", "Múltiples análisis", "Panel 0 completo"],
            key="json_export_option"
        )
    
    with col2:
        st.markdown("#### Información")
        
        if export_option == "Último análisis":
            st.info("Exporta el último análisis de micro-red realizado")
        elif export_option == "Múltiples análisis":
            st.info("Exporta todos los análisis guardados")
        else:
            st.info("Exporta datos del Panel 0 con todos los actores")
    
    st.divider()
    
    if 'ultimo_resultado' in st.session_state:
        resultado = st.session_state.ultimo_resultado
        json_str = json.dumps(resultado, indent=2, ensure_ascii=False, default=str)
        
        st.code(json_str, language="json")
        
        st.download_button(
            "📥 Descargar JSON",
            data=json_str,
            file_name=f"modelo_2_0_{resultado['metadata']['actor'][:10]}_{resultado['metadata']['fecha_analisis'][:10]}.json",
            mime="application/json",
            key="download_json"
        )
    else:
        st.warning("⚠️ No hay análisis realizados aún. Ve a [🔬 Micro-Red] para crear uno.")

with tab2:
    st.subheader("📊 Exportar CSV")
    
    st.markdown("Exporta datos en formato CSV para Excel o análisis estadístico")
    
    datos = cargar_todos_datos()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Dimensiones Cognitivas")
        
        if datos.get('dimensiones') is not None:
            df = datos['dimensiones']
            csv = df.to_csv(index=False)
            
            st.download_button(
                "📥 Descargar CSV - Dimensiones",
                data=csv,
                file_name="dimensiones_cognitivas.csv",
                mime="text/csv",
                key="download_csv_dim"
            )
        else:
            st.warning("No hay datos de dimensiones")
    
    with col2:
        st.markdown("#### Contexto Territorial")
        
        if datos.get('contexto') is not None:
            df = datos['contexto']
            csv = df.to_csv(index=False)
            
            st.download_button(
                "📥 Descargar CSV - Contexto",
                data=csv,
                file_name="contexto_territorial.csv",
                mime="text/csv",
                key="download_csv_context"
            )
        else:
            st.warning("No hay datos de contexto")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Memoria Temporal")
        
        if datos.get('memoria') is not None:
            df = datos['memoria']
            csv = df.to_csv(index=False)
            
            st.download_button(
                "📥 Descargar CSV - Series",
                data=csv,
                file_name="memoria_temporal.csv",
                mime="text/csv",
                key="download_csv_memoria"
            )
        else:
            st.warning("No hay datos de memoria temporal")
    
    with col2:
        st.markdown("#### Panel 0")
        
        if datos.get('panel_0') is not None:
            df = datos['panel_0']
            csv = df.to_csv(index=False)
            
            st.download_button(
                "📥 Descargar CSV - Panel 0",
                data=csv,
                file_name="panel_0_protagonistas.csv",
                mime="text/csv",
                key="download_csv_panel0"
            )
        else:
            st.warning("No hay datos del Panel 0")

with tab3:
    st.subheader("📋 Resúmenes y Reportes")
    
    st.markdown("""
    Genera resúmenes rápidos de tu análisis.
    """)
    
    if 'ultimo_resultado' in st.session_state:
        resultado = st.session_state.ultimo_resultado
        
        # Crear resumen en texto
        resumen = f"""
RESUMEN EJECUTIVO - MODELO 2.0
================================

Actor: {resultado['metadata']['actor']}
Fase: {resultado['metadata']['fase']}
Subcapa: {resultado['metadata']['subcapa']}
Fecha: {resultado['metadata']['fecha_analisis']}

DIAGNÓSTICO:
{resultado.get('diagnostico', 'No disponible')}

ESTADO DEL GATE:
{resultado.get('estado_gate', '?').upper()} - {resultado.get('justificacion_gate', '')}

DIMENSIONES COGNITIVAS:
"""
        for dim, data in resultado.get('dimensiones_cognitivas', {}).items():
            resumen += f"  {dim}: {data.get('valor', 0):.0f}/100 ({data.get('estado', '?')})\n"
        
        resumen += f"\nBAARREAS IDENTIFICADAS: {len(resultado.get('barreras', []))}\n"
        for barrera in resultado.get('barreras', [])[:3]:
            resumen += f"  - {barrera['nombre']}\n"
        
        resumen += f"\nACTIVOS IDENTIFICADOS: {len(resultado.get('activos', []))}\n"
        for activo in resultado.get('activos', [])[:3]:
            resumen += f"  - {activo['nombre']}\n"
        
        st.text_area("Resumen Ejecutivo", value=resumen, height=300)
        
        st.download_button(
            "📥 Descargar Resumen (TXT)",
            data=resumen,
            file_name="resumen_ejecutivo.txt",
            mime="text/plain"
        )
    else:
        st.warning("⚠️ No hay análisis para resumir")

with tab4:
    st.subheader("🗂️ Archivos Descargados (Historial)")
    
    st.markdown("Archivos generados previamente en esta sesión:")
    
    outputs = list(OUTPUTS_DIR.glob("*"))
    
    if outputs:
        for archivo in sorted(outputs, reverse=True)[:10]:
            tamaño = archivo.stat().st_size
            if tamaño < 1024:
                tamaño_str = f"{tamaño} B"
            elif tamaño < 1024*1024:
                tamaño_str = f"{tamaño/1024:.1f} KB"
            else:
                tamaño_str = f"{tamaño/(1024*1024):.1f} MB"
            
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"📄 {archivo.name}")
            
            with col2:
                st.caption(tamaño_str)
            
            with col3:
                if st.button("🗑️", key=f"delete_{archivo.name}"):
                    archivo.unlink()
                    st.success("Eliminado")
    else:
        st.info("No hay archivos descargados aún")

st.divider()

st.subheader("📤 Exportación Avanzada")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Integración con Sistemas Externos")
    
    st.markdown("""
    Los datos JSON pueden integrarse con:
    
    - Power BI
    - Tableau
    - Jupyter Notebooks
    - APIs REST
    - Bases de datos
    - Dashboards personalizados
    """)

with col2:
    st.markdown("#### Formatos Soportados")
    
    st.markdown("""
    **Disponibles:**
    - JSON (estructura completa)
    - CSV (tabular)
    - TXT (resúmenes)
    
    **Próximamente:**
    - PDF (reportes formales)
    - XLSX (Excel avanzado)
    - PNG (gráficos)
    """)

# Footer
st.divider()

if st.button("← Volver al Dashboard"):
    st.switch_page("pages/01_Dashboard.py")
