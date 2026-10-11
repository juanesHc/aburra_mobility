"""Zonas del modelo: las macrozonas del informe que OSM permite dibujar."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from ..errores import ErrorPipeline
from ..red.municipios import MUNICIPIOS, clave_municipio

COMUNAS_MEDELLIN = {
    "medellin__popular": ("Popular", 7680903),
    "medellin__santa_cruz": ("Santa Cruz", 7680904),
    "medellin__manrique": ("Manrique", 7680859),
    "medellin__aranjuez": ("Aranjuez", 7677386),
    "medellin__castilla": ("Castilla", 7680807),
    "medellin__doce_de_octubre": ("Doce de Octubre", 7680403),
    "medellin__robledo": ("Robledo", 7680678),
    "medellin__villa_hermosa": ("Villa Hermosa", 11937925),
    "medellin__buenos_aires": ("Buenos Aires", 7673971),
    "medellin__la_candelaria": ("La Candelaria", 7673972),
    "medellin__laureles_estadio": ("Laureles-Estadio", 7680490),
    "medellin__la_america": ("La América", 7680799),
    "medellin__san_javier": ("San Javier", 7680798),
    "medellin__el_poblado": ("El Poblado", 7673973),
    "medellin__guayabal": ("Guayabal", 7676069),
    "medellin__belen": ("Belén", 7676068),
    "medellin__corregimiento_san_sebastian_de_palmitas": ("San Sebastián de Palmitas", 3541284),
    "medellin__corregimiento_san_cristobal": ("San Cristóbal", 3541285),
    "medellin__corregimiento_altavista": ("Altavista", 3541283),
    "medellin__corregimiento_san_antonio_de_prado": ("San Antonio de Prado", 3541286),
    "medellin__corregimiento_santa_elena": ("Santa Elena", 3541287),
}


@dataclass(frozen=True)
class Zona:
    id: str
    nombre: str
    municipio: str
    relacion_osm: int


def zonas_modelo() -> list[Zona]:
    """Las 16 comunas y 5 corregimientos de Medellin y un municipio entero por cada uno de los otros nueve."""
    zonas = [Zona(z, nombre, "medellin", rel) for z, (nombre, rel) in COMUNAS_MEDELLIN.items()]
    zonas += [Zona(m.clave, m.nombre, m.clave, m.relacion_osm)
              for m in MUNICIPIOS.values() if m.clave != "medellin"]
    return zonas


def zona_de_macrozona(taz_id: str, municipio: str) -> str | None:
    """Zona del modelo a la que va una macrozona del informe; None para 'Sin especificar'."""
    if taz_id in COMUNAS_MEDELLIN:
        return taz_id
    clave = clave_municipio(municipio)
    return clave if clave in MUNICIPIOS and clave != "medellin" else None


def marginales(procesados: Path) -> pd.DataFrame:
    """Viajes que salen y llegan por zona del modelo, sumando las macrozonas que agrupa."""
    mz = pd.read_csv(procesados / "macrozonas_od.csv")
    mz["zona"] = [zona_de_macrozona(t, m) for t, m in zip(mz["taz_id"], mz["municipio"])]
    perdidas = mz[mz["zona"].isna() & (mz["municipio"] != "Sin especificar")]
    if not perdidas.empty:
        raise ErrorPipeline("macrozonas del informe sin zona en el modelo: "
                            + ", ".join(sorted(set(perdidas["taz_id"]))))
    tabla = mz.dropna(subset=["zona"]).pivot_table(index="zona", columns="extremo",
                                                   values="viajes", aggfunc="sum")
    return tabla.rename(columns={"origen": "salen", "destino": "llegan"})[["salen", "llegan"]]
