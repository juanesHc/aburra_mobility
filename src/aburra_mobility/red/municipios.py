"""Municipios del Valle de Aburra y su limite administrativo en OSM."""

import re
import unicodedata
from dataclasses import dataclass

from ..errores import ErrorPipeline


@dataclass(frozen=True)
class Municipio:
    clave: str
    nombre: str
    relacion_osm: int
    divipola: str


MUNICIPIOS = {m.clave: m for m in [
    Municipio("barbosa", "Barbosa", 1307290, "05079"),
    Municipio("bello", "Bello", 1307262, "05088"),
    Municipio("caldas", "Caldas", 1307283, "05129"),
    Municipio("copacabana", "Copacabana", 1307276, "05212"),
    Municipio("envigado", "Envigado", 1307277, "05266"),
    Municipio("girardota", "Girardota", 1307263, "05308"),
    Municipio("itagui", "Itagüí", 1343279, "05360"),
    Municipio("la_estrella", "La Estrella", 1307284, "05380"),
    Municipio("medellin", "Medellín", 1343264, "05001"),
    Municipio("sabaneta", "Sabaneta", 1307270, "05631"),
]}

POR_DEFECTO = "sabaneta"


def clave_municipio(texto: str) -> str:
    """'Itagüí' -> 'itagui', 'La Estrella' -> 'la_estrella'."""
    sin_tildes = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[\s\-]+", "_", sin_tildes.strip().lower())


def clave_red(municipios: list[Municipio]) -> str:
    """Nombre de archivo de la red de uno o varios municipios."""
    return "_".join(sorted({m.clave for m in municipios}))


VALLE = "valle"


def buscar_municipios(textos: list[str]) -> list[Municipio]:
    """Municipios sin repetir, en orden alfabetico de clave; "valle" equivale a los diez."""
    if any(clave_municipio(t) == VALLE for t in textos):
        return sorted(MUNICIPIOS.values(), key=lambda m: m.clave)
    return sorted({buscar_municipio(t).clave: buscar_municipio(t) for t in textos}.values(),
                  key=lambda m: m.clave)


def es_valle_completo(municipios: list[Municipio]) -> bool:
    return {m.clave for m in municipios} == set(MUNICIPIOS)


def buscar_municipio(texto: str) -> Municipio:
    clave = clave_municipio(texto)
    if clave not in MUNICIPIOS:
        raise ErrorPipeline(f"municipio desconocido '{texto}'. "
                            f"Opciones: {', '.join(sorted(MUNICIPIOS))}")
    return MUNICIPIOS[clave]
