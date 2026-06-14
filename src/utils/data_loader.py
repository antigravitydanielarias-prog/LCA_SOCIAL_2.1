"""
Carga y normalización de datos desde Excel para el Modelo S-LCA 2.x.

Los archivos reales (carpeta `EXCELS DE CARGA`, copiados a `data/uploads`) traen
particularidades que el prototipo no manejaba y que rompían el puente datos->motor
(informe §3, "los datos no se conectan al motor"):

  - Hojas con una FILA DE TÍTULO antes del encabezado real.
  - Contexto territorial en formato LARGO (Indicador | Valor), no ancho.
  - IOM ya calculado dentro de la hoja de operativa-material.

Aquí se detecta el encabezado y se devuelve una estructura limpia y estable, de
modo que `calculations.py` solo tenga que llamar al motor `modelo_slca`.

El parseo pesado vive en funciones puras `_parse_*` (testeables sin Streamlit);
las funciones `cargar_*` son envoltorios cacheados para la app.
"""
import unicodedata
from pathlib import Path

import pandas as pd
import streamlit as st

from config import UPLOADS_DIR, TEMPLATES_DIR

DIMENSIONES_COG = ("IA", "IAT", "ICI", "IVC", "IME", "IIN", "IPRA", "ICS")

# Indicador (nombre normalizado en el Excel) -> clave canónica del motor / UI.
_CONTEXTO_ALIAS = {
    "pobreza multidimensional": "pobreza_multidimensional",
    "informalidad": "informalidad",
    "educacion promedio": "educacion_promedio",
    "acceso internet": "acceso_internet",
    "desempleo juvenil": "tasa_desempleo_juvenil",
    "participacion ciudadana": "participacion_ciudadana",
}

ARCHIVOS_REQUERIDOS = {
    "panel_0": "PANEL_0_PROTAGONISTAS.xlsx",
    "dimensiones": "DIMENSIONES_COGNITIVAS.xlsx",
    "contexto": "CONTEXTO_TERRITORIAL.xlsx",
    "memoria": "MEMORIA_TEMPORAL.xlsx",
    "operativa": "OPERATIVA_MATERIAL.xlsx",
}


# ----------------------------------------------------------------------------
# Utilidades de parseo (puras)
# ----------------------------------------------------------------------------
def _norm(texto) -> str:
    """Minúsculas, sin acentos, espacios colapsados — para comparar etiquetas."""
    if texto is None:
        return ""
    s = unicodedata.normalize("NFKD", str(texto))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(s.lower().split())


def _to_float(valor):
    """Convierte a float; devuelve None si no es numérico o es NaN."""
    try:
        if valor is None:
            return None
        if isinstance(valor, float) and pd.isna(valor):
            return None
        return float(valor)
    except (TypeError, ValueError):
        return None


def _find_header_row(raw: pd.DataFrame, claves) -> int:
    """
    Índice de la primera fila cuya celda COINCIDA con alguna clave.

    Se exige coincidencia a nivel de palabra (igualdad o `clave + ' '`) para no
    confundir el encabezado real ('Dimensión') con una fila de título
    ('DIMENSIONES COGNITIVAS', donde 'dimension' aparece como subcadena).
    """
    claves_norm = [_norm(k) for k in claves]
    for i in range(min(len(raw), 8)):
        for v in raw.iloc[i].tolist():
            celda = _norm(v)
            if not celda:
                continue
            if any(celda == k or celda.startswith(k + " ") for k in claves_norm):
                return i
    return 0


def _leer_con_encabezado(path, sheet, claves) -> pd.DataFrame:
    """Lee una hoja detectando automáticamente la fila de encabezado real."""
    raw = pd.read_excel(path, sheet_name=sheet, header=None)
    h = _find_header_row(raw, claves)
    return pd.read_excel(path, sheet_name=sheet, header=h)


# ----------------------------------------------------------------------------
# Parsers puros por archivo
# ----------------------------------------------------------------------------
def _parse_dimensiones(path) -> pd.DataFrame | None:
    """
    DataFrame índice=dimensión (IA, IAT, ...), columnas Fase_1/Fase_2/Fase_3
    (+ Nombre). Tolera la fila de título y los encabezados con salto de línea
    ('Fase 1\\nPreparación').
    """
    df = _leer_con_encabezado(path, "RESUMEN", ["dimension", "dimensión"])
    col_dim = col_nombre = None
    fase_cols = {}
    for c in df.columns:
        n = _norm(c)
        if col_dim is None and n.startswith("dimension"):
            col_dim = c
        elif n.startswith("fase 1") or n == "fase_1":
            fase_cols[1] = c
        elif n.startswith("fase 2") or n == "fase_2":
            fase_cols[2] = c
        elif n.startswith("fase 3") or n == "fase_3":
            fase_cols[3] = c
        elif col_nombre is None and "nombre" in n:
            col_nombre = c
    if col_dim is None or not fase_cols:
        return None

    filas = {}
    for _, row in df.iterrows():
        dim = str(row[col_dim]).strip()
        if dim not in DIMENSIONES_COG:
            continue
        filas[dim] = {
            "Fase_1": _to_float(row.get(fase_cols.get(1))),
            "Fase_2": _to_float(row.get(fase_cols.get(2))),
            "Fase_3": _to_float(row.get(fase_cols.get(3))),
            "Nombre": str(row[col_nombre]) if col_nombre else dim,
        }
    if not filas:
        return None
    out = pd.DataFrame.from_dict(filas, orient="index")
    out.index.name = "Dimension"
    return out


