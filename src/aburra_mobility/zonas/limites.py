"""Limites de las zonas desde OpenStreetMap, con cache local."""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np

from ..errores import ErrorPipeline

SERVIDORES = [
    "https://overpass-api.de/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
]
INTENTOS = 3
ESPERA_S = 20


def descargar_limites(relaciones: list[int], destino: Path) -> dict:
    """Geometria de las relaciones de OSM; usa el cache si ya cubre todas."""
    if destino.exists():
        datos = json.loads(destino.read_text(encoding="utf-8"))
        if set(relaciones) <= {r["id"] for r in datos["elements"]}:
            print(f"  Usando limites en cache: {destino}")
            return datos
    consulta = f"[out:json][timeout:180];rel(id:{','.join(map(str, relaciones))});out geom;"
    cuerpo = urllib.parse.urlencode({"data": consulta}).encode()
    for intento in range(INTENTOS):
        for url in SERVIDORES:
            print(f"  Descargando {len(relaciones)} limites de {url.split('/')[2]}...")
            try:
                req = urllib.request.Request(url, data=cuerpo,
                                             headers={"User-Agent": "aburra-mobility (semillero)"})
                with urllib.request.urlopen(req, timeout=240) as r:
                    datos = json.loads(r.read().decode("utf-8"))
            except (OSError, ValueError) as e:
                print(f"    fallo ({str(e)[:80]})")
                continue
            if set(relaciones) <= {r["id"] for r in datos.get("elements", [])}:
                destino.parent.mkdir(parents=True, exist_ok=True)
                destino.write_text(json.dumps(datos), encoding="utf-8")
                return datos
        if intento < INTENTOS - 1:
            time.sleep(ESPERA_S)
    raise ErrorPipeline("no se pudieron descargar los limites de las zonas: Overpass esta "
                        "saturado. Intenta de nuevo en unos minutos.")


def anillos(relacion: dict) -> list[np.ndarray]:
    """Une las vias 'outer' de una relacion en anillos cerrados de (lon, lat)."""
    tramos = [[(p["lon"], p["lat"]) for p in m["geometry"]] for m in relacion["members"]
              if m["type"] == "way" and m.get("role") in ("outer", "") and "geometry" in m]
    cerrados = []
    while tramos:
        anillo = tramos.pop()
        while anillo[0] != anillo[-1]:
            for i, t in enumerate(tramos):
                if t[0] == anillo[-1]:
                    anillo += t[1:]
                elif t[-1] == anillo[-1]:
                    anillo += t[::-1][1:]
                else:
                    continue
                tramos.pop(i)
                break
            else:
                raise ErrorPipeline(f"el limite de {relacion['tags'].get('name')} "
                                    f"(relacion {relacion['id']}) no cierra en OSM")
        cerrados.append(np.array(anillo))
    return cerrados


def dentro(puntos: np.ndarray, anillos_zona: list[np.ndarray]) -> np.ndarray:
    """Mascara de los puntos (lon, lat) que caen dentro de alguno de los anillos."""
    res = np.zeros(len(puntos), dtype=bool)
    for a in anillos_zona:
        x1, y1, x2, y2 = a[:-1, 0], a[:-1, 1], a[1:, 0], a[1:, 1]
        dy = np.where(y2 == y1, 1e-15, y2 - y1)
        (lon0, lat0), (lon1, lat1) = a.min(axis=0), a.max(axis=0)
        cand = np.flatnonzero((puntos[:, 0] >= lon0) & (puntos[:, 0] <= lon1)
                              & (puntos[:, 1] >= lat0) & (puntos[:, 1] <= lat1))
        for bloque in np.array_split(cand, max(1, len(cand) // 500)):
            x, y = puntos[bloque, 0:1], puntos[bloque, 1:2]
            cruza = ((y1 > y) != (y2 > y)) & (x < (x2 - x1) * (y - y1) / dy + x1)
            res[bloque] ^= cruza.sum(axis=1) % 2 == 1
    return res
