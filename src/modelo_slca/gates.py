"""
gates.py — Motor de decisión de gates del Modelo S-LCA 2.0
==========================================================

Núcleo de Python puro (sin dependencias de UI). Recibe los indicadores de
una micro-red y devuelve un veredicto estructurado y CITABLE.

Corrige el bug crítico del prototipo original (informe §3 y §6.3):
    En el código anterior, una dimensión ausente caía en `valor = 0` o se
    saltaba, y la lógica podía devolver ENABLED sin evidencia. Aquí la
    ausencia de datos NUNCA produce ENABLED. Por principio de precaución
    (Steel, 2015), faltar evidencia bloquea con motivo 'datos_insuficientes',
    que es distinto de un bloqueo por barrera real.

Cada umbral arrastra su justificación bibliográfica (ver referencias.py),
cerrando el hueco §6.1 (umbrales heurísticos -> umbrales fundamentados).
"""

from dataclasses import dataclass, field
from enum import Enum

try:
    from .referencias import citar
except ImportError:  # permite ejecutar el archivo de forma suelta
    from referencias import citar


# Las 8 dimensiones cognitivas que el motor espera evaluar.
DIMENSIONES_COGNITIVAS = ("IA", "IAT", "ICI", "IVC", "IME", "IIN", "IPRA", "ICS")


class EstadoGate(str, Enum):
    BLOCKED = "blocked"
    CONDITIONAL = "conditional"
    ENABLED = "enabled"
    # Nuevo estado explícito: no se puede concluir por falta de datos.
    # Se trata como bloqueante (precautorio) pero se rotula aparte para no
    # confundirlo con una barrera real del territorio.
    DATOS_INSUFICIENTES = "datos_insuficientes"


@dataclass(frozen=True)
class Umbral:
    valor: float
    cita: str          # id en referencias.py
    descripcion: str


# Umbrales del modelo, cada uno anclado a su referencia.
UMBRALES: dict[str, Umbral] = {
    "ICI_MINIMO": Umbral(
        40, "wustenhagen_2007",
        "Confianza institucional mínima para participación genuina."),
    "IOM_MINIMO": Umbral(
        30, "geels_2011",
        "Capacidad operativa-material mínima (régimen socio-técnico)."),
    "DIMENSION_CRITICA": Umbral(
        25, "plested_2006",
        "Toda dimensión debe superar el piso crítico antes de avanzar."),
    "POBREZA_ALTO_RIESGO": Umbral(
        50, "alkire_foster_2011",
        "Corte de privación que activa condiciones especiales (doble corte)."),
}


@dataclass
class ResultadoGate:
    estado: EstadoGate
    motivo: str                       # 'datos_insuficientes' | 'barrera' | 'ok'
    justificacion: str
    citas: list[str] = field(default_factory=list)   # ids de referencias
    datos_faltantes: list[str] = field(default_factory=list)

    @property
    def puede_avanzar(self) -> bool:
        return self.estado in (EstadoGate.ENABLED, EstadoGate.CONDITIONAL)

    def justificacion_con_citas(self) -> str:
        if not self.citas:
            return self.justificacion
        refs = "; ".join(citar(c) for c in self.citas)
        return f"{self.justificacion}  [Fundamento: {refs}]"


def _valor(indicador) -> float | None:
    """Normaliza una entrada que puede venir como número, None o dict."""
    if indicador is None:
        return None
    if isinstance(indicador, dict):
        indicador = indicador.get("valor")
    if indicador is None:
        return None
    try:
        return float(indicador)
    except (TypeError, ValueError):
        return None


