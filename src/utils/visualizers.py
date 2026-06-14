"""
Módulo de visualizaciones del Modelo 2.0
Usa Plotly para gráficos interactivos
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from config import DIMENSIONES, COLORS

def crear_radar_8d(dimensiones):
    """Crea gráfico radar de 8 dimensiones coloreadas"""
    
    labels = list(DIMENSIONES.keys())
    valores = [dimensiones.get(dim, {}).get('valor', 0) for dim in labels]
    
    # Colorear por severidad
    colores = []
    for valor in valores:
        if valor < 25:
            colores.append(COLORS['critico'])
        elif valor < 40:
            colores.append(COLORS['bajo'])
        elif valor < 60:
            colores.append(COLORS['moderado'])
        else:
            colores.append(COLORS['fuerte'])
    
    fig = go.Figure(data=go.Scatterpolar(
        r=valores,
        theta=labels,
        fill='toself',
        name='Dimensiones Cognitivas',
        fillcolor='rgba(102, 126, 234, 0.2)',
        line=dict(color='rgb(102, 126, 234)', width=2)
    ))
    
    # Agregar línea de umbral (40)
    fig.add_trace(go.Scatterpolar(
        r=[40] * len(labels),
        theta=labels,
        fill=None,
        name='Umbral mínimo',
        line=dict(color='rgba(255, 127, 14, 0.5)', dash='dash')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10)
            )
        ),
        showlegend=True,
        height=500,
        font=dict(size=11)
    )
    
    return fig

def crear_tabla_dimensiones(dimensiones):
    """Crea tabla interactiva de dimensiones"""
    data = []
    for dim, nombre in DIMENSIONES.items():
        valor = dimensiones.get(dim, {}).get('valor', 0)
        estado = dimensiones.get(dim, {}).get('estado', 'desconocido')
        
        # Ícono según estado
        if estado == 'crítico':
            icono = '❌'
        elif estado == 'bajo':
            icono = '⚠️'
        elif estado == 'moderado':
            icono = '⏸️'
        else:
            icono = '✓'
        
        data.append({
            'Dimensión': dim,
            'Nombre': nombre,
            'Valor': f"{valor:.0f}/100",
            'Estado': f"{icono} {estado.upper()}"
        })
    
    df = pd.DataFrame(data)
    return df

def crear_grafico_serie_temporal(memoria):
    """Serie temporal de 12 meses. Acepta un DataFrame (col 'Fecha' + dims) o un dict."""

    if memoria is None:
        return None

    colores_dims = {
        'IA': '#1f77b4', 'IAT': '#ff7f0e', 'ICI': '#d62728', 'IVC': '#2ca02c',
        'IME': '#9467bd', 'IIN': '#8c564b', 'IPRA': '#e377c2', 'ICS': '#7f7f7f',
    }

    # Normalizar la entrada -> (fechas, {dim: valores})
    if isinstance(memoria, pd.DataFrame):
        if memoria.empty:
            return None
        col_fecha = next((c for c in memoria.columns if str(c).strip().lower() == 'fecha'), None)
        fechas = memoria[col_fecha].astype(str).tolist() if col_fecha is not None else list(range(len(memoria)))
        series = {dim: pd.to_numeric(memoria[dim], errors='coerce').tolist()
                  for dim in DIMENSIONES if dim in memoria.columns}
    else:
        fechas = memoria.get('fechas', [])
        series = {dim: memoria.get(dim, []) for dim in DIMENSIONES}

    if not len(fechas):
        return None

    fig = go.Figure()
    for dim in DIMENSIONES.keys():
        valores = series.get(dim, [])
        if valores is not None and len(valores) > 0:
            fig.add_trace(go.Scatter(
                x=fechas, y=valores, mode='lines+markers', name=dim,
                line=dict(color=colores_dims.get(dim), width=2),
            ))

    fig.update_layout(
        title='Series Temporales (12 meses)', xaxis_title='Fecha',
        yaxis_title='Valor (0-100)', height=400, hovermode='x unified',
        legend=dict(x=0.01, y=0.99),
    )
    return fig

def crear_grafico_comparacion_actores(panel_0):
    """Crea gráfico de comparación de readiness entre actores"""
    
    if panel_0 is None or panel_0.empty:
        return None
    
    # Esperar que tenga columnas: Actor, Readiness_Actual, Readiness_Requerido
    if not all(col in panel_0.columns for col in ['Actor', 'Readiness_Actual', 'Readiness_Requerido']):
        return None
    
    fig = go.Figure(data=[
        go.Bar(
            x=panel_0['Actor'],
            y=panel_0['Readiness_Actual'],
            name='Readiness Actual',
            marker_color='rgb(102, 126, 234)'
        ),
        go.Bar(
            x=panel_0['Actor'],
            y=panel_0['Readiness_Requerido'],
            name='Readiness Requerido',
            marker_color='rgba(255, 127, 14, 0.5)'
        )
    ])
    
    fig.update_layout(
        barmode='group',
        title='Readiness: Actual vs Requerido',
        xaxis_title='Actor',
        yaxis_title='Readiness (0-100)',
        height=400,
        hovermode='x'
    )
    
    return fig

def crear_matriz_gates(gates_por_actor_fase):
    """Crea matriz de estados de gates"""
    
    # Estructura esperada: dict con actor como key, 
    # y valores dict con fase como key y estado como valor
    
    if not gates_por_actor_fase:
        return None
    
    data = []
    for actor, fases in gates_por_actor_fase.items():
        row = {'Actor': actor}
        for fase, estado in fases.items():
            # Convertir estado a color
            if estado == 'blocked':
                color_val = '❌ BLOQUEADO'
            elif estado == 'conditional':
                color_val = '⚠️ CONDICIONAL'
            else:
                color_val = '✅ HABILITADO'
            row[f'Fase {fase}'] = color_val
        data.append(row)
    
    return pd.DataFrame(data)

def crear_alertas_criticas(alertas):
    """Formatea alertas críticas para mostrar"""
    
    if not alertas:
        return None
    
    alertas_formateadas = []
    for alerta in alertas:
        if alerta.get('severidad') == 'CRÍTICA':
            alertas_formateadas.append({
                'Severidad': '🔴 CRÍTICA',
                'Alerta': alerta.get('alerta', ''),
                'Evidencia': alerta.get('evidencia', '')[:100] + '...'
            })
    
    if alertas_formateadas:
        return pd.DataFrame(alertas_formateadas)
    return None

def crear_gauge_readiness(valor_actual, valor_requerido):
    """Crea gauge de readiness comunitaria"""
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=valor_actual,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Readiness Comunitaria"},
        delta={'reference': valor_requerido},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 25], 'color': "lightgray"},
                {'range': [25, 50], 'color': "gray"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': valor_requerido
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig

def crear_barras_barreras_activos(barreras, activos):
    """Crea gráfico de barreras vs activos"""
    
    # Barreras (negativo)
    barreras_df = pd.DataFrame(barreras) if barreras else pd.DataFrame()
    activos_df = pd.DataFrame(activos) if activos else pd.DataFrame()
    
    fig = go.Figure()
    
    if not barreras_df.empty:
        fig.add_trace(go.Bar(
            y=barreras_df['nombre'],
            x=-barreras_df['valor'],
            name='Barreras',
            marker_color='rgb(214, 39, 40)',
            orientation='h'
        ))
    
    if not activos_df.empty:
        fig.add_trace(go.Bar(
            y=activos_df['nombre'],
            x=activos_df['valor'],
            name='Activos',
            marker_color='rgb(44, 160, 44)',
            orientation='h'
        ))
    
    fig.update_layout(
        barmode='relative',
        title='Barreras vs Activos',
        xaxis_title='Valor (-100 a +100)',
        height=400,
        showlegend=True
    )
    
    return fig
