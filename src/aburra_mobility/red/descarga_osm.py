"""Descarga de la red vial desde OpenStreetMap, por grupos de vias y con cache local."""

from __future__ import annotations

import io
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from ..entorno import sumo_home
from ..errores import ErrorPipeline
from .municipios import Municipio

GRUPOS = {
    "arterias": ["motorway", "trunk", "primary", "secondary", "tertiary",
                 "motorway_link", "trunk_link", "primary_link", "secondary_link", "tertiary_link",
                 "traffic_signals"],
    "locales": ["unclassified", "residential", "living_street", "road"],
    "servicio": ["service"],
}
OPCIONALES = {"servicio"}
SERVIDORES = "hpi,oapi,pcoffee"
REINTENTOS = 2
ESPERA_S = 20


def ruta_cache(mun: Municipio, carpeta_osm: Path) -> Path:
    return carpeta_osm / f"{mun.clave}_city.osm.xml"


def carpeta_partes(carpeta_osm: Path) -> Path:
    return carpeta_osm / "partes"


def ruta_parte(mun: Municipio, carpeta_osm: Path, grupo: str) -> Path:
    return carpeta_partes(carpeta_osm) / f"{mun.clave}_{grupo}.osm.xml"


def obtener_osm(mun: Municipio, carpeta_osm: Path, archivo_local: Path | None = None,
                forzar_descarga: bool = False) -> Path:
    """Devuelve el .osm a convertir: archivo local, cache o descarga nueva."""
    if archivo_local:
        if not archivo_local.exists():
            raise ErrorPipeline(f"no existe {archivo_local}")
        print(f"  Usando archivo local: {archivo_local}")
        return archivo_local

    destino = ruta_cache(mun, carpeta_osm)
    if destino.exists() and not forzar_descarga:
        print(f"  Usando OSM en cache: {destino}")
        print("  (para bajarlo de nuevo: --descargar)")
        return destino
    if forzar_descarga:
        for grupo in GRUPOS:
            ruta_parte(mun, carpeta_osm, grupo).unlink(missing_ok=True)
    return descargar(mun, carpeta_osm)


def descargar(mun: Municipio, carpeta_osm: Path) -> Path:
    """Baja la red vial del municipio por partes, reanudando las que ya se tienen."""
    osmget = sumo_home() / "tools" / "osmGet.py"
    if not osmget.exists():
        raise ErrorPipeline(f"no se encontro {osmget}")
    carpeta_partes(carpeta_osm).mkdir(parents=True, exist_ok=True)

    print(f"  Descargando {mun.nombre} desde Overpass en {len(GRUPOS)} partes "
          f"(relacion {mun.relacion_osm}).")
    print("  Cada parte puede tardar varios minutos si los servidores estan saturados.")
    listas, faltan = [], []
    for grupo, tipos in GRUPOS.items():
        parte = ruta_parte(mun, carpeta_osm, grupo)
        if parte.exists():
            print(f"  [{grupo}] ya estaba descargada de un intento anterior")
            listas.append(parte)
            continue
        print(f"  [{grupo}] descargando...")
        sys.stdout.flush()
        if bajar_parte(osmget, mun, grupo, tipos, parte):
            print(f"  [{grupo}] lista ({parte.stat().st_size // 1024} KB)")
            listas.append(parte)
        else:
            print(f"  [{grupo}] fallo")
            faltan.append(grupo)

    obligatorias = [g for g in faltan if g not in OPCIONALES]
    if obligatorias:
        raise ErrorPipeline(_mensaje_fallo(mun, carpeta_osm, listas, obligatorias))
    if faltan:
        print(f"  AVISO: sin la parte {', '.join(faltan)}. No cambia la red para autos; "
              "para incluirla, vuelve a descargar con --descargar.")

    destino = ruta_cache(mun, carpeta_osm)
    fusionar_osm(listas, destino)
    for p in listas:
        p.unlink()
        p.with_suffix(".log").unlink(missing_ok=True)
    print(f"  Guardado: {destino} ({destino.stat().st_size // 1024} KB)")
    return destino


