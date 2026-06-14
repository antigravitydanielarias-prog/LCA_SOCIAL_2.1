"""Modelo S-LCA 2.0 — motor de Python puro (agnóstico a la interfaz)."""

from .gates import (
    EstadoGate,
    ResultadoGate,
    evaluar_gate,
    UMBRALES,
    DIMENSIONES_COGNITIVAS,
)
from .referencias import REFERENCIAS, citar, por_componente

__all__ = [
    "EstadoGate",
    "ResultadoGate",
    "evaluar_gate",
    "UMBRALES",
    "DIMENSIONES_COGNITIVAS",
    "REFERENCIAS",
    "citar",
    "por_componente",
]
