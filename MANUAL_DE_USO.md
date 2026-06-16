# Manual de Uso — Modelo S-LCA 2.1
### Evaluación Social del Ciclo de Vida para transiciones de fase en energía comunitaria

Este manual explica, paso a paso, **cómo ejecutar el proceso completo**: desde
instalar y levantar la aplicación, hasta cargar los datos de un territorio,
interpretar los veredictos de los *gates* y exportar los resultados.

> **En una frase:** el sistema decide si un proyecto de energía comunitaria puede
> avanzar de fase y devuelve, por unidad de análisis, un estado
> **`HABILITADO` / `CONDICIONAL` / `BLOQUEADO` / `DATOS INSUFICIENTES`**, con su
> justificación académica, un costo estimado de transición y recomendaciones.

---

## 1. Requisitos previos

- **Python 3.9 o superior** (probado en 3.14). Verifícalo con `python --version`.
- **pip** (viene con Python).
- Un **navegador web** (Chrome, Edge, Firefox…).

---

## 2. Instalación

> ⚠️ **Paso 0 — entra primero a la carpeta del proyecto.** El error
> «no se encuentra `requirements.txt`» casi siempre es por estar en otra carpeta
> (como `C:\Users\TuUsuario`).

### Windows (PowerShell)
```powershell
# 1) Entra a la carpeta del proyecto (ajusta la ruta a donde lo tengas)
cd "D:\FOTOS\escritorio semana 14\GRID\Vento\LCA social\LCA_SOCIAL_2.1"

# 2) (Opcional) entorno virtual aislado
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3) Instalar dependencias
pip install -r requirements.txt
```

### macOS / Linux
```bash
cd ".../LCA social/LCA_SOCIAL_2.1"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

> 💡 **¿Ya tienes Python con Streamlit en el sistema?** Puedes **saltarte el
> entorno virtual y el `pip install`** e ir directo a la sección 3. En Windows
> **no uses `source`** (es de macOS/Linux); la activación en PowerShell es
> `.\venv\Scripts\Activate.ps1`.
>
> Para las pruebas: `pip install -r requirements-dev.txt`.

---

## 3. Cómo ejecutar la aplicación

Desde la carpeta `LCA_SOCIAL_2.1`:

```bash
python -m streamlit run streamlit_app.py
```

- Se abrirá automáticamente en el navegador. Si no, entra a **http://localhost:8501**.
- El repositorio ya trae `.streamlit/config.toml` con el puerto **8501** y el tema.
- **Para detener** la aplicación: pulsa `Ctrl + C` en la terminal.

> ¿El puerto 8501 está ocupado? Usa otro:
> `python -m streamlit run streamlit_app.py --server.port 8502`

---

## 4. Los datos que usa el sistema

El modelo se alimenta de **5 archivos Excel**. Ya viene cargado el caso de estudio
real **«La Esperanza, Bajo Atrato (Chocó)»** en `data/uploads/`, así que puedes
explorar la app de inmediato.

| Archivo | Hoja que se lee | Qué contiene |
|---------|-----------------|--------------|
| `PANEL_0_PROTAGONISTAS.xlsx` | `PROTAGONISTAS_READINESS` | Los 5 actores con su *readiness* y alertas |
| `DIMENSIONES_COGNITIVAS.xlsx` | `RESUMEN` | Las 8 dimensiones por fase (IA, IAT, ICI, …) |
| `CONTEXTO_TERRITORIAL.xlsx` | `INDICADORES_DANE` | Pobreza, informalidad, educación, internet… |
| `MEMORIA_TEMPORAL.xlsx` | `SERIE_TEMPORAL_12M` | Serie de 12 meses de cada dimensión |
| `OPERATIVA_MATERIAL.xlsx` | `INFRAESTRUCTURA` | Inventario físico + IOM (índice operativo-material) |

**¿Dónde se guardan?** En `data/uploads/`. **¿Plantillas en blanco?** En
`data/templates/` (o regenéralas con `python tools/generar_plantillas.py`).

### Cómo cargar tus propios datos
Tienes dos formas equivalentes:
1. **Desde la app:** página **⚙️ Configuración → Cargar Datos**, y sube los `.xlsx`.
2. **Manual:** copia los 5 archivos a la carpeta `data/uploads/` (con los mismos
   nombres) y refresca la página.

> El sistema **tolera** que las hojas traigan una fila de título antes del
> encabezado, contexto en formato largo (`Indicador | Valor`) y el IOM ya
> calculado dentro de la hoja. No tienes que reformatear nada de eso.

---

## 5. El proceso completo, paso a paso

```
   ┌─────────────┐   ┌──────────┐   ┌───────────┐   ┌───────────────┐   ┌──────────┐
   │ 1. Plantillas│→ │ 2. Llenar │→ │ 3. Cargar  │→ │ 4. Analizar    │→ │ 5. Export │
   │  (en blanco) │   │  con datos│   │ en la app  │   │ (gates/costos) │   │ JSON/CSV │
   └─────────────┘   └──────────┘   └───────────┘   └───────────────┘   └──────────┘
