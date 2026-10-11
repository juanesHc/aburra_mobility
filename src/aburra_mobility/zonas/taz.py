"""Asignacion de las calles de la red a las zonas y archivo TAZ de SUMO."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import numpy as np

from .limites import anillos, dentro
from .macrozonas import Zona

VIAS_RAPIDAS = ("highway.motorway", "highway.trunk")
LARGO_MIN_M = 10.0


def aristas_por_zona(net, zonas: list[Zona], limites: dict, nucleo: set[str]) -> dict[str, list]:
    """Aristas donde puede empezar o terminar un viaje, agrupadas por zona."""
    geometria = {r["id"]: anillos(r) for r in limites["elements"]}
    candidatas = [e for e in net.getEdges()
                  if e.getID() in nucleo and e.allows("passenger")
                  and not e.getType().startswith(VIAS_RAPIDAS) and e.getLength() >= LARGO_MIN_M]
    puntos = np.array([net.convertXY2LonLat(*e.getShape()[len(e.getShape()) // 2])
                       for e in candidatas])
    libre = np.ones(len(candidatas), dtype=bool)
    por_zona = defaultdict(list)
    for z in zonas:
        dentro_zona = dentro(puntos, geometria[z.relacion_osm]) & libre
        libre &= ~dentro_zona
        por_zona[z.id] = [candidatas[i] for i in np.flatnonzero(dentro_zona)]
    return {z: es for z, es in por_zona.items() if es}


def escribir_taz(por_zona: dict[str, list], destino: Path):
    """Archivo de zonas: cada calle pesa como origen y destino segun su largo."""
    lineas = ['<?xml version="1.0" encoding="UTF-8"?>', "<tazs>"]
    for z, es in sorted(por_zona.items()):
        lineas.append(f'    <taz id="{z}">')
        for e in es:
            lineas.append(f'        <tazSource id="{e.getID()}" weight="{e.getLength():.1f}"/>')
            lineas.append(f'        <tazSink id="{e.getID()}" weight="{e.getLength():.1f}"/>')
        lineas.append("    </taz>")
    lineas += ["</tazs>", ""]
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(lineas), encoding="utf-8")
