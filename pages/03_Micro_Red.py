"""
Micro-Red - Análisis Profundo por Actor × Fase × Subcapa
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import json

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config import ACTORES, DIMENSIONES
from utils.data_loader import cargar_todos_datos, validar_carga_datos
from utils.calculations import calcular_micro_red, exportar_json
from utils.visualizers import (
    crear_radar_8d,
    crear_tabla_dimensiones,
    crear_barras_barreras_activos
)

st.set_page_config(page_title="Micro-Red Analysis", layout="wide")

st.title("🔬 Micro-Red - Análisis Profundo")

st.markdown("""
Evaluación completa de un actor en una fase y subcapa específica.
Integra 8 dimensiones cognitivas, contexto territorial y operativa-material.
""")

st.divider()

# Verificar carga de datos
archivos_cargados, faltantes = validar_carga_datos()

if not archivos_cargados:
    st.warning(f"⚠️ Faltan archivos: {', '.join(faltantes)}")
    st.info("📥 Carga todos los archivos requeridos desde la configuración")
else:
    # Selectores
    col1, col2, col3 = st.columns(3)
    
    with col1:
        actor = st.selectbox("🎯 Actor", ACTORES, key="actor_selector")
    
    with col2:
        fase = st.selectbox("📍 Fase", [1, 2, 3], key="fase_selector")
    
    with col3:
        subcapa = st.selectbox("📂 Subcapa", ['A', 'B', 'C'], key="subcapa_selector")
    
    st.divider()
    
    # Botón para calcular
    if st.button("🔄 Calcular Micro-Red", key="btn_calculate"):
        with st.spinner("Calculando micro-red..."):
            try:
                # Cargar datos
                datos = cargar_todos_datos()
                
                # Calcular micro-red
                resultado = calcular_micro_red(actor, fase, subcapa, datos)
                
                # Guardar en session state
                st.session_state.ultimo_resultado = resultado
                
                st.success("✅ Micro-red calculada exitosamente")
                
            except Exception as e:
                st.error(f"❌ Error al calcular: {str(e)}")
    
    # Si existe resultado previo
    if 'ultimo_resultado' in st.session_state:
        resultado = st.session_state.ultimo_resultado
        
        st.divider()
        
        # Tabs para diferentes vistas
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Radar 8D",
            "📋 Dimensiones",
            "🌍 Contexto",
            "💡 Análisis",
            "🚪 Gate",
            "📄 JSON"
        ])
        
        with tab1:
            st.subheader("Radar 8D - Dimensiones Cognitivas")
            
            dims = resultado['dimensiones_cognitivas']
            fig = crear_radar_8d(dims)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("**Interpretación:**")
            st.markdown("""
            - Zona roja (< 25): Dimensiones críticas que requieren intervención inmediata
            - Zona naranja (25-40): Dimensiones bajas que necesitan apoyo
            - Zona amarilla (40-60): Dimensiones moderadas
            - Zona verde (60+): Dimensiones fortalecidas
            """)
        
        with tab2:
            st.subheader("Tabla de Dimensiones Cognitivas")
            
            df_dims = crear_tabla_dimensiones(dims)
            st.dataframe(df_dims, use_container_width=True)
            
            # Desglose por dimensión
            st.subheader("Detalle por Dimensión")
            
            for dim_code, dim_name in DIMENSIONES.items():
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    valor = dims.get(dim_code, {}).get('valor', 0)
                    st.progress(valor / 100, text=f"{dim_code}: {dim_name}")
                
                with col2:
                    st.metric("Valor", f"{valor:.0f}")
                
                with col3:
                    st.metric("Estado", dims.get(dim_code, {}).get('estado', '?'))
        
        with tab3:
            st.subheader("Contexto Territorial (DANE)")
            
            contexto = resultado.get('contexto_territorial', {})
            
            if contexto:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    pobreza = contexto.get('pobreza_multidimensional', 0)
                    st.metric("Pobreza Multidimensional", f"{pobreza:.0f}%")
                
                with col2:
                    informalidad = contexto.get('informalidad', 0)
                    st.metric("Informalidad", f"{informalidad:.0f}%")
                
                with col3:
                    educacion = contexto.get('educacion_promedio', 0)
                    st.metric("Educación Promedio", f"{educacion:.1f} años")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    internet = contexto.get('acceso_internet', 0)
                    st.metric("Acceso Internet", f"{internet:.0f}%")
                
                with col2:
                    desempleo = contexto.get('tasa_desempleo_juvenil', 0)
                    st.metric("Desempleo Juvenil", f"{desempleo:.0f}%")
                
                with col3:
                    participacion = contexto.get('participacion_ciudadana', 0)
                    st.metric("Participación Ciudadana", f"{participacion:.0f}%")
            else:
                st.info("⚠️ Datos de contexto territorial no disponibles")
        
        with tab4:
            st.subheader("Análisis y Puente Interpretativo")
            
            st.markdown("#### Diagnóstico:")
            st.markdown(resultado.get('diagnostico', 'No disponible'))
            
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🚧 Barreras Identificadas")
                barreras = resultado.get('barreras', [])
                if barreras:
                    for barrera in barreras[:5]:
                        with st.container(border=True):
                            st.markdown(f"**{barrera['nombre']}**")
                            st.markdown(f"Severidad: {barrera['severidad'].upper()}")
                            st.progress(barrera['valor'] / 100 if barrera['valor'] > 0 else 0)
                else:
                    st.info("No hay barreras identificadas")
            
            with col2:
                st.subheader("✨ Activos Identificados")
                activos = resultado.get('activos', [])
                if activos:
                    for activo in activos[:5]:
                        with st.container(border=True):
                            st.markdown(f"**{activo['nombre']}**")
                            st.markdown(f"Valor: {activo['valor']:.0f}/100")
                            st.progress(activo['valor'] / 100)
                else:
                    st.info("No hay activos identificados")
        
        with tab5:
            st.subheader("🚪 Estado de GATE")
            
            gate_state = resultado.get('estado_gate', 'unknown')
            
            if gate_state == 'blocked':
                st.error(f"❌ **BLOQUEADO**")
            elif gate_state == 'conditional':
                st.warning(f"⚠️ **CONDICIONAL**")
            else:
                st.success(f"✅ **HABILITADO**")
            
            st.markdown(f"**Justificación:** {resultado.get('justificacion_gate', 'No disponible')}")
            
            st.divider()
            
            st.subheader("💰 Costo de Transición")
            costo = resultado.get('costo_transicion', {})
            if costo:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Costo Directo", costo.get('costo_directo', 'N/A'))
                with col2:
                    st.metric("Contingencia (25%)", costo.get('contingencia_25pct', 'N/A'))
                with col3:
                    st.metric("Total", costo.get('total_presupuesto', 'N/A'))
                
                st.metric("Tiempo Estimado", costo.get('tiempo', 'N/A'))
            
            st.divider()
            
            st.subheader("📝 Recomendaciones")
            recomendaciones = resultado.get('recomendaciones', [])
            if recomendaciones:
                for rec in recomendaciones:
                    with st.container(border=True):
                        st.markdown(f"**[{rec['orden']}] {rec['accion']}**")
                        st.markdown(f"Prioridad: {rec['prioridad']} | Plazo: {rec['plazo']}")
            else:
                st.info("No hay recomendaciones")
        
        with tab6:
            st.subheader("📄 JSON Estructurado")
            
            # Mostrar JSON
            json_str = exportar_json(resultado)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.code(json_str, language="json")
            
            with col2:
                st.markdown("### Opciones de Descarga")
                
                st.download_button(
                    "📥 Descargar JSON",
                    data=json_str,
                    file_name=f"micro_red_{actor.lower().replace(' ', '_')}_{fase}_{subcapa}.json",
                    mime="application/json"
                )
                
                # Copiar al portapapeles (simple)
                if st.button("📋 Copiar JSON"):
                    st.info("JSON copiado al portapapeles")
        
        st.divider()
        
        # Información de confianza
        confianza = resultado.get('nivel_confianza', 0)
        st.markdown(f"**Nivel de Confianza en el Análisis:** {confianza}% ")
        
        if resultado.get('datos_faltantes'):
            st.warning(f"⚠️ Datos faltantes: {', '.join(resultado['datos_faltantes'])}")

# Footer
st.divider()
if st.button("← Volver al Dashboard"):
    st.switch_page("pages/01_Dashboard.py")