```

1. **Obtén las plantillas** (`data/templates/` o página Export/Config).
2. **Llénalas** con los datos del territorio (valores 0–100 en las dimensiones,
   indicadores socioeconómicos, inventario físico, etc.).
3. **Carga** los 5 Excel (página Configuración o carpeta `data/uploads/`).
4. **Valida** en **⚙️ Configuración → Validación** que estén los 5 archivos.
5. **Analiza:**
   - **📊 Dashboard** → estado de los gates por fase, *readiness* por actor y alertas.
   - **🔬 Micro-Red** → elige *Actor × Fase × Subcapa* y pulsa **Calcular**. Verás:
     radar de 8 dimensiones, contexto territorial, **veredicto del gate con su
     cita académica**, costo de transición y recomendaciones.
   - **📈 Series** → evolución de las 8 dimensiones en 12 meses.
6. **Exporta** en **💾 Export** (JSON estructurado, CSV o resumen ejecutivo).

---

## 6. Cómo leer los resultados (los *gates*)

Por cada micro-red (actor × fase × subcapa) el sistema devuelve **un estado**:

| Estado | Significado | Qué hacer |
|--------|-------------|-----------|
| ✅ **HABILITADO** | Todas las condiciones evaluables se cumplen | Proceder; mantener monitoreo |
| ⚠️ **CONDICIONAL** | Se puede avanzar pero con condiciones especiales | Proceder con salvaguardas (p. ej. pobreza alta) |
| ❌ **BLOQUEADO** | Hay una **barrera real** del territorio | Resolver el bloqueo **antes** de avanzar |
| 🚫 **DATOS INSUFICIENTES** | Faltan datos requeridos | Recolectar la evidencia faltante. **No es una aprobación** |

### Los umbrales (y por qué)
Cada umbral está **fundamentado en literatura** (ver `src/modelo_slca/referencias.py`):

| Regla | Umbral | Fundamento |
|-------|--------|-----------|
| Confianza institucional mínima | `ICI ≥ 40` | Wüstenhagen et al. (2007); Edwards et al. (2000) |
| Capacidad operativa-material mínima | `IOM ≥ 30` | Geels (2011); Koirala et al. (2016) |
| Piso crítico de cualquier dimensión | `dim ≥ 25` | Plested et al. (2006) |
| Pobreza que activa condición | `> 50 %` | Alkire & Foster (2011) |
| Datos faltantes ⇒ no habilita | — | Principio de precaución (Steel, 2015) |

### Ejemplo real (caso La Esperanza)
- **Fase 1 → ❌ BLOQUEADO**: `ICI = 28 < 40` (confianza institucional crítica).
- **Fase 2 → ⚠️ CONDICIONAL**: pobreza `67 % > 50 %`.
- **Fase 3 → ⚠️ CONDICIONAL**: pobreza `67 % > 50 %`.

Esto se lee así: *la comunidad aún no debe avanzar a la Fase 1 hasta reparar la
confianza institucional; una vez resuelta, podría avanzar bajo condiciones por el
alto nivel de pobreza.*

---

## 7. Las páginas de la aplicación

| Página | Para qué sirve |
|--------|----------------|
| **🏠 Inicio** | Portada y navegación; estado de carga de archivos |
| **📊 Dashboard** | Visión general: gates por fase, *readiness* por actor, alertas y recomendaciones |
| **👥 Panel 0** | Los 5 actores con *readiness* actual vs requerido |
| **🔬 Micro-Red** | Análisis profundo de un actor × fase × subcapa (el corazón del sistema) |
| **📈 Series** | Evolución temporal (12 meses), tendencias, volatilidad y shocks |
| **⚙️ Configuración** | Cargar datos, validar archivos y ver umbrales |
| **💾 Export** | Descargar resultados en JSON / CSV / resumen |

---

## 8. Verificar que todo funciona (pruebas)

```bash
pip install -r requirements-dev.txt
python -m pytest tests -v
```

Deben pasar **14 pruebas** (motor de decisión + integración con el caso real).

---

## 9. Solución de problemas

| Síntoma | Causa probable | Solución |
|---------|----------------|----------|
| `Could not open requirements file` | Estás en otra carpeta (p. ej. `C:\Users\TuUsuario`) | Primero `cd` a la carpeta `LCA_SOCIAL_2.1` y repite |
| `source ... no se reconoce` (Windows) | `source` es solo de macOS/Linux | En PowerShell usa `.\venv\Scripts\Activate.ps1`, o sáltate el venv |
| `Unable to copy ... venvlauncher.exe` | El venv estaba activo al recrearlo | `deactivate`, borra la carpeta `venv` y recréala — o sáltate el venv |
| «Faltan archivos» | No están los 5 Excel en `data/uploads/` | Cárgalos (Configuración) o cópialos a esa carpeta |
| Todo sale **DATOS INSUFICIENTES** | Celdas de valores vacías o falta una dimensión/IOM | Completa los 8 valores por fase y el IOM |
| El navegador no abre | El puerto 8501 está ocupado | `python -m streamlit run streamlit_app.py --server.port 8502` |
| Cambié un Excel y no se refleja | Caché de Streamlit | Botón **Limpiar caché** (Configuración) o recarga la página |
| (Solo en Claude Code) error `check-sql-files.py` | Plugin externo de CockroachDB con un script faltante | Es **inofensivo**; desactiva/reinstala ese plugin con `/plugin` |

---

## 10. Estructura del proyecto (mapa rápido)

```
LCA_SOCIAL_2.1/
├─ streamlit_app.py          ← punto de entrada (lo que ejecutas)
├─ pages/                     ← las 6 páginas de la interfaz
├─ src/
│  ├─ config.py              ← actores, fases, dimensiones, umbrales
│  ├─ modelo_slca/           ← NÚCLEO de decisión (Python puro y citable)
│  │  ├─ gates.py            ← lógica de gates (única fuente de verdad)
│  │  └─ referencias.py      ← respaldo bibliográfico de cada umbral
│  └─ utils/
│     ├─ data_loader.py      ← lee y normaliza los Excel
│     ├─ calculations.py     ← conecta datos → motor → interfaz
│     └─ visualizers.py      ← gráficos (Plotly)
├─ data/
│  ├─ uploads/               ← tus 5 Excel (caso La Esperanza ya incluido)
│  └─ templates/             ← plantillas en blanco
├─ tools/generar_plantillas.py  ← regenera las plantillas
└─ tests/                    ← pruebas automáticas (pytest)
```

---

## 11. Fundamento académico

La lógica no es heurística: cada decisión arrastra su(s) referencia(s). El
compendio vive en `src/modelo_slca/referencias.py` y el marco completo (S-LCA,
*stage-gate*, *community readiness*, transiciones socio-técnicas, MCDA, pobreza
multidimensional) está en `INFORME_SISTEMA_SLCA.md` e `INFORME_IEEE_SLCA.md`.

---

*Modelo S-LCA 2.1 · Universidad EAFIT · Caso: La Esperanza, Bajo Atrato (Chocó).*
