"""
Adaptador del Modelo S-LCA 2.x
==============================

Capa intermedia entre los datos (estructuras de `data_loader`) y el NÚCLEO de
decisión `modelo_slca` (gates.py). Su único trabajo:

  1. Extraer, para un (actor, fase, subcapa), los indicadores que el motor espera.
  2. Llamar a `evaluar_gate` -> ÚNICA fuente de verdad de la lógica de gates.
  3. Mapear el `ResultadoGate` (limpio y citable) al diccionario rico que
     consumen las páginas Streamlit y los visualizadores.

No contiene la lógica de umbrales (vive en `modelo_slca`) ni I/O de Excel
(vive en `data_loader`). Sin dependencias de Streamlit -> testeable directamente.

Corrige los dos bugs del prototipo (informe §3):
  * El crash de `estimar_confianza` (iteraba las claves del dict, no los valores).
  * "Datos faltantes = aprobado": ahora lo decide el motor (DATOS_INSUFICIENTES).
"""
from datetime import datetime
import json

import pandas as pd

from config import DIMENSIONES, ACTORES
from modelo_slca import evaluar_gate, DIMENSIONES_COGNITIVAS

# Etiqueta legible por estado (incluye el estado precautorio).
ESTADO_LABEL = {
    "blocked": "❌ BLOQUEADO",
    "conditional": "⚠️ CONDICIONAL",
    "enabled": "✅ HABILITADO",
    "datos_insuficientes": "🚫 DATOS INSUFICIENTES",
}

# Costos base por actor (USD) para la estimación de transición.
_COSTOS_ACTOR = {
    "Comunidad Local": 30000,
    "Gobierno Local": 15000,
    "Proveedores Técnicos": 20000,
    "Actores Económicos": 12000,
    "Actores Externos": 10000,
}


# ----------------------------------------------------------------------------
# Extracción de indicadores desde los datos cargados
# ----------------------------------------------------------------------------
def _dimensiones_para_fase(df_dim, fase):
    """{dim: valor|None} a partir del DataFrame tidy de dimensiones."""
    if df_dim is None:
        return {d: None for d in DIMENSIONES_COGNITIVAS}
    col = f"Fase_{fase}"
    out = {}
    for dim in DIMENSIONES_COGNITIVAS:
        valor = None
        if col in getattr(df_dim, "columns", []) and dim in df_dim.index:
            v = df_dim.loc[dim, col]
            valor = None if pd.isna(v) else float(v)
        out[dim] = valor
    return out


def _tendencia(df_dim, dim, fase):
    """Flecha de tendencia comparando la fase con la siguiente disponible."""
    if df_dim is None or dim not in getattr(df_dim, "index", []):
        return "→"
    actual = df_dim.loc[dim].get(f"Fase_{fase}")
    siguiente = df_dim.loc[dim].get(f"Fase_{min(fase + 1, 3)}")
    if pd.isna(actual) or pd.isna(siguiente) or actual == siguiente:
        return "→"
    return "↑" if siguiente > actual else "↓"


def _memoria_dict(df_mem):
    """DataFrame de serie temporal -> dict {fechas, IA, IAT, ...} (últimos 12)."""
    if df_mem is None or getattr(df_mem, "empty", True):
        return {}
    mem = {}
    col_fecha = next((c for c in df_mem.columns if str(c).strip().lower() == "fecha"), None)
    if col_fecha is not None:
        mem["fechas"] = df_mem[col_fecha].tail(12).astype(str).tolist()
    for dim in DIMENSIONES_COGNITIVAS:
        if dim in df_mem.columns:
            mem[dim] = pd.to_numeric(df_mem[dim], errors="coerce").tail(12).tolist()
    return mem


def _datos_faltantes_legibles(faltantes):
    """Convierte ['dimension:ICI', 'IOM'] -> textos amigables."""
    legibles = []
    for f in faltantes:
        if f.startswith("dimension:"):
            cod = f.split(":", 1)[1]
            legibles.append(f"Dimensión {cod} ({DIMENSIONES.get(cod, cod)})")
        elif f == "IOM":
            legibles.append("IOM (operativa-material)")
        else:
            legibles.append(f)
    return legibles


