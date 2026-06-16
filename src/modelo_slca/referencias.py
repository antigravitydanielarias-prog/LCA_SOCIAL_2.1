"""
referencias.py — Compilado bibliográfico del Modelo S-LCA 2.0
=============================================================

Anclaje académico del sistema, en código. Cada referencia se mapea al
componente del informe que fundamenta (§4.x) y al uso concreto dentro del
motor (p. ej., la justificación de un umbral de gate).

El objetivo es que el motor pueda CITAR su propia lógica: cuando un gate
devuelve BLOCKED por ICI<40, la justificación puede arrastrar la(s)
referencia(s) que respaldan ese umbral. Esto cierra el hueco §6.1 del
informe (umbrales hoy heurísticos -> umbrales fundamentados).

Uso típico:
    from modelo_slca.referencias import REFERENCIAS, citar, por_componente
    citar("alkire_foster_2011")          # -> str formateada
    por_componente("§4.7")               # -> list[Referencia]
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Referencia:
    id: str
    autores: str
    anio: int
    titulo: str
    fuente: str
    identificador: str   # DOI, handle o URL estable
    componente: str      # sección del informe que fundamenta
    uso: str             # para qué se cita dentro del sistema

    def formato(self) -> str:
        return (f"{self.autores} ({self.anio}). {self.titulo}. "
                f"{self.fuente}. {self.identificador}")


REFERENCIAS: dict[str, Referencia] = {

    # --- §4.1 Marco raíz S-LCA -------------------------------------------
    "unep_setac_2009": Referencia(
        id="unep_setac_2009",
        autores="UNEP/SETAC",
        anio=2009,
        titulo="Guidelines for Social Life Cycle Assessment of Products",
        fuente="United Nations Environment Programme / SETAC",
        identificador="https://www.lifecycleinitiative.org/",
        componente="§4.1",
        uso=("Marco metodológico raíz. Define las 5 categorías de "
             "stakeholders (trabajadores, cadena de valor, COMUNIDAD LOCAL, "
             "consumidores, sociedad). Fundamenta que el actor sea la unidad."),
    ),
    "unep_2020": Referencia(
        id="unep_2020",
        autores="UNEP (Benoît Norris, C., Traverso, M., Neugebauer, S., et al.)",
        anio=2020,
        titulo=("Guidelines for Social Life Cycle Assessment of Products "
                "and Organizations"),
        fuente="United Nations Environment Programme",
        identificador="https://wedocs.unep.org/handle/20.500.11822/34554",
        componente="§4.1",
        uso=("Versión vigente. Extiende a escala organizacional y añade la "
             "categoría 'Children'. Referencia base obligada del informe."),
    ),

    # --- §4.2 Modelo de puertas / fases ----------------------------------
    "cooper_1990": Referencia(
        id="cooper_1990",
        autores="Cooper, R. G.",
        anio=1990,
        titulo="Stage-Gate Systems: A New Tool for Managing New Products",
        fuente="Business Horizons, 33(3), 44-54",
        identificador="https://doi.org/10.1016/0007-6813(90)90040-I",
        componente="§4.2",
        uso="Origen del modelo de puertas por fases (gates de decisión).",
    ),
    "cooper_2008": Referencia(
        id="cooper_2008",
        autores="Cooper, R. G.",
        anio=2008,
        titulo=("Perspective: The Stage-Gate Idea-to-Launch Process — "
                "Update, What's New, and NexGen Systems"),
        fuente="Journal of Product Innovation Management, 25(3), 213-232",
        identificador="https://doi.org/10.1111/j.1540-5885.2008.00296.x",
        componente="§4.2",
        uso=("Aclara que Stage-Gate NO es lineal ni rígido: respalda que tus "
             "gates son puntos de decisión, no una secuencia obligatoria."),
    ),
    "mankins_2009": Referencia(
        id="mankins_2009",
        autores="Mankins, J. C.",
        anio=2009,
        titulo="Technology readiness assessments: A retrospective",
        fuente="Acta Astronautica, 65(9-10), 1216-1223",
        identificador="https://doi.org/10.1016/j.actaastro.2009.03.058",
        componente="§4.2",
        uso="Niveles de madurez tecnológica (TRL) como análogo de gate.",
    ),

    # --- §4.3 Community Readiness (ancla principal) ----------------------
    "edwards_2000": Referencia(
        id="edwards_2000",
        autores=("Edwards, R. W., Jumper-Thurman, P., Plested, B. A., "
                 "Oetting, E. R., & Swanson, L."),
        anio=2000,
        titulo="Community Readiness: Research to Practice",
        fuente="Journal of Community Psychology, 28(3), 291-307",
        identificador="https://doi.org/10.1002/(SICI)1520-6629(200005)28:3<291::AID-JCOP5>3.0.CO;2-9",
        componente="§4.3",
        uso=("ANCLA PRINCIPAL del esquema de gates. Define 9 etapas de "
             "readiness, de 'ausencia de conciencia' a 'apropiación "
             "comunitaria'. Fundamenta los estados por niveles."),
    ),
    "plested_2006": Referencia(
        id="plested_2006",
        autores="Plested, B. A., Edwards, R. W., & Jumper-Thurman, P.",
        anio=2006,
        titulo="Community Readiness: A Handbook for Successful Change",
        fuente="Tri-Ethnic Center for Prevention Research, Colorado State Univ.",
        identificador="https://www.ndhealth.gov/injury/nd_prevention_tool_kit/docs/community_readiness_handbook.pdf",
        componente="§4.3",
        uso=("Regla clave: para avanzar, TODAS las dimensiones deben estar a "
             "nivel similar de readiness. Fundamenta 'cualquier dim < crítico "
             "-> BLOCKED' y las estrategias apropiadas a la etapa."),
    ),

    # --- §4.4 Aceptación social / justicia energética --------------------
    "wustenhagen_2007": Referencia(
        id="wustenhagen_2007",
        autores="Wüstenhagen, R., Wolsink, M., & Bürer, M. J.",
        anio=2007,
        titulo=("Social acceptance of renewable energy innovation: "
                "An introduction to the concept"),
        fuente="Energy Policy, 35(5), 2683-2691",
        identificador="https://doi.org/10.1016/j.enpol.2006.12.001",
        componente="§4.4",
        uso=("Referencia obligada de aceptación social. Triángulo: "
             "socio-política, comunitaria y de mercado. Fundamenta las "
             "dimensiones cognitivas (ICI, IAT, IA...)."),
    ),
    "sovacool_dworkin_2015": Referencia(
        id="sovacool_dworkin_2015",
        autores="Sovacool, B. K., & Dworkin, M. H.",
        anio=2015,
        titulo="Energy justice: Conceptual insights and practical applications",
        fuente="Applied Energy, 142, 435-444",
        identificador="https://doi.org/10.1016/j.apenergy.2015.01.002",
        componente="§4.4",
        uso=("Justicia distributiva, procedimental y de reconocimiento. "
             "Lenguaje para conectar ICI/IIN con equidad."),
    ),

    # --- §4.5 Transiciones socio-técnicas (capa operativa-material) ------
    "geels_2011": Referencia(
        id="geels_2011",
        autores="Geels, F. W.",
        anio=2011,
        titulo=("The multi-level perspective on sustainability transitions: "
                "Responses to seven criticisms"),
        fuente="Environmental Innovation and Societal Transitions, 1(1), 24-40",
        identificador="https://doi.org/10.1016/j.eist.2011.02.002",
        componente="§4.5",
        uso=("MLP: nichos, regímenes y paisaje. Fundamenta separar lo "
             "material/infraestructural (IOM) de lo cognitivo."),
    ),
    "geels_2002": Referencia(
        id="geels_2002",
        autores="Geels, F. W.",
        anio=2002,
        titulo=("Technological transitions as evolutionary reconfiguration "
                "processes: a multi-level perspective and a case-study"),
        fuente="Research Policy, 31(8-9), 1257-1274",
        identificador="https://doi.org/10.1016/S0048-7333(02)00062-8",
        componente="§4.5",
        uso="Desarrollo seminal de la MLP aplicada a transiciones.",
    ),

    # --- §4.6 Energía comunitaria / micro-redes --------------------------
    "koirala_2016": Referencia(
        id="koirala_2016",
        autores="Koirala, B. P., Koliou, E., Friege, J., Hakvoort, R. A., & Herder, P. M.",
        anio=2016,
        titulo=("Energetic communities for community energy: A review of key "
                "issues and trends shaping integrated community energy systems"),
        fuente="Renewable and Sustainable Energy Reviews, 56, 722-744",
        identificador="https://doi.org/10.1016/j.rser.2015.11.080",
        componente="§4.6",
        uso=("Referencia obligada del marco de actores (tu Panel 0 ya usa su "
             "Table 4). Evaluación de infraestructura y recursos existentes."),
    ),
    "bauwens_2022": Referencia(
        id="bauwens_2022",
        autores="Bauwens, T., Schraven, D., Drewing, E., Radtke, J., et al.",
        anio=2022,
        titulo=("Conceptualizing community in energy systems: A systematic "
                "review of 183 definitions"),
        fuente="Renewable and Sustainable Energy Reviews, 156, 111999",
        identificador="https://doi.org/10.1016/j.rser.2021.111999",
        componente="§4.6",
        uso="Problematiza la definición de 'comunidad' en tu sistema.",
    ),
    "vanegas_cantarero_2020": Referencia(
        id="vanegas_cantarero_2020",
        autores="Vanegas Cantarero, M. M.",
        anio=2020,
        titulo=("Of renewable energy, energy democracy, and sustainable "
                "development: A roadmap to accelerate the energy transition "
                "in developing countries"),
        fuente="Energy Research & Social Science, 70, 101716",
        identificador="https://doi.org/10.1016/j.erss.2020.101716",
        componente="§4.6",
        uso="Energía comunitaria y democracia energética en países en desarrollo.",
    ),

    # --- §4.7 Contexto territorial / pobreza multidimensional ------------
    "alkire_foster_2011": Referencia(
        id="alkire_foster_2011",
        autores="Alkire, S., & Foster, J.",
        anio=2011,
        titulo="Counting and multidimensional poverty measurement",
        fuente="Journal of Public Economics, 95(7-8), 476-487",
        identificador="https://doi.org/10.1016/j.jpubeco.2010.11.006",
        componente="§4.7",
        uso=("Referencia obligada. Método de DOBLE CORTE (corte dentro de "
             "cada dimensión + corte entre dimensiones). Estructuralmente "
             "idéntico a tu lógica de umbral por indicador + agregación. "
             "Advierte que los cortes exigen justificación normativa fuerte: "
             "cierra el hueco §6.1."),
    ),

    # --- §4.8 Decisión multicriterio (umbrales y pesos) ------------------
    "pohekar_ramachandran_2004": Referencia(
        id="pohekar_ramachandran_2004",
        autores="Pohekar, S. D., & Ramachandran, M.",
        anio=2004,
        titulo=("Application of multi-criteria decision making to sustainable "
                "energy planning — A review"),
        fuente="Renewable and Sustainable Energy Reviews, 8(4), 365-381",
        identificador="https://doi.org/10.1016/j.rser.2003.12.007",
        componente="§4.8",
        uso="Revisión seminal de MCDA en planificación energética sostenible.",
    ),
    "saaty_1980": Referencia(
        id="saaty_1980",
        autores="Saaty, T. L.",
        anio=1980,
        titulo="The Analytic Hierarchy Process",
        fuente="McGraw-Hill, New York",
        identificador="ISBN 0-07-054371-2",
        componente="§4.8",
        uso=("Base del AHP. Justificación metodológica para asignar PESOS a "
             "las dimensiones (hueco §6.2)."),
    ),

    # --- §4.9 / §6.3 Memoria temporal y principio de precaución ----------
    "steel_2015": Referencia(
        id="steel_2015",
        autores="Steel, D.",
        anio=2015,
        titulo="Philosophy and the Precautionary Principle",
        fuente="Cambridge University Press",
        identificador="https://doi.org/10.1017/CBO9781139939652",
        componente="§6.3",
        uso=("Principio de precaución: ausencia de evidencia != aprobación. "
             "Fundamenta el FIX del bug crítico (datos faltantes -> NO "
             "habilitado)."),
    ),
    "kostadinov_2015": Referencia(
        id="kostadinov_2015",
        autores="Kostadinov, I., Daniel, M., Stanley, L., Gancia, A., & Cargo, M.",
        anio=2015,
        titulo=("A systematic review of community readiness tool applications: "
                "Implications for reporting"),
        fuente="International Journal of Environmental Research and Public Health, 12(4), 3453-3468",
        identificador="https://doi.org/10.3390/ijerph120403453",
        componente="§6.4",
        uso="Precedente metodológico para la VALIDACIÓN del modelo.",
    ),
}


def citar(ref_id: str) -> str:
    """Devuelve la cita formateada de una referencia por su id."""
    ref = REFERENCIAS.get(ref_id)
    if ref is None:
        raise KeyError(f"Referencia desconocida: {ref_id!r}")
    return ref.formato()


def por_componente(componente: str) -> list[Referencia]:
    """Lista las referencias que fundamentan un componente del informe."""
    return [r for r in REFERENCIAS.values() if r.componente == componente]


if __name__ == "__main__":
    print(f"{len(REFERENCIAS)} referencias compiladas.\n")
    for comp in sorted({r.componente for r in REFERENCIAS.values()}):
        print(comp)
        for r in por_componente(comp):
            print(f"  - {r.formato()}")
        print()
