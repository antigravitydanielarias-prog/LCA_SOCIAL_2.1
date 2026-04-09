"""
Configuración global del Modelo 2.0
"""
import os
from pathlib import Path

# Directorios
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
TEMPLATES_DIR = DATA_DIR / "templates"
UPLOADS_DIR = DATA_DIR / "uploads"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

# Crear directorios si no existen
for directory in [DATA_DIR, TEMPLATES_DIR, UPLOADS_DIR, OUTPUTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Configuración de dimensiones
DIMENSIONES = {
    'IA': 'Aspiraciones y expectativas',
    'IAT': 'Tecnología y apropiación',
    'ICI': 'Confianza institucional',
    'IVC': 'Identidad cultural',
    'IME': 'Mentalidad emprendedora',
    'IIN': 'Normas de género',
    'IPRA': 'Riesgo climático',
    'ICS': 'Consumo sostenible'
}

# Actores
ACTORES = [
    'Comunidad Local',
    'Gobierno Local',
    'Proveedores Técnicos',
    'Actores Económicos',
    'Actores Externos'
]

# Fases
FASES = {
    1: 'PREPARACIÓN',
    2: 'EJECUCIÓN',
    3: 'SOSTENIBILIDAD'
}

# Subcapas
SUBCAPAS = {
    'A': 'Reconocimiento',
    'B': 'Evaluación',
    'C': 'Alineación'
}

# Umbrales de Gates
GATE_THRESHOLDS = {
    'ICI_MINIMO': 40,  # Umbral mínimo de confianza institucional
    'IOM_MINIMO': 30,  # Umbral mínimo operativa-material
    'DIMENSION_CRITICA': 25,  # Umbral crítico para cualquier dimensión
    'POBREZA_ALTO_RIESGO': 50  # Umbral de pobreza que requiere condicionales
}

# Estados de Gate
GATE_STATES = {
    'blocked': '❌ BLOQUEADO',
    'conditional': '⚠️ CONDICIONAL',
    'enabled': '✅ HABILITADO'
}

# Colores para visualizaciones
COLORS = {
    'blocked': '#d62728',
    'conditional': '#ff7f0e',
    'enabled': '#2ca02c',
    'critico': '#d62728',
    'bajo': '#ff9999',
    'moderado': '#ffcc99',
    'fuerte': '#99cc99',
    'neutral': '#cccccc'
}

# Configuración de escala Likert
LIKERT_SCALE = {
    1: 'Muy en desacuerdo',
    2: 'En desacuerdo',
    3: 'Neutral',
    4: 'De acuerdo',
    5: 'Muy de acuerdo'
}

# Archivos Excel esperados
EXCEL_FILES = {
    'panel_0': 'PANEL_0_PROTAGONISTAS.xlsx',
    'dimensiones': 'DIMENSIONES_COGNITIVAS.xlsx',
    'contexto': 'CONTEXTO_TERRITORIAL.xlsx',
    'memoria': 'MEMORIA_TEMPORAL.xlsx',
    'operativa': 'OPERATIVA_MATERIAL.xlsx'
}
