# 🔗 Enlaces del Proyecto — LCA Social 2.1

Documento índice con **todos los accesos** del proyecto: código, app, documentos
y un *brief* listo para pegar en una herramienta de diseño.

---

## 🖥️ La aplicación

| Recurso | Enlace / Acción |
|---------|-----------------|
| Abrir la app (local) | **http://localhost:8501** (cuando está corriendo) |
| Iniciar con 1 clic | Doble clic en el icono **«LCA Social 2.1»** del escritorio |
| Iniciar por terminal | `python -m streamlit run streamlit_app.py` |

---

## 💾 Repositorios en GitHub

| Repo | Enlace |
|------|--------|
| **App 2.1** (principal) | https://github.com/antigravitydanielarias-prog/LCA_SOCIAL_2.1 |
| Rama de trabajo | `feat/motor-slca-integracion` |
| Crear Pull Request (app) | https://github.com/antigravitydanielarias-prog/LCA_SOCIAL_2.1/pull/new/feat/motor-slca-integracion |
| **Repo externo** (docs + datos) | https://github.com/antigravitydanielarias-prog/LCA-social |
| Crear Pull Request (externo) | https://github.com/antigravitydanielarias-prog/LCA-social/pull/new/feat/motor-slca-integracion |

---

## 📄 Documentos clave

| Documento | Para qué sirve | Enlace |
|-----------|----------------|--------|
| **Manual de uso** | Cómo instalar, ejecutar y leer resultados | [MANUAL_DE_USO.md](https://github.com/antigravitydanielarias-prog/LCA_SOCIAL_2.1/blob/feat/motor-slca-integracion/MANUAL_DE_USO.md) |
| **Resumen visual** | Versión digerible para el equipo (abrir en navegador) | `RESUMEN_EJECUTIVO_VISUAL.html` |
| Informe del sistema | Marco conceptual + anclaje académico | [INFORME_SISTEMA_SLCA.md](https://github.com/antigravitydanielarias-prog/LCA-social/blob/feat/motor-slca-integracion/INFORME_SISTEMA_SLCA.md) |
| Esqueleto IEEE | Borrador del paper | [INFORME_IEEE_SLCA.md](https://github.com/antigravitydanielarias-prog/LCA-social/blob/feat/motor-slca-integracion/INFORME_IEEE_SLCA.md) |
| Bitácora de cambios | Qué se transformó en la 2.1 | [CAMBIOS_2.1.md](https://github.com/antigravitydanielarias-prog/LCA-social/blob/feat/motor-slca-integracion/CAMBIOS_2.1.md) |

---

## 🧠 El motor de decisión (lo «citable»)

| Archivo | Qué contiene | Enlace |
|---------|--------------|--------|
| `gates.py` | La lógica de los *gates* (única fuente de verdad) | [ver](https://github.com/antigravitydanielarias-prog/LCA_SOCIAL_2.1/blob/feat/motor-slca-integracion/src/modelo_slca/gates.py) |
| `referencias.py` | El respaldo bibliográfico de cada umbral | [ver](https://github.com/antigravitydanielarias-prog/LCA_SOCIAL_2.1/blob/feat/motor-slca-integracion/src/modelo_slca/referencias.py) |

---

## 🎨 Brief para llevar a diseño (copiar y pegar)

> **Qué es:** una herramienta que decide si un proyecto de **energía comunitaria**
> (paneles solares en un territorio) puede **avanzar de fase**, mirando no solo lo
> técnico sino la **madurez social** de la comunidad.
>
> **Cómo decide:** combina 4 miradas — lo que la gente **piensa** (confianza,
> aspiraciones), lo que **existe** físicamente (infraestructura), el **contexto**
> del territorio (pobreza, educación) y la **trayectoria** (12 meses). Con eso
> entrega un semáforo: **🟢 Habilitado · 🟡 Condicional · 🔴 Bloqueado · ⚪ Datos
> insuficientes**, con su justificación académica y un costo estimado.
>
> **Caso real:** «La Esperanza, Bajo Atrato (Chocó)». Resultado: Fase 1 🔴
> bloqueada (falta confianza institucional), Fases 2-3 🟡 condicionales (alta
> pobreza). 
>
> **Tono buscado:** claro, humano, para público interdisciplinario (no solo
> ingenieros). Paleta sugerida: verde sostenibilidad + acentos de semáforo.

---

*Modelo S-LCA 2.1 · Universidad EAFIT · Caso: La Esperanza, Bajo Atrato (Chocó).*
