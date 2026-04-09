"""
Panel 0 - Protagonistas y Readiness
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.data_loader import cargar_panel_0

st.set_page_config(page_title="Panel 0 - Protagonistas", layout="wide")

st.title("👥 Panel 0 - Protagonistas")

st.markdown("""
Visualización de los 5 actores clave con su readiness actual, histórico y alertas.
""")

st.divider()

# Cargar datos
panel_0 = cargar_panel_0()

if panel_0 is None or panel_0.empty:
    st.warning("⚠️ No hay datos cargados. Por favor carga Panel_0_PROTAGONISTAS.xlsx")
    
    # Mostrar ejemplo de estructura esperada
    st.subheader("📋 Estructura Esperada:")
    
    ejemplo = pd.DataFrame({
        'Actor': ['Comunidad Local', 'Gobierno Local', 'Proveedores Técnicos', 'Actores Económicos', 'Actores Externos'],
        'Readiness_Actual': [17, 8, 42, 25, 18],
        'Readiness_Requerido': [40, 35, 30, 25, 25],
        'Historial_12m': [5, 12, 35, 22, 25],
        'Tendencia': ['↑', '↓', '↑', '↑', '↓'],
        'Alertas': ['Diálogos iniciados', 'Cambio político', 'Ninguna', 'Ninguna', 'Fondos restringidos']
    })
    
    st.dataframe(ejemplo, use_container_width=True)
    
    st.info("📥 Carga el archivo PANEL_0_PROTAGONISTAS.xlsx con esta estructura en la pestaña PROTAGONISTAS_READINESS")
    
else:
    # Mostrar datos cargados
    st.subheader("📊 Estado Actual")
    st.dataframe(panel_0, use_container_width=True)
    
    st.divider()
    
    st.subheader("📈 Análisis por Actor")
    
    # Mostrar gráfico si hay datos suficientes
    if 'Readiness_Actual' in panel_0.columns and 'Readiness_Requerido' in panel_0.columns:
        import plotly.graph_objects as go
        
        fig = go.Figure(data=[
            go.Bar(x=panel_0['Actor'], y=panel_0['Readiness_Actual'], name='Actual', marker_color='#667eea'),
            go.Bar(x=panel_0['Actor'], y=panel_0['Readiness_Requerido'], name='Requerido', marker_color='#ff7f0e')
        ])
        
        fig.update_layout(
            barmode='group',
            title='Readiness: Actual vs Requerido por Actor',
            xaxis_title='Actor',
            yaxis_title='Readiness (0-100)',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Volver al dashboard
st.divider()
if st.button("← Volver al Dashboard"):
    st.switch_page("pages/01_Dashboard.py")
