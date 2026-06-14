"""
Tests de integración: datos reales (La Esperanza, Bajo Atrato) -> adaptador -> motor.

Comprueban que el puente datos->motor (informe §3) funciona end-to-end y produce
el gradiente esperado: Fase 1 BLOCKED (ICI), Fases 2-3 CONDITIONAL (pobreza).
"""
from pathlib import Path

import pytest

from utils import data_loader as dl
from utils.calculations import calcular_micro_red

UPLOADS = Path(__file__).resolve().parent.parent / "data" / "uploads"
pytestmark = pytest.mark.skipif(
    not UPLOADS.exists(), reason="sin datos en data/uploads"
)


def _datos():
    return {
        "dimensiones": dl._parse_dimensiones(UPLOADS / "DIMENSIONES_COGNITIVAS.xlsx"),
        "contexto": dl._parse_contexto(UPLOADS / "CONTEXTO_TERRITORIAL.xlsx"),
        "operativa": dl._parse_operativa(UPLOADS / "OPERATIVA_MATERIAL.xlsx"),
        "memoria": dl._parse_memoria(UPLOADS / "MEMORIA_TEMPORAL.xlsx"),
        "panel_0": dl._parse_panel0(UPLOADS / "PANEL_0_PROTAGONISTAS.xlsx"),
    }


def test_parseo_dimensiones_resuelve_la_fila_de_titulo():
    d = dl._parse_dimensiones(UPLOADS / "DIMENSIONES_COGNITIVAS.xlsx")
    assert d is not None
    assert {"IA", "ICI", "IVC"}.issubset(set(d.index))
    assert d.loc["ICI", "Fase_1"] == 28  # bloqueo principal del caso


def test_parseo_contexto_largo_e_iom_precalculado():
    ctx = dl._parse_contexto(UPLOADS / "CONTEXTO_TERRITORIAL.xlsx")
    assert ctx["pobreza_multidimensional"] == 67
    op = dl._parse_operativa(UPLOADS / "OPERATIVA_MATERIAL.xlsx")
    assert op["IOM"] == 44


def test_fase1_blocked_por_ici():
    r = calcular_micro_red("Comunidad Local", 1, "A", _datos())
    assert r["estado_gate"] == "blocked"
    assert "ICI" in r["justificacion_gate"]
    assert r["citas"]  # arrastra fundamento bibliográfico


def test_fases_2_y_3_conditional_por_pobreza():
    datos = _datos()
    for fase in (2, 3):
        r = calcular_micro_red("Comunidad Local", fase, "A", datos)
        assert r["estado_gate"] == "conditional"


def test_sin_datos_nunca_habilita():
    vacio = {"dimensiones": None, "contexto": {}, "operativa": None,
             "memoria": None, "panel_0": None}
    r = calcular_micro_red("Comunidad Local", 1, "A", vacio)
    assert r["estado_gate"] == "datos_insuficientes"
    assert r["estado_gate"] != "enabled"
    assert r["nivel_confianza"] <= 30
