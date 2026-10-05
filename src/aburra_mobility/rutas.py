"""Rutas del proyecto, en un solo lugar."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

DATOS = RAIZ / "data"
RAW = DATOS / "raw"
PROCESADOS = DATOS / "processed"
OSM = DATOS / "osm"

INFORME = RAW / "Informe_Movilidad_AMVA_20260827.xlsx"

ESCENARIOS = RAIZ / "scenarios"
VTYPES = ESCENARIOS / "vtypes.add.xml"
PERFIL_SALIDAS = ESCENARIOS / "perfil_salidas.csv"
SUPUESTOS = ESCENARIOS / "SUPUESTOS.md"

REDES = ESCENARIOS / "redes"
PRUEBA_TECNICA = ESCENARIOS / "prueba_tecnica"


def red_municipio(clave: str) -> Path:
    return REDES / f"{clave}.net.xml"


RETICULA = REDES / "reticula.net.xml"
