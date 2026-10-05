"""Procedencia de los semaforos de la red: cuales vienen de OSM y cuales no."""

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass

from .datos_osm import SenalOSM

DIST_SENAL_OSM = 35.0


@dataclass
class Semaforos:
    total: int
    desde_osm: list[str]
    adivinados: list[str]
    senales_sin_usar: list[SenalOSM]
    ciclos: list[float]
    cruces_controlados: int


def clasificar_semaforos(net, senales: list[SenalOSM]) -> Semaforos:
    """Separa los semaforos con senal OSM cercana de los adivinados y lista las senales sin usar."""
    nodos_por_tls = defaultdict(set)
    for tls in net.getTrafficLights():
        for entrada, _, _ in tls.getConnections():
            nodos_por_tls[tls.getID()].add(entrada.getEdge().getToNode())

    puntos = [(s.id, *net.convertLonLat2XY(s.lon, s.lat)) for s in senales]
    desde_osm, adivinados, usadas = [], [], set()
    for tid, nodos in nodos_por_tls.items():
        cerca = set()
        for nodo in nodos:
            nx, ny = nodo.getCoord()[:2]
            for sid, x, y in puntos:
                if math.hypot(x - nx, y - ny) <= DIST_SENAL_OSM:
                    cerca.add(sid)
        de_osm = cerca or tid.startswith("GS_")
        (desde_osm if de_osm else adivinados).append(tid)
        usadas |= cerca

    ciclos = [sum(p.duration for p in prog.getPhases())
              for tls in net.getTrafficLights() for prog in tls.getPrograms().values()]

    return Semaforos(
        total=len(nodos_por_tls),
        desde_osm=desde_osm,
        adivinados=adivinados,
        senales_sin_usar=[s for s in senales if s.id not in usadas],
        ciclos=ciclos,
        cruces_controlados=sum(len(n) for n in nodos_por_tls.values()),
    )