# ----------------------------------------------------------------------------
# Orquestación principal
# ----------------------------------------------------------------------------
def calcular_micro_red(actor, fase, subcapa, datos):
    """
    Calcula la micro-red (actor × fase × subcapa) y devuelve el diagnóstico
    completo. La decisión de gate la toma SIEMPRE el motor `modelo_slca`.
    """
    if actor not in ACTORES:
        raise ValueError(f"Actor inválido: {actor}")
    fase = int(fase)
    if fase not in (1, 2, 3):
        raise ValueError(f"Fase inválida: {fase}")
    if subcapa not in ("A", "B", "C"):
        raise ValueError(f"Subcapa inválida: {subcapa}")

    df_dim = datos.get("dimensiones")
    dims_fase = _dimensiones_para_fase(df_dim, fase)
    iom = (datos.get("operativa") or {}).get("IOM")
    contexto = datos.get("contexto") or {}

    # >>> NÚCLEO: una sola llamada al motor citable (precautorio ante faltantes).
    veredicto = evaluar_gate(dims_fase, iom, contexto)
    estado = veredicto.estado.value

    # Vista por dimensión para UI / visualizadores.
    dim_cog = {}
    for dim, valor in dims_fase.items():
        dim_cog[dim] = {
            "valor": valor if valor is not None else 0,
            "estado": clasificar_estado(valor),
            "tendencia": _tendencia(df_dim, dim, fase),
            "proyeccion_3m": valor if valor is not None else 0,
        }

    resultado = {
        "metadata": {
            "actor": actor,
            "fase": str(fase),
            "subcapa": subcapa,
            "fecha_analisis": datetime.now().isoformat(),
            "version_modelo": "2.1",
        },
        "dimensiones_cognitivas": dim_cog,
        "dimension_operativa_material": {"IOM": iom if iom is not None else 0},
        "contexto_territorial": contexto,
        "memoria_temporal": _memoria_dict(datos.get("memoria")),
        "estado_gate": estado,
        "estado_label": ESTADO_LABEL.get(estado, estado),
        "motivo_gate": veredicto.motivo,
        "justificacion_gate": veredicto.justificacion_con_citas(),
        "citas": list(veredicto.citas),
        "puede_avanzar": veredicto.puede_avanzar,
        "datos_faltantes": _datos_faltantes_legibles(veredicto.datos_faltantes),
        "barreras": identificar_barreras(dim_cog),
        "activos": identificar_activos(dim_cog),
        "recomendaciones": generar_recomendaciones(actor, fase, subcapa, dim_cog, veredicto),
        "costo_transicion": calcular_costo_transicion(actor, fase, subcapa, estado),
        "nivel_confianza": 0,
    }
    resultado["nivel_confianza"] = estimar_confianza(resultado)
    resultado["diagnostico"] = generar_diagnostico(resultado)
    return resultado


# ----------------------------------------------------------------------------
# Diagnóstico de apoyo (barreras, activos, costos, narrativa)
# ----------------------------------------------------------------------------
def clasificar_estado(valor):
    """Clasifica un indicador 0-100 en una banda cualitativa."""
    if valor is None:
        return "desconocido"
    if valor < 25:
        return "crítico"
    if valor < 40:
        return "bajo"
    if valor < 60:
        return "moderado"
    if valor < 80:
        return "fuerte"
    return "muy_fuerte"


def identificar_barreras(dimensiones):
    """Dimensiones por debajo de su umbral -> barreras ordenadas por severidad."""
    umbrales = {"IA": 40, "IAT": 40, "ICI": 40, "IVC": 50,
                "IME": 40, "IIN": 40, "IPRA": 40, "ICS": 40}
    barreras = []
    for dim, umbral in umbrales.items():
        valor = dimensiones.get(dim, {}).get("valor", 100)
        if valor < umbral:
            severidad = "crítica" if valor < 25 else ("moderada" if valor < 40 else "leve")
            barreras.append({
                "nombre": f"{dim} - {DIMENSIONES.get(dim, dim)}",
                "dimensión": dim,
                "valor": valor,
                "severidad": severidad,
            })
    return sorted(barreras, key=lambda x: x["valor"])


def identificar_activos(dimensiones):
    """Dimensiones altas -> activos ordenados de mayor a menor."""
    umbrales = {"IA": 60, "IAT": 60, "ICI": 60, "IVC": 70,
                "IME": 60, "IIN": 60, "IPRA": 60, "ICS": 60}
    activos = []
    for dim, umbral in umbrales.items():
        valor = dimensiones.get(dim, {}).get("valor", 0)
        if valor >= umbral:
            activos.append({
                "nombre": f"{dim} - {DIMENSIONES.get(dim, dim)}",
                "dimensión": dim,
                "valor": valor,
                "potencial": "altísimo" if valor >= 80 else "alto",
            })
    return sorted(activos, key=lambda x: x["valor"], reverse=True)