def evaluar_gate(
    dimensiones: dict,
    iom,
    contexto: dict | None = None,
    requeridas: tuple[str, ...] = DIMENSIONES_COGNITIVAS,
) -> ResultadoGate:
    """
    Evalúa el estado del gate para una micro-red.

    dimensiones : dict como {'ICI': 28, 'IA': {'valor': 45}, ...}
    iom         : número | dict | None  (índice operativa-material)
    contexto    : dict con 'pobreza_multidimensional', etc.
    requeridas  : dimensiones que DEBEN existir para poder concluir.

    Regla de oro: si falta algún dato requerido, el gate NO puede devolver
    ENABLED. Devuelve DATOS_INSUFICIENTES (bloqueante, precautorio).
    """
    contexto = contexto or {}

    # ----- 1. Chequeo de completitud (principio de precaución) -----------
    faltantes: list[str] = []
    for dim in requeridas:
        if _valor(dimensiones.get(dim)) is None:
            faltantes.append(f"dimension:{dim}")
    if _valor(iom) is None:
        faltantes.append("IOM")

    if faltantes:
        return ResultadoGate(
            estado=EstadoGate.DATOS_INSUFICIENTES,
            motivo="datos_insuficientes",
            justificacion=(
                "No se puede habilitar la transición: faltan datos requeridos. "
                "La ausencia de evidencia no equivale a aprobación."),
            citas=["steel_2015"],
            datos_faltantes=faltantes,
        )

    # A partir de aquí todos los valores requeridos existen.
    ici = _valor(dimensiones.get("ICI"))
    iom_val = _valor(iom)
    pobreza = _valor(contexto.get("pobreza_multidimensional")) or 0.0

    # ----- 2. Reglas de BLOQUEO por barrera real -------------------------
    if ici < UMBRALES["ICI_MINIMO"].valor:
        u = UMBRALES["ICI_MINIMO"]
        return ResultadoGate(
            EstadoGate.BLOCKED, "barrera",
            f"ICI={ici:.0f} < {u.valor:.0f} (confianza institucional crítica).",
            citas=[u.cita, "edwards_2000"],
        )

    if iom_val < UMBRALES["IOM_MINIMO"].valor:
        u = UMBRALES["IOM_MINIMO"]
        return ResultadoGate(
            EstadoGate.BLOCKED, "barrera",
            f"IOM={iom_val:.0f} < {u.valor:.0f} (capacidad material insuficiente).",
            citas=[u.cita, "koirala_2016"],
        )

    critico = UMBRALES["DIMENSION_CRITICA"].valor
    for dim in requeridas:
        v = _valor(dimensiones.get(dim))
        if v < critico:
            return ResultadoGate(
                EstadoGate.BLOCKED, "barrera",
                f"{dim}={v:.0f} < {critico:.0f} (dimensión bajo el piso crítico).",
                citas=[UMBRALES["DIMENSION_CRITICA"].cita],
            )

    # ----- 3. Regla CONDICIONAL ------------------------------------------
    if pobreza > UMBRALES["POBREZA_ALTO_RIESGO"].valor:
        u = UMBRALES["POBREZA_ALTO_RIESGO"]
        return ResultadoGate(
            EstadoGate.CONDITIONAL, "barrera",
            f"Pobreza multidimensional={pobreza:.0f}% > {u.valor:.0f}%: "
            f"proceder con condiciones especiales.",
            citas=[u.cita],
        )

    # ----- 4. ENABLED ----------------------------------------------------
    return ResultadoGate(
        EstadoGate.ENABLED, "ok",
        "Todas las condiciones evaluables se cumplen. Proceder; mantener "
        "monitoreo de la trayectoria temporal.",
        citas=["plested_2006"],
    )


if __name__ == "__main__":
    # Demostración: el caso 'Comunidad 1A' del informe y el caso del bug.
    comunidad_1a = {
        "IA": 45, "IAT": 38, "ICI": 28, "IVC": 72,
        "IME": 32, "IIN": 55, "IPRA": 41, "ICS": 38,
    }
    r = evaluar_gate(comunidad_1a, iom=42, contexto={"pobreza_multidimensional": 67})
    print("Comunidad 1A  ->", r.estado.value, "|", r.motivo)
    print("  ", r.justificacion_con_citas(), "\n")

    # El bug original: datos incompletos. Antes -> ENABLED. Ahora -> bloqueo.
    incompletos = {"IA": 70, "IVC": 80}  # faltan ICI, IOM, etc.
    r2 = evaluar_gate(incompletos, iom=None, contexto={})
    print("Datos incompletos ->", r2.estado.value, "|", r2.motivo)
    print("   faltantes:", r2.datos_faltantes)
    print("  ", r2.justificacion_con_citas())
