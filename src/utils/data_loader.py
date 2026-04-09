"""
Módulo para cargar datos desde archivos Excel
"""
import pandas as pd
import streamlit as st
from pathlib import Path
from config import UPLOADS_DIR, TEMPLATES_DIR, DIMENSIONES, ACTORES

@st.cache_data
def cargar_panel_0(filepath=None):
    """Carga datos del Panel 0 (Protagonistas)"""
    if filepath is None:
        filepath = UPLOADS_DIR / 'PANEL_0_PROTAGONISTAS.xlsx'
    
    if not Path(filepath).exists():
        return None
    
    try:
        df = pd.read_excel(filepath, sheet_name='PROTAGONISTAS_READINESS')
        return df
    except Exception as e:
        st.error(f"Error cargando Panel 0: {e}")
        return None

@st.cache_data
def cargar_dimensiones_cognitivas(filepath=None):
    """Carga datos de dimensiones cognitivas"""
    if filepath is None:
        filepath = UPLOADS_DIR / 'DIMENSIONES_COGNITIVAS.xlsx'
    
    if not Path(filepath).exists():
        return None
    
    try:
        # Cargar la pestaña de resumen que debe existir
        df_resumen = pd.read_excel(filepath, sheet_name='RESUMEN')
        return df_resumen
    except Exception as e:
        st.error(f"Error cargando dimensiones: {e}")
        return None

@st.cache_data
def cargar_contexto_territorial(filepath=None):
    """Carga datos de contexto territorial"""
    if filepath is None:
        filepath = UPLOADS_DIR / 'CONTEXTO_TERRITORIAL.xlsx'
    
    if not Path(filepath).exists():
        return None
    
    try:
        df = pd.read_excel(filepath, sheet_name='INDICADORES_DANE')
        return df
    except Exception as e:
        st.error(f"Error cargando contexto territorial: {e}")
        return None

@st.cache_data
def cargar_memoria_temporal(filepath=None):
    """Carga datos de memoria temporal"""
    if filepath is None:
        filepath = UPLOADS_DIR / 'MEMORIA_TEMPORAL.xlsx'
    
    if not Path(filepath).exists():
        return None
    
    try:
        df = pd.read_excel(filepath, sheet_name='SERIE_TEMPORAL_12M')
        return df
    except Exception as e:
        st.error(f"Error cargando memoria temporal: {e}")
        return None

@st.cache_data
def cargar_operativa_material(filepath=None):
    """Carga datos de dimensión operativa-material"""
    if filepath is None:
        filepath = UPLOADS_DIR / 'OPERATIVA_MATERIAL.xlsx'
    
    if not Path(filepath).exists():
        return None
    
    try:
        df = pd.read_excel(filepath, sheet_name='INFRAESTRUCTURA')
        return df
    except Exception as e:
        st.error(f"Error cargando operativa-material: {e}")
        return None

def validar_carga_datos():
    """Valida que todos los archivos requeridos estén cargados"""
    archivos_requeridos = [
        'PANEL_0_PROTAGONISTAS.xlsx',
        'DIMENSIONES_COGNITIVAS.xlsx',
        'CONTEXTO_TERRITORIAL.xlsx',
        'MEMORIA_TEMPORAL.xlsx',
        'OPERATIVA_MATERIAL.xlsx'
    ]
    
    archivos_faltantes = []
    for archivo in archivos_requeridos:
        if not (UPLOADS_DIR / archivo).exists():
            archivos_faltantes.append(archivo)
    
    return len(archivos_faltantes) == 0, archivos_faltantes

def descargar_templates():
    """Retorna diccionario con paths de templates"""
    return {
        'panel_0': TEMPLATES_DIR / 'PANEL_0_PROTAGONISTAS_TEMPLATE.xlsx',
        'dimensiones': TEMPLATES_DIR / 'DIMENSIONES_COGNITIVAS_TEMPLATE.xlsx',
        'contexto': TEMPLATES_DIR / 'CONTEXTO_TERRITORIAL_TEMPLATE.xlsx',
        'memoria': TEMPLATES_DIR / 'MEMORIA_TEMPORAL_TEMPLATE.xlsx',
        'operativa': TEMPLATES_DIR / 'OPERATIVA_MATERIAL_TEMPLATE.xlsx'
    }

def cargar_todos_datos():
    """Carga todos los datos y retorna diccionario consolidado"""
    datos = {
        'panel_0': cargar_panel_0(),
        'dimensiones': cargar_dimensiones_cognitivas(),
        'contexto': cargar_contexto_territorial(),
        'memoria': cargar_memoria_temporal(),
        'operativa': cargar_operativa_material()
    }
    return datos