def bajar_parte(osmget: Path, mun: Municipio, grupo: str, tipos: list[str], parte: Path) -> bool:
    """Una consulta de osmGet por area para un grupo de tipos de via."""
    prefijo = f"{mun.clave}_{grupo}_descargando"
    tmp = parte.parent / f"{prefijo}_city.osm.xml"
    tmp.unlink(missing_ok=True)
    cmd = [
        sys.executable, str(osmget),
        "--area", str(mun.relacion_osm),
        "--prefix", prefijo,
        "--output-dir", str(parte.parent),
        "--road-types", json.dumps({"highway": tipos}),
        "--url", SERVIDORES,
        "--retries", str(REINTENTOS),
        "--retry-delay", str(ESPERA_S),
        "--verbose",
    ]
    log = parte.with_suffix(".log")
    with log.open("w", encoding="utf-8") as f, subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
            encoding="utf-8", errors="replace") as proc:
        for linea in proc.stdout:
            f.write(linea)
            if linea.startswith("Download from"):
                print("    " + linea.split(" failed ")[0].replace("Download from ", "fallo en ")
                      + " (" + linea.split("(", 1)[-1].split(")")[0] + "), reintentando")
                sys.stdout.flush()
    if proc.returncode != 0 or not tmp.exists():
        tmp.unlink(missing_ok=True)
        return False
    tmp.replace(parte)
    return True


def fusionar_osm(partes: list[Path], destino: Path):
    """Une varios .osm en uno, sin repetir nodos, vias ni relaciones."""
    elementos = {"node": {}, "way": {}, "relation": {}}
    meta = None
    for p in partes:
        for _, el in ET.iterparse(io.BytesIO(_sin_encabezado(p)), events=("end",)):
            if el.tag == "meta" and meta is None:
                meta = ET.tostring(el, encoding="unicode").strip()
            elif el.tag in elementos:
                elementos[el.tag].setdefault(el.get("id"), ET.tostring(el, encoding="unicode").strip())
                el.clear()
    tmp = destino.with_name(destino.name + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<osm version="0.6" generator="aburra-mobility: osmGet.py por partes">\n')
        if meta:
            f.write(f"  {meta}\n")
        for tipo in ("node", "way", "relation"):
            for _, texto in sorted(elementos[tipo].items(), key=lambda kv: int(kv[0])):
                f.write(f"  {texto}\n")
        f.write("</osm>\n")
    tmp.replace(destino)


def _sin_encabezado(parte: Path) -> bytes:
    """Contenido del .osm sin el comentario de opciones que osmGet pone al inicio."""
    datos = parte.read_bytes()
    m = re.search(rb"<osm[\s>]", datos)
    inicio = m.start() if m else 0
    cabeza = re.sub(rb"<!--.*?-->", b"", datos[:inicio], flags=re.DOTALL)
    return cabeza + datos[inicio:]


def _mensaje_fallo(mun: Municipio, carpeta_osm: Path, listas: list[Path], faltan: list[str]) -> str:
    msg = (f"no se pudo descargar {mun.nombre}: fallo la parte {', '.join(faltan)} "
           "(Overpass suele estar saturado).")
    if listas:
        hechas = ", ".join(p.name.removesuffix(".osm.xml").removeprefix(mun.clave + "_") for p in listas)
        msg += (f"\nLas partes ya descargadas ({hechas}) quedan guardadas: al volver a correr el "
                "comando solo se piden las que faltan.")
    msg += f"\nDetalle de cada intento en {carpeta_partes(carpeta_osm)}."
    if ruta_cache(mun, carpeta_osm).exists():
        msg += "\nEl cache anterior sigue intacto: corre sin --descargar para usarlo."
    return msg
