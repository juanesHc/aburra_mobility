"""Demanda SINTETICA para probar la cadena de herramientas. NO ES MEDELLIN."""

from __future__ import annotations

import random
from pathlib import Path

import pandas as pd

VIAJES = 3000
DESDE, HASTA = 5, 10
PARES_POR_HORA = 12
SEMILLA = 42

ADVERTENCIA = """
  ==================================================================
  ARCHIVO DE PRUEBA - NO USAR PARA RESULTADOS

  Perfil temporal: REAL (EOD 2025 AMVA).
  Distribucion espacial: INVENTADA (uniforme sobre el perimetro).
  Red: {red}. Si es una red OSM, el 'perimetro' son las aristas
  is_fringe, que en su mayoria son calles ciegas, no accesos reales.

  No existe matriz origen-destino. Cualquier conclusion sobre flujos,
  congestion o rutas carece de validez.
  ==================================================================
"""


def escribir_flujos(entradas: list[str], salidas: list[str], perfil_csv: Path,
                    destino: Path, red: Path) -> dict:
    """Convierte el perfil horario en elementos <flow> de SUMO."""
    perfil = pd.read_csv(perfil_csv)[["hora", "w_privado"]]
    perfil.columns = ["hora", "peso"]

    v = perfil[(perfil["hora"] >= DESDE) & (perfil["hora"] < HASTA)].copy()
    v["peso"] = v["peso"] / v["peso"].sum()
    v["viajes"] = (v["peso"] * VIAJES).round().astype(int)

    advertencia = ADVERTENCIA.format(red=red.name)
    if "--" in advertencia:
        raise ValueError("La advertencia del .rou.xml no puede contener '--'.")

    rng = random.Random(SEMILLA)
    lineas = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f"<!--{advertencia}-->",
        '<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        '        xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">',
        "",
    ]

    n_flows = emitidos = 0
    for _, fila in v.iterrows():
        hora, total_hora = int(fila["hora"]), int(fila["viajes"])
        if total_hora <= 0:
            continue
        base, resto = divmod(total_hora, PARES_POR_HORA)
        for i in range(PARES_POR_HORA):
            n = base + (1 if i < resto else 0)
            if n <= 0:
                continue
            origen = rng.choice(entradas)
            candidatos = [s for s in salidas if s != origen]
            if not candidatos:
                continue
            lineas.append(
                f'    <flow id="f_{hora:02d}_{i:02d}" type="privado" '
                f'begin="{hora*3600}" end="{hora*3600+3600}" number="{n}" '
                f'from="{origen}" to="{rng.choice(candidatos)}" '
                f'departLane="best" departSpeed="max"/>'
            )
            n_flows += 1
            emitidos += n

    lineas += ["", "</routes>", ""]
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(lineas), encoding="utf-8")

    return {
        "flows": n_flows,
        "viajes": emitidos,
        "pico_hora": int(v.loc[v["viajes"].idxmax(), "hora"]),
        "pico_viajes": int(v["viajes"].max()),
    }
