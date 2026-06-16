"""
Dashboard - Visión General del Modelo 2.1

Gates por fase, readiness por actor y alertas, CALCULADOS a partir de los datos
cargados (ya no son valores fijos). La decisión de gate la toma el motor
`modelo_slca` vía `calcular_micro_red`.
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.data_loader import cargar_todos_datos, validar_carga_datos
from utils.calculations import calcular_micro_red
from utils.visualizers import crear_grafico_comparacion_actores, crear_gauge_readiness

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📊 Dashboard - Visión General")
st.markdown(
    "Estado de gates por fase, readiness por actor y alertas, calculados a "
    "partir de los datos cargados."
)
st.divider()

ok, faltantes = validar_carga_datos()
if not ok:
    st.warning(f"⚠️ Faltan archivos: {', '.join(faltantes)}")
    st.info("📥 Carga los archivos en ⚙️ Configuración para activar el dashboard.")
    st.stop()

datos = cargar_todos_datos()
panel = datos.get("panel_0")
ACTOR_PRINCIPAL = "Comunidad Local"

# --- Gates por fase (actor principal, subcapa A) --------------------------
st.subheader(f"🚪 Estado de Gates por Fase — {ACTOR_PRINCIPAL}")
resultados = {f: calcular_micro_red(ACTOR_PRINCIPAL, f, "A", datos) for f in (1, 2, 3)}

for col, f in zip(st.columns(3), (1, 2, 3)):
    r = resultados[f]
    estado = r["estado_gate"]
    with col:
        st.markdown(f"**Fase {f}**")
        if estado == "blocked":
            st.error(r["estado_label"])
        elif estado == "conditional":
            st.warning(r["estado_label"])
        elif estado == "datos_insuficientes":
            st.info(r["estado_label"])
        else:
            st.success(r["estado_label"])
        # Justificación sin la cola de citas (se ven completas en Micro-Red).
        st.caption(r["justificacion_gate"].split("[Fundamento")[0].strip())

st.divider()

# --- Readiness del actor principal (gauge real) ---------------------------
st.subheader("📊 Readiness Comunitaria")
actual = requerido = None
if panel is not None and not panel.empty and "Actor" in panel.columns:
    fila = panel[panel["Actor"] == ACTOR_PRINCIPAL]
    if not fila.empty:
        if "Readiness_Actual" in panel.columns:
            actual = float(fila["Readiness_Actual"].iloc[0])
        if "Readiness_Requerido" in panel.columns:
            requerido = float(fila["Readiness_Requerido"].iloc[0])

c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    if actual is not None and requerido is not None:
        st.plotly_chart(crear_gauge_readiness(actual, requerido), width='stretch')
    else:
        st.info("Sin datos de readiness para el actor principal.")
with c2:
    if actual is not None:
        st.metric("Actual", f"{actual:.0f}/100")
with c3:
    if requerido is not None:
        delta = f"{actual - requerido:+.0f}" if actual is not None else None
        st.metric("Requerido", f"{requerido:.0f}/100", delta=delta, delta_color="normal")

st.divider()

# --- Readiness por actor --------------------------------------------------
st.subheader("👥 Readiness por Actor")
fig = crear_grafico_comparacion_actores(panel)
if fig:
    st.plotly_chart(fig, width='stretch')
elif panel is not None:
    st.dataframe(panel, width='stretch')

st.divider()

# --- Alertas reales (desde Panel 0) ---------------------------------------
st.subheader("🚨 Alertas")
if panel is not None and "Alertas" in panel.columns:
    marca = panel["Alertas"].astype(str).str.strip().str.lower()
    activas = panel[marca.isin(["sí", "si", "yes", "true", "1"])]
    if not activas.empty:
        for _, row in activas.iterrows():
            desc = row.get("Descripcion_Alerta", "") if "Descripcion_Alerta" in panel.columns else ""
            st.warning(f"**{row['Actor']}** — {desc or 'Alerta activa'}")
    else:
        st.success("Sin alertas activas en el Panel 0.")
else:
    st.info("El Panel 0 no incluye columna de alertas.")

st.divider()

# --- Recomendaciones del primer gate que no puede avanzar -----------------
st.subheader("📋 Recomendaciones Prioritarias")
bloqueada = next((resultados[f] for f in (1, 2, 3) if not resultados[f]["puede_avanzar"]), None)
if bloqueada:
    st.markdown(f"_Fase {bloqueada['metadata']['fase']} — {bloqueada['estado_label']}_")
    for rec in bloqueada["recomendaciones"]:
        with st.container(border=True):
            st.markdown(f"**[{rec['orden']}] {rec['accion']}**")
            st.caption(f"Prioridad: {rec['prioridad']} · Plazo: {rec['plazo']}")
else:
    st.success("Todas las fases evaluadas pueden avanzar.")

st.divider()
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🔬 Ir a Micro-Red"):
        st.switch_page("pages/03_Micro_Red.py")
with c2:
    if st.button("👥 Ir a Panel 0"):
        st.switch_page("pages/02_Panel_0.py")
with c3:
    if st.button("💾 Ir a Export"):
        st.switch_page("pages/06_Export.py")
