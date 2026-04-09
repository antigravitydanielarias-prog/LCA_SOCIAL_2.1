"""
Dashboard - Vista General del Modelo 2.0
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.data_loader import cargar_panel_0, cargar_dimensiones_cognitivas
from utils.visualizers import (
    crear_grafico_comparacion_actores, 
    crear_gauge_readiness,
    crear_alertas_criticas
)

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📊 Dashboard - Visión General")

st.markdown("""
Panel de control centralizado con alertas, estado de gates y readiness comunitaria.
""")

st.divider()

# Cargar datos
panel_0 = cargar_panel_0()

if panel_0 is None or panel_0.empty:
    st.warning("⚠️ No hay datos cargados. Por favor carga los archivos desde la configuración.")
    st.info("📋 Usa el botón 'Cargar Datos' en el panel lateral")
else:
    # Sección de Alertas Críticas
    st.subheader("🚨 Alertas Críticas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.error("❌ BLOQUEADO")
        st.markdown("**Comunidad × Fase 1 × 1B**")
        st.markdown("ICI=28 < 40 (Confianza crítica)")
    
    with col2:
        st.warning("⚠️ CONDICIONAL")
        st.markdown("**Gobierno × Fase 1 × 1C**")
        st.markdown("Marco regulatorio pendiente")
    
    with col3:
        st.warning("⚠️ RIESGO")
        st.markdown("**Actores Externos**")
        st.markdown("Readiness -7 en últimos 6 meses")
    
    st.divider()
    
    # Sección de Readiness
    st.subheader("📊 Readiness Comunitaria Agregada")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Gauge de readiness
        fig_gauge = crear_gauge_readiness(17, 40)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        st.metric(
            "Actual",
            "17/100",
            delta="+12",
            delta_color="normal"
        )
        st.markdown("*Última medición: 12 meses*")
    
    with col3:
        st.metric(
            "Requerido",
            "40/100",
            delta="-23",
            delta_color="inverse"
        )
        st.markdown("*Para Fase 1*")
    
    st.divider()
    
    # Comparación de actores
    st.subheader("👥 Readiness por Actor")
    
    if not panel_0.empty:
        # Crear datos de comparación si existen columnas
        if all(col in panel_0.columns for col in ['Actor', 'Readiness_Actual', 'Readiness_Requerido']):
            fig = crear_grafico_comparacion_actores(panel_0)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("⚠️ Estructura de datos no coincide con lo esperado")
            st.dataframe(panel_0, use_container_width=True)
    
    st.divider()
    
    # Matriz de Gates
    st.subheader("🚪 Matriz de Estados de Gates")
    
    gates_data = {
        'Actor': ['Comunidad', 'Gobierno', 'Técnicos', 'Económicos', 'Externos'],
        '1A': ['✅', '✅', '✅', '✅', '⚠️'],
        '1B': ['❌', '✅', '✅', '✅', '?'],
        '1C': ['❌', '⚠️', '✅', '?', '?'],
        '2A': ['?', '?', '?', '?', '?'],
        '2B': ['?', '?', '?', '?', '?'],
        '2C': ['?', '?', '?', '?', '?'],
        '3A': ['?', '?', '?', '?', '?'],
        '3B': ['?', '?', '?', '?', '?'],
        '3C': ['?', '?', '?', '?', '?'],
    }
    
    import pandas as pd
    df_gates = pd.DataFrame(gates_data)
    st.dataframe(df_gates, use_container_width=True)
    
    st.markdown("""
    **Leyenda:**
    - ✅ HABILITADO: Proceder sin condiciones
    - ⚠️ CONDICIONAL: Proceder con condiciones específicas
    - ❌ BLOQUEADO: Requiere acciones previas
    - ? PENDIENTE: Por evaluar
    """)
    
    st.divider()
    
    # Información y próximos pasos
    st.subheader("📋 Próximos Pasos Recomendados")
    
    st.markdown("""
    ### Inmediato (Esta semana):
    1. **Diálogos de Reparación con Comunidad** → Resolver desconfianza (ICI=28)
    2. **Formalizar Compromiso Municipal** → Obtener respaldo político
    3. **Revisar Marco Regulatorio** → Alineación legal
    
    ### Corto Plazo (1-3 meses):
    1. Capacitación digital para comunidad (IAT: 38 → 50)
    2. Talleres de aspiraciones (IA: 45 → mantener)
    3. Evaluación técnica detallada (Fase 1B)
    
    ### Mediano Plazo (3-6 meses):
    1. Diseño participativo del proyecto (Fase 1C)
    2. Búsqueda de financiamiento
    3. Constitución de cooperativa
    """)
    
    # Footer
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔬 Ir a Micro-Red Analysis"):
            st.switch_page("pages/03_Micro_Red.py")
    
    with col2:
        if st.button("👥 Ir a Panel 0"):
            st.switch_page("pages/02_Panel_0.py")
    
    with col3:
        if st.button("💾 Ir a Export"):
            st.switch_page("pages/06_Export.py")
