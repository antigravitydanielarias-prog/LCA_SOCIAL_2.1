"""
Tests del NÚCLEO de decisión (`modelo_slca.gates`).

Verifican el contrato nuevo: estados, citas y —sobre todo— que la ausencia de
datos NUNCA produzca ENABLED (corrección del bug crítico del informe §3/§6.3).
"""
from modelo_slca import evaluar_gate, EstadoGate, citar

# Caso base "todo bien" (las 8 dimensiones presentes y altas).
DIMS_OK = {"IA": 70, "IAT": 65, "ICI": 70, "IVC": 75,
           "IME": 62, "IIN": 60, "IPRA": 58, "ICS": 61}


def _completo(**cambios):
    d = dict(DIMS_OK)
    d.update(cambios)
    return d


def test_enabled_cuando_todo_cumple():
    r = evaluar_gate(_completo(), iom=70, contexto={"pobreza_multidimensional": 30})
    assert r.estado is EstadoGate.ENABLED
    assert r.puede_avanzar


def test_blocked_por_ici_bajo_con_cita():
    r = evaluar_gate(_completo(ICI=28), iom=70, contexto={"pobreza_multidimensional": 30})
    assert r.estado is EstadoGate.BLOCKED
    assert "ICI" in r.justificacion
    assert "wustenhagen_2007" in r.citas


def test_blocked_por_iom_bajo():
    r = evaluar_gate(_completo(), iom=20, contexto={"pobreza_multidimensional": 30})
    assert r.estado is EstadoGate.BLOCKED
    assert not r.puede_avanzar


def test_blocked_por_dimension_critica():
    r = evaluar_gate(_completo(IME=20), iom=70, contexto={"pobreza_multidimensional": 30})
    assert r.estado is EstadoGate.BLOCKED


def test_conditional_por_pobreza_alta_con_cita():
    r = evaluar_gate(_completo(), iom=70, contexto={"pobreza_multidimensional": 67})
    assert r.estado is EstadoGate.CONDITIONAL
    assert r.puede_avanzar
    assert "alkire_foster_2011" in r.citas


def test_datos_insuficientes_no_es_enabled():
    """Regresión del bug: faltan dimensiones e IOM -> NO habilitado."""
    r = evaluar_gate({"IA": 70, "IVC": 80}, iom=None, contexto={})
    assert r.estado is EstadoGate.DATOS_INSUFICIENTES
    assert r.estado is not EstadoGate.ENABLED
    assert not r.puede_avanzar
    assert any("ICI" in f for f in r.datos_faltantes)
    assert "IOM" in r.datos_faltantes


def test_iom_faltante_bloquea_precautoriamente():
    r = evaluar_gate(_completo(), iom=None, contexto={"pobreza_multidimensional": 30})
    assert r.estado is EstadoGate.DATOS_INSUFICIENTES


def test_valores_altos_no_compensan_datos_faltantes():
    """Aunque lo presente sea altísimo, faltar un requerido bloquea."""
    r = evaluar_gate({"IA": 99}, iom=99, contexto={})
    assert r.estado is EstadoGate.DATOS_INSUFICIENTES


def test_citas_se_formatean():
    assert "Wüstenhagen" in citar("wustenhagen_2007")
    assert "Alkire" in citar("alkire_foster_2011")
