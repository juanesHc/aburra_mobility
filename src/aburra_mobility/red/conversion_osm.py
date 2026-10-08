"""Conversion OSM -> red SUMO con netconvert."""

from __future__ import annotations

import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path

from ..entorno import sumo_home
from ..errores import ErrorPipeline

JOIN_DIST = 15.0

ANCHO_CARRIL_COMPARTIDO = 2.5


def typemaps() -> list[Path]:
    """Typemap base + capa urbana."""
    carpeta = sumo_home() / "data" / "typemap"
    return [carpeta / "osmNetconvert.typ.xml", carpeta / "osmNetconvertUrbanDe.typ.xml"]


def opciones_netconvert(adivinar_semaforos: bool) -> list[str]:
    return [
        "--type-files", ",".join(str(t) for t in typemaps()),

        "--keep-edges.by-vclass", "passenger",

        "--geometry.remove",
        "--roundabouts.guess",

        "--junctions.join",
        "--junctions.join-dist", str(JOIN_DIST),

        "--tls.guess-signals",
        "--tls.discard-simple",
        "--tls.join",
        "--tls.guess", "true" if adivinar_semaforos else "false",
        "--tls.default-type", "static",

        "--remove-edges.isolated",

        "--no-turnarounds.except-deadend",

        "--osm.turn-lanes",
        "--osm.annotate-defaults",

        "--output.street-names",
        "--output.original-names",
    ]


def correr_netconvert(cmd: list[str], log: Path) -> str:
    """Corre netconvert, anexa comando y salida al log, y devuelve la salida."""
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    salida = r.stdout + r.stderr
    with log.open("a", encoding="utf-8") as f:
        f.write("$ " + " ".join(cmd) + "\n")
        f.write(salida + "\n")
    if r.returncode != 0:
        raise ErrorPipeline(f"netconvert fallo. Ver {log}\n{r.stderr[-2000:]}")
    return salida


def convertir(osms: list[Path], red: Path, log: Path, adivinar_semaforos: bool) -> str:
    """Convierte uno o varios .osm en una sola red."""
    cmd = ["netconvert", "--osm-files", ",".join(str(o) for o in osms),
           *opciones_netconvert(adivinar_semaforos),
           "--output-file", str(red)]
    return correr_netconvert(cmd, log)


def carriles_compartidos(net, excluir: set[str] = frozenset()) -> dict[str, list[int]]:
    """Carriles mas angostos que un auto, por arista: {id: [indices]}."""
    from .aristas import ANCHO_AUTO

    return {e.getID(): [l.getIndex() for l in e.getLanes() if l.getWidth() < ANCHO_AUTO]
            for e in net.getEdges()
            if e.getID() not in excluir and any(l.getWidth() < ANCHO_AUTO for l in e.getLanes())}


def salidas_de_glorieta(net, excluir: set[str] = frozenset()) -> list[tuple[str, str, int, int]]:
    """Salidas de glorieta que solo se toman desde el carril exterior, como (desde, hacia, carril, carril_destino)."""
    anillo = {eid for r in net.getRoundabouts() for eid in r.getEdges()}
    nuevas = []
    for eid in sorted(anillo - excluir):
        e = net.getEdge(eid)
        if e.getLaneNumber() < 2 or not e.getLanes()[1].allows("passenger"):
            continue
        carriles, hacia = defaultdict(set), {}
        for l in e.getLanes():
            for c in l.getOutgoing():
                destino = c.getTo().getID()
                if destino in anillo or destino in excluir:
                    continue
                carriles[destino].add(l.getIndex())
                if l.getIndex() == 0:
                    hacia[destino] = c.getToLane().getIndex()
        for destino, desde in sorted(carriles.items()):
            if desde == {0}:
                ultimo = net.getEdge(destino).getLaneNumber() - 1
                nuevas.append((eid, destino, 1, min(hacia[destino] + 1, ultimo)))
    return nuevas


def ajustar_red(sin_podar: Path, red: Path, a_quitar: set[str],
                a_ensanchar: dict[str, list[int]], a_conectar: list[tuple[str, str, int, int]],
                log: Path):
    """Segunda pasada de netconvert: poda, ensancha carriles compartidos y agrega salidas de glorieta."""
    with tempfile.TemporaryDirectory() as tmp:
        conexiones = Path(tmp) / "salidas_glorieta.con.xml"
        conexiones.write_text("<connections>\n" + "".join(
            f'    <connection from="{a}" to="{b}" fromLane="{i}" toLane="{j}"/>\n'
            for a, b, i, j in a_conectar) + "</connections>\n", encoding="utf-8")
        lista = Path(tmp) / "aristas_a_podar.txt"
        lista.write_text("\n".join(sorted(a_quitar)), encoding="utf-8")
        parche = Path(tmp) / "anchos.edg.xml"
        parche.write_text("<edges>\n" + "".join(
            f'    <edge id="{eid}">'
            + "".join(f'<lane index="{i}" width="{ANCHO_CARRIL_COMPARTIDO}"/>' for i in carriles)
            + "</edge>\n"
            for eid, carriles in sorted(a_ensanchar.items())) + "</edges>\n", encoding="utf-8")
        cmd = ["netconvert", "--sumo-net-file", str(sin_podar),
               "--edge-files", str(parche),
               "--connection-files", str(conexiones),
               "--remove-edges.input-file", str(lista),
               "--remove-edges.isolated",
               "--output-file", str(red)]
        correr_netconvert(cmd, log)
