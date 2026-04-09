"""
Series Temporales - Seguimiento de 12 meses
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config import DIMENSIONES
from utils.data_loader import cargar_memoria_temporal
from utils.visualizers import crear_grafico_serie_temporal

st.set_page_config(page_title="Series Temporales", layout="wide")

st.title("📈 Series Temporales - Seguimiento 12 Meses")

st.markdown("""
Visualiza cómo han evolucionado las 8 dimensiones en los últimos 12 meses.
Identifica tendencias, shocks y cambios significativos.
""")

st.divider()

# Cargar datos
memoria = cargar_memoria_temporal()

if memoria is None or memoria.empty:
    st.warning("⚠️ No hay datos de memoria temporal cargados")
    st.info("📥 Carga MEMORIA_TEMPORAL.xlsx desde la configuración")
    
    # Mostrar estructura esperada
    st.subheader("📋 Estructura Esperada:")
    
    ejemplo = pd.DataFrame({
        'Fecha': ['Ago 2023', 'Sep 2023', 'Oct 2023', '...', 'Ago 2024'],
        'IA': [35, 36, 37, '...', 45],
        'IAT': [38, 38, 38, '...', 38],
        'ICI': [32, 31, 30, '...', 28],
        'IVC': [64, 65, 66, '...', 72],
        'IME': [30, 30, 31, '...', 32],
        'IIN': [53, 53, 54, '...', 55],
        'IPRA': [38, 39, 40, '...', 41],
        'ICS': [35, 35, 36, '...', 38],
        'Eventos': ['', 'Inicio diálogos', 'Capacitación', '...', '(Actual)']
    })
    
    st.dataframe(ejemplo, use_container_width=True)
    
else:
    # Mostrar gráfico de series
    st.subheader("📊 Evolución de 8 Dimensiones (12 meses)")
    
    fig = crear_grafico_serie_temporal(memoria)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Tabla de datos
    st.subheader("📋 Datos Brutos")
    st.dataframe(memoria, use_container_width=True)
    
    st.divider()
    
    # Análisis de tendencias
    st.subheader("📈 Análisis de Tendencias")
    
    if not memoria.empty:
        # Calcular cambios
        cambios = {}
        for dim in DIMENSIONES.keys():
            if dim in memoria.columns:
                valores = pd.to_numeric(memoria[dim], errors='coerce')
                if len(valores) >= 2:
                    primer_valor = valores.iloc[0]
                    ultimo_valor = valores.iloc[-1]
                    cambio = ultimo_valor - primer_valor
                    cambio_pct = (cambio / primer_valor * 100) if primer_valor != 0 else 0
                    
                    cambios[dim] = {
                        'primer': primer_valor,
                        'último': ultimo_valor,
                        'cambio': cambio,
                        'cambio_pct': cambio_pct,
                        'tendencia': '↑' if cambio > 0 else ('↓' if cambio < 0 else '→')
                    }
        
        # Mostrar análisis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📈 Dimensiones en Mejora")
            mejoras = [(dim, data) for dim, data in cambios.items() if data['cambio'] > 0]
            mejoras.sort(key=lambda x: x[1]['cambio'], reverse=True)
            
            for dim, data in mejoras[:4]:
                st.metric(
                    f"{dim} - {DIMENSIONES[dim]}",
                    f"{data['último']:.0f}",
                    delta=f"+{data['cambio']:.0f} ({data['cambio_pct']:.1f}%)",
                    delta_color="normal"
                )
        
        with col2:
            st.markdown("#### 📉 Dimensiones en Declive")
            declives = [(dim, data) for dim, data in cambios.items() if data['cambio'] < 0]
            declives.sort(key=lambda x: x[1]['cambio'])
            
            for dim, data in declives[:4]:
                st.metric(
                    f"{dim} - {DIMENSIONES[dim]}",
                    f"{data['último']:.0f}",
                    delta=f"{data['cambio']:.0f} ({data['cambio_pct']:.1f}%)",
                    delta_color="inverse"
                )
        
        st.divider()
        
        # Detección de volatilidad
        st.subheader("🌊 Análisis de Volatilidad")
        
        volatilidad_data = []
        for dim in DIMENSIONES.keys():
            if dim in memoria.columns:
                valores = pd.to_numeric(memoria[dim], errors='coerce')
                if len(valores) > 1:
                    volatilidad = valores.std()
                    max_val = valores.max()
                    min_val = valores.min()
                    rango = max_val - min_val
                    
                    volatilidad_data.append({
                        'Dimensión': dim,
                        'Volatilidad': volatilidad,
                        'Rango': rango,
                        'Min': min_val,
                        'Max': max_val,
                        'Tipo': 'Alta' if volatilidad > 2 else ('Media' if volatilidad > 0.5 else 'Baja')
                    })
        
        if volatilidad_data:
            df_volatilidad = pd.DataFrame(volatilidad_data)
            df_volatilidad = df_volatilidad.sort_values('Volatilidad', ascending=False)
            st.dataframe(df_volatilidad, use_container_width=True)
            
            st.markdown("""
            **Interpretación:**
            - **Alta volatilidad** (>2): Dimensión inestable, requiere monitoreo
            - **Media volatilidad** (0.5-2): Cambios moderados
            - **Baja volatilidad** (<0.5): Dimensión estable
            """)
    
    st.divider()
    
    # Detección de shocks
    if 'Eventos' in memoria.columns:
        st.subheader("⚡ Shocks y Eventos Detectados")
        
        eventos = memoria[memoria['Eventos'].notna() & (memoria['Eventos'] != '')]
        if not eventos.empty:
            for idx, row in eventos.iterrows():
                with st.container(border=True):
                    st.markdown(f"**{row['Fecha']}** - {row['Eventos']}")
        else:
            st.info("No hay eventos registrados")

# Descargar datos
st.divider()

if st.button("← Volver al Dashboard"):
    st.switch_page("pages/01_Dashboard.py")