def _parse_contexto(path) -> dict | None:
    """Contexto territorial en formato largo -> dict {clave_canonica: valor}."""
    df = _leer_con_encabezado(path, "INDICADORES_DANE", ["indicador", "valor"])
    col_ind = col_val = col_nombre = None
    for c in df.columns:
        n = _norm(c)
        if n == "indicador":
            col_ind = c
        elif n == "valor":
            col_val = c
        elif n == "nombre":
            col_nombre = c
    if col_val is None:
        return None

    ctx = {}
    for _, row in df.iterrows():
        etiqueta = _norm(row.get(col_ind) if col_ind is not None else None) \
            or _norm(row.get(col_nombre) if col_nombre is not None else None)
        valor = _to_float(row.get(col_val))
        if valor is None or not etiqueta:
            continue
        for alias, canon in _CONTEXTO_ALIAS.items():
            if alias in etiqueta:
                ctx[canon] = valor
                break
    return ctx or None


def _iom_desde_estado(raw: pd.DataFrame):
    """Fallback: estima IOM (0-100) a partir de los 'Estado' del inventario."""
    pesos = {"funciona": 1.0, "parcial": 0.5, "regular": 0.5, "sin instalar": 0.0}
    valores = [pesos[_norm(v)] for row in raw.itertuples(index=False)
               for v in row if _norm(v) in pesos]
    if not valores:
        return None
    return round(sum(valores) / len(valores) * 100, 1)


def _parse_operativa(path) -> dict | None:
    """
    Operativa-material -> {'IOM': float|None}. Prefiere el IOM ya calculado en
    la hoja (celda contigua a 'IOM Calculado'); si no, lo deriva de los estados.
    """
    raw = pd.read_excel(path, sheet_name="INFRAESTRUCTURA", header=None)
    iom = None
    for row in raw.itertuples(index=False):
        celdas = list(row)
        if any("iom calculado" in _norm(v) for v in celdas):
            for v in celdas:
                f = _to_float(v)
                if f is not None:
                    iom = f
                    break
            if iom is not None:
                break
    if iom is None:
        iom = _iom_desde_estado(raw)
    return {"IOM": iom}


def _parse_memoria(path) -> pd.DataFrame | None:
    """Serie temporal de 12 meses (Fecha + 8 dimensiones + Eventos)."""
    df = _leer_con_encabezado(path, "SERIE_TEMPORAL_12M", ["fecha"])
    return df if not df.empty else None


def _parse_panel0(path) -> pd.DataFrame | None:
    """Panel 0 de protagonistas (5 actores con readiness y alertas)."""
    df = _leer_con_encabezado(path, "PROTAGONISTAS_READINESS", ["actor"])
    return df if not df.empty else None


# ----------------------------------------------------------------------------
# Envoltorios cacheados (capa de aplicación / Streamlit)
# ----------------------------------------------------------------------------
def _ruta(nombre, filepath):
    return Path(filepath) if filepath is not None else UPLOADS_DIR / ARCHIVOS_REQUERIDOS[nombre]


def _cargar(nombre, parser, filepath, etiqueta):
    p = _ruta(nombre, filepath)
    if not Path(p).exists():
        return None
    try:
        return parser(p)
    except Exception as e:  # noqa: BLE001 - la UI muestra el error y sigue
        st.error(f"Error cargando {etiqueta}: {e}")
        return None


@st.cache_data(show_spinner=False)
def cargar_panel_0(filepath=None):
    """Panel 0 (Protagonistas) -> DataFrame."""
    return _cargar("panel_0", _parse_panel0, filepath, "Panel 0")


@st.cache_data(show_spinner=False)
def cargar_dimensiones_cognitivas(filepath=None):
    """Dimensiones cognitivas -> DataFrame tidy (índice=dimensión, Fase_1..3)."""
    return _cargar("dimensiones", _parse_dimensiones, filepath, "dimensiones")


@st.cache_data(show_spinner=False)
def cargar_contexto_territorial(filepath=None):
    """Contexto territorial -> dict {clave_canonica: valor}."""
    return _cargar("contexto", _parse_contexto, filepath, "contexto territorial")


@st.cache_data(show_spinner=False)
def cargar_memoria_temporal(filepath=None):
    """Memoria temporal -> DataFrame (12 meses)."""
    return _cargar("memoria", _parse_memoria, filepath, "memoria temporal")


@st.cache_data(show_spinner=False)
def cargar_operativa_material(filepath=None):
    """Operativa-material -> dict {'IOM': valor}."""
    return _cargar("operativa", _parse_operativa, filepath, "operativa-material")


def validar_carga_datos():
    """Valida que los 5 archivos requeridos existan en uploads."""
    faltantes = [nombre for nombre in ARCHIVOS_REQUERIDOS.values()
                 if not (UPLOADS_DIR / nombre).exists()]
    return len(faltantes) == 0, faltantes


def descargar_templates():
    """Rutas de las plantillas Excel disponibles."""
    return {clave: TEMPLATES_DIR / nombre for clave, nombre in ARCHIVOS_REQUERIDOS.items()}


def cargar_todos_datos():
    """Carga consolidada para el adaptador (claves estables)."""
    return {
        "panel_0": cargar_panel_0(),
        "dimensiones": cargar_dimensiones_cognitivas(),
        "contexto": cargar_contexto_territorial(),
        "memoria": cargar_memoria_temporal(),
        "operativa": cargar_operativa_material(),
    }
