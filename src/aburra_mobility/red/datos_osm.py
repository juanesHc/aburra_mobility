"""Lo que hace falta del .osm crudo para contrastarlo con la red convertida."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class SenalOSM:
    id: str
    lon: float
    lat: float
    tipo: str
    via: str = ""
    tipo_via: str = ""
    en_glorieta: bool = False
    cruza_servicio: bool = False
    vecinos: set = field(default_factory=set)

    @property
    def grado(self) -> int:
        return len(self.vecinos)


@dataclass
class ResumenOSM:
    fechas: dict[str, str] = field(default_factory=dict)
    senales: list[SenalOSM] = field(default_factory=list)
    restricciones: Counter = field(default_factory=Counter)
    vias_por_tipo: Counter = field(default_factory=Counter)
    vias_con_turn_lanes: Counter = field(default_factory=Counter)
    vias_por_archivo: dict[str, set[str]] = field(default_factory=dict)


def leer_osm(osms: list[Path]) -> ResumenOSM:
    """Resume uno o varios .osm."""
    r = ResumenOSM()
    senal_por_id: dict[str, SenalOSM] = {}
    vistos: set[tuple[str, str]] = set()
    for osm in osms:
        vias = r.vias_por_archivo.setdefault(osm.name, set())
        _leer_archivo(osm, r, senal_por_id, vistos, vias)
    return r


def _leer_archivo(osm: Path, r: ResumenOSM, senal_por_id, vistos, vias_del_archivo):
    r.fechas[osm.name] = "desconocida"
    for _, el in ET.iterparse(osm, events=("end",)):
        if el.tag == "meta":
            r.fechas[osm.name] = el.get("osm_base", "desconocida")
            continue
        if el.tag not in ("node", "way", "relation"):
            continue
        if el.tag == "way":
            vias_del_archivo.add(el.get("id"))
        clave = (el.tag, el.get("id"))
        if clave in vistos:
            el.clear()
            continue
        vistos.add(clave)
        tags = {t.get("k"): t.get("v") for t in el.findall("tag")}
        if el.tag == "node":
            vehicular = tags.get("highway") == "traffic_signals"
            peatonal = tags.get("crossing") == "traffic_signals"
            if vehicular or peatonal:
                s = SenalOSM(el.get("id"), float(el.get("lon")), float(el.get("lat")),
                             "vehicular" if vehicular else "peatonal")
                r.senales.append(s)
                senal_por_id[s.id] = s
        elif el.tag == "way":
            tipo = tags.get("highway")
            nds = [n.get("ref") for n in el.findall("nd")]
            for i, ref in enumerate(nds):
                s = senal_por_id.get(ref)
                if s is None:
                    continue
                if not s.via or (s.tipo_via == "service" and tipo != "service"):
                    s.via, s.tipo_via = tags.get("name", "(sin nombre)"), tipo or ""
                s.en_glorieta |= tags.get("junction") == "roundabout"
                if tipo == "service":
                    s.cruza_servicio = True
                    continue
                s.vecinos.update(nds[j] for j in (i - 1, i + 1) if 0 <= j < len(nds))
            if tipo:
                r.vias_por_tipo[tipo] += 1
                if any(k.startswith("turn:lanes") for k in tags):
                    r.vias_con_turn_lanes[tipo] += 1
        elif tags.get("type") == "restriction":
            r.restricciones[tags.get("restriction", "?")] += 1
        el.clear()