def generar_recomendaciones(actor, fase, subcapa, dimensiones, veredicto):
    """Recomendaciones priorizadas según el veredicto del motor."""
    recomendaciones = []
    estado = veredicto.estado.value

    if estado == "datos_insuficientes":
        recomendaciones.append({
            "orden": 1,
            "prioridad": "CRÍTICA",
            "accion": "Completar la recolección de datos antes de decidir "
                      "(la ausencia de evidencia no habilita la transición).",
            "plazo": "Inmediato",
        })
        return recomendaciones

    if estado == "blocked":
        recomendaciones.append({
            "orden": 1,
            "prioridad": "CRÍTICA",
            "accion": f"Resolver el bloqueo antes de avanzar a Fase {fase} Subcapa {subcapa}.",
            "plazo": "Inmediato",
        })

    for dim in ("ICI", "IAT", "IME"):
        valor = dimensiones.get(dim, {}).get("valor", 100)
        if valor < 40:
            recomendaciones.append({
                "orden": len(recomendaciones) + 1,
                "prioridad": "ALTA" if valor < 25 else "MEDIA",
                "accion": f"Invertir en {DIMENSIONES.get(dim, dim)} (actual {valor:.0f}/100).",
                "plazo": "2-6 meses",
            })
    return recomendaciones


def calcular_costo_transicion(actor, fase, subcapa, estado):
    """Costo estimado según actor y estado de gate."""
    if estado == "datos_insuficientes":
        return {
            "costo_directo": "N/D",
            "contingencia_25pct": "N/D",
            "total_presupuesto": "N/D",
            "tiempo": "—",
            "estado_gate": estado,
            "nota": "Costo no estimable sin datos completos.",
        }

    costo_base = _COSTOS_ACTOR.get(actor, 15000)
    multiplicador = {"blocked": 2.5, "conditional": 1.5, "enabled": 1.0}.get(estado, 1.0)
    costo_total = costo_base * multiplicador
    return {
        "costo_directo": f"${costo_total:,.0f}",
        "contingencia_25pct": f"${costo_total * 0.25:,.0f}",
        "total_presupuesto": f"${costo_total * 1.25:,.0f}",
        "tiempo": "3-9 meses" if estado == "blocked" else "2-3 meses",
        "estado_gate": estado,
    }


def estimar_confianza(resultado):
    """
    Nivel de confianza 0-100 del análisis. (Aquí estaba el crash del prototipo:
    iteraba las CLAVES del dict en vez de los VALORES.)
    """
    confianza = 70
    confianza -= len(resultado["datos_faltantes"]) * 10
    dims = resultado["dimensiones_cognitivas"]
    disponibles = len([d for d in dims.values() if d["valor"] > 0])
    confianza += (disponibles / len(DIMENSIONES_COGNITIVAS)) * 20
    if resultado["estado_gate"] == "datos_insuficientes":
        confianza = min(confianza, 30)
    return int(max(0, min(100, confianza)))


def generar_diagnostico(resultado):
    """Diagnóstico narrativo corto."""
    dims = resultado["dimensiones_cognitivas"]
    ici = dims.get("ICI", {}).get("valor", 0)
    ivc = dims.get("IVC", {}).get("valor", 0)
    ia = dims.get("IA", {}).get("valor", 0)
    m = resultado["metadata"]
    fuerza_ici = "CRÍTICA" if ici < 40 else ("MODERADA" if ici < 60 else "FUERTE")
    return (
        f"El {m['actor']} en Fase {m['fase']} Subcapa {m['subcapa']} presenta: "
        f"Confianza institucional {ici:.0f}/100 ({fuerza_ici}), "
        f"Identidad cultural {ivc:.0f}/100, Aspiraciones {ia:.0f}/100. "
        f"Estado de gate: {resultado['estado_label']}. "
        f"{resultado['justificacion_gate']}"
    )


def exportar_json(resultado):
    """Serializa el resultado a JSON formateado."""
    return json.dumps(resultado, indent=2, ensure_ascii=False, default=str)
