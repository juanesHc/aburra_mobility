"""Tiempos de viaje entre zonas sobre la red, a flujo libre."""

from __future__ import annotations

import heapq

import numpy as np
import pandas as pd

from ..red.conectividad import grafo_autos


def arista_representativa(aristas: list):
    """La arista mas cercana al centro de la zona, ponderando cada una por su largo."""
    largos = np.array([e.getLength() for e in aristas])
    puntos = np.array([e.getShape()[len(e.getShape()) // 2] for e in aristas])
    centro = (puntos * largos[:, None]).sum(axis=0) / largos.sum()
    return aristas[int(np.argmin(((puntos - centro) ** 2).sum(axis=1)))]


def _dijkstra(origen: str, siguientes: dict[str, set[str]], tiempo: dict[str, float]) -> dict[str, float]:
    dist = {origen: 0.0}
    cola = [(0.0, origen)]
    while cola:
        d, u = heapq.heappop(cola)
        if d > dist[u]:
            continue
        for v in siguientes[u]:
            nd = d + tiempo[v]
            if nd < dist.get(v, np.inf):
                dist[v] = nd
                heapq.heappush(cola, (nd, v))
    return dist


def tiempos_entre_zonas(net, por_zona: dict[str, list]) -> pd.DataFrame:
    """Minutos entre las aristas representativas; dentro de una zona, el promedio hacia sus calles."""
    siguientes = grafo_autos(net)
    tiempo = {e.getID(): e.getLength() / e.getSpeed() for e in net.getEdges()}
    zonas = sorted(por_zona)
    rep = {z: arista_representativa(por_zona[z]).getID() for z in zonas}
    m = pd.DataFrame(np.nan, index=zonas, columns=zonas)
    for z in zonas:
        dist = _dijkstra(rep[z], siguientes, tiempo)
        for w in zonas:
            m.loc[z, w] = dist.get(rep[w], np.nan)
        largos = np.array([e.getLength() for e in por_zona[z]])
        internos = np.array([dist.get(e.getID(), np.nan) for e in por_zona[z]])
        m.loc[z, z] = np.nansum(internos * largos) / largos[~np.isnan(internos)].sum()
    return m / 60.0
