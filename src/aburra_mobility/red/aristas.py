"""Lectura de atributos de las aristas de una red SUMO generada desde OSM."""

TIPOS_ARTERIA = {"motorway", "trunk", "primary", "secondary", "tertiary"}

ANCHO_AUTO = 1.8


def tipo_corto(edge) -> str:
    """'highway.primary_link' -> 'primary_link'."""
    t = edge.getType() or "?"
    return t.split(".", 1)[1] if t.startswith("highway.") else t


def es_arterial(edge) -> bool:
    """Troncal a terciaria, incluidos sus enlaces (_link)."""
    return tipo_corto(edge).split("_")[0] in TIPOS_ARTERIA


def atributos_por_defecto(edge) -> set[str]:
    """Atributos que netconvert tomo del typemap porque OSM no los traia."""
    return set((edge.getParam("osmDefaults") or "").split())


def carriles_por_defecto(edge) -> bool:
    return "numLanes" in atributos_por_defecto(edge)


def velocidad_por_defecto(edge) -> bool:
    return "speed" in atributos_por_defecto(edge)


def vias_osm(edge) -> list[str]:
    """Ids de las vias OSM que forman la arista."""
    return (edge.getLanes()[0].getParam("origId") or "").split()


def mas_angosta_que_un_auto(edge) -> bool:
    return min(l.getWidth() for l in edge.getLanes()) < ANCHO_AUTO


def km(edges) -> float:
    return sum(e.getLength() for e in edges) / 1000
