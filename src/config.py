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

# Umbrales de Gates.
# FUENTE ÚNICA DE VERDAD: el motor `modelo_slca.gates.UMBRALES` (cada umbral
# arrastra su justificación bibliográfica). Aquí solo se reexponen como dict
# plano para la UI; si el motor no estuviera disponible, se usan los literales.
try:
    from modelo_slca.gates import UMBRALES as _UMBRALES
    GATE_THRESHOLDS = {k: _UMBRALES[k].valor for k in (
        'ICI_MINIMO', 'IOM_MINIMO', 'DIMENSION_CRITICA', 'POBREZA_ALTO_RIESGO'
    )}
except Exception:  # pragma: no cover - fallback defensivo
    GATE_THRESHOLDS = {
        'ICI_MINIMO': 40,        # Confianza institucional mínima
        'IOM_MINIMO': 30,        # Capacidad operativa-material mínima
        'DIMENSION_CRITICA': 25, # Piso crítico para cualquier dimensión
        'POBREZA_ALTO_RIESGO': 50,  # Activa condición especial
    }

# Estados de Gate (incluye el estado precautorio por datos faltantes)
GATE_STATES = {
    'blocked': '❌ BLOQUEADO',
    'conditional': '⚠️ CONDICIONAL',
    'enabled': '✅ HABILITADO',
    'datos_insuficientes': '🚫 DATOS INSUFICIENTES',
}

# Colores para visualizaciones
COLORS = {
    'blocked': '#d62728',
    'conditional': '#ff7f0e',
    'enabled': '#2ca02c',
    'datos_insuficientes': '#6c757d',
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
