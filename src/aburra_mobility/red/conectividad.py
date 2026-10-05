"""Conectividad de la red: componentes, aristas ruteables y aristas de borde."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Conectividad:
    debiles: list[set[str]]
    fuertes: list[set[str]]
    llegan: set[str]
    salen: set[str]
    utiles: set[str]
    podar: set[str]
    fuera_del_principal: set[str]


def _grafo_autos(net) -> dict[str, set[str]]:
    """Grafo arista -> aristas siguientes, solo por conexiones que un auto puede usar."""
    sig = {}
    for e in net.getEdges():
        destinos = set()
        for otra, conexiones in e.getOutgoing().items():
            if any(c.getFromLane().allows("passenger") and c.getToLane().allows("passenger")
                   for c in conexiones):
                destinos.add(otra.getID())
        sig[e.getID()] = destinos
    return sig


def _invertir(sig: dict[str, set[str]]) -> dict[str, set[str]]:
    inv = defaultdict(set)
    for u, vs in sig.items():
        for v in vs:
            inv[v].add(u)
    return inv


def _alcanzables(inicio: set[str], sig, excluir: set[str] = frozenset()) -> set[str]:
    visto, pila = set(inicio), list(inicio)
    while pila:
        for v in sig[pila.pop()]:
            if v not in visto and v not in excluir:
                visto.add(v)
                pila.append(v)
    return visto


def componentes_debiles(sig) -> list[set[str]]:
    vecinos = defaultdict(set)
    for u, vs in sig.items():
        vecinos[u]
        for v in vs:
            vecinos[u].add(v)
            vecinos[v].add(u)
    comps, visto = [], set()
    for u in vecinos:
        if u in visto:
            continue
        c = _alcanzables({u}, vecinos)
        visto |= c
        comps.append(c)
    return sorted(comps, key=len, reverse=True)


def componentes_fuertes(sig) -> list[set[str]]:
    """Kosaraju iterativo: la recursion se desborda con redes de ciudad."""
    orden, visto = [], set()
    for raiz in sig:
        if raiz in visto:
            continue
        visto.add(raiz)
        pila = [(raiz, iter(sig[raiz]))]
        while pila:
            u, it = pila[-1]
            for v in it:
                if v not in visto:
                    visto.add(v)
                    pila.append((v, iter(sig[v])))
                    break
            else:
                orden.append(u)
                pila.pop()
    inv = _invertir(sig)
    comps, asignado = [], set()
    for u in reversed(orden):
        if u in asignado:
            continue
        c = _alcanzables({u}, inv, excluir=asignado)
        asignado |= c
        comps.append(c)
    return sorted(comps, key=len, reverse=True)


def analizar_conectividad(net) -> Conectividad:
    """Decide que aristas se conservan."""
    sig = _grafo_autos(net)
    inv = _invertir(sig)
    debiles = componentes_debiles(sig)
    fuertes = componentes_fuertes(sig)
    nucleo = fuertes[0]
    principal = next(c for c in debiles if nucleo <= c)

    llegan = _alcanzables(nucleo, inv)
    salen = _alcanzables(nucleo, sig)
    fuentes = {e for e in sig if not inv[e]}
    sumideros = {e for e in sig if not sig[e]}
    de_paso = _alcanzables(nucleo | fuentes, sig) & _alcanzables(nucleo | sumideros, inv)

    utiles = (llegan | salen | de_paso) & principal
    return Conectividad(
        debiles=debiles,
        fuertes=fuertes,
        llegan=llegan,
        salen=salen,
        utiles=utiles,
        podar=set(sig) - utiles,
        fuera_del_principal=set(sig) - principal,
    )


def aristas_de_borde(net) -> tuple[list, list]:
    """Aristas de entrada y salida de la red."""
    entradas = [e for e in net.getEdges() if e.is_fringe(e.getIncoming())]
    salidas = [e for e in net.getEdges() if e.is_fringe(e.getOutgoing())]
    return entradas, salidas


def ids_de_borde(red: Path) -> tuple[list[str], list[str]]:
    """Ids ordenados de las aristas de borde utiles como origen y destino."""
    import sumolib

    net = sumolib.net.readNet(str(red))
    c = analizar_conectividad(net)
    entradas, salidas = aristas_de_borde(net)
    return (sorted(e.getID() for e in entradas if e.getID() in c.llegan),
            sorted(e.getID() for e in salidas if e.getID() in c.salen))
