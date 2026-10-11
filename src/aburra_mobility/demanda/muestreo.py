"""Sorteo de los viajes de una corrida a partir de la matriz esperada."""

from __future__ import annotations

import subprocess
from pathlib import Path

import numpy as np

from ..errores import ErrorPipeline
from .gravitacional import MatrizODGravitacional

ADVERTENCIA = """
  ==================================================================
  DEMANDA ESTIMADA - NO ES UNA MATRIZ OBSERVADA

  Totales por zona y perfil horario: informe EOD 2025 AMVA.
  Reparto entre pares de zonas: modelo gravitacional + Furness,
  con beta = {beta} por minuto SIN CALIBRAR.
  Zonas: {zonas} (Bello, Itagui y Envigado van como un solo bloque).
  Escala: {escala} de los vehiculos reales. Semilla: {semilla}.

  Ver scenarios/demanda_od/demanda_od.md antes de usar resultados.
  ==================================================================
"""


def sortear(matriz: MatrizODGravitacional, desde: int, hasta: int, escala: float,
            semilla: int) -> list[tuple[int, str, str, int]]:
    """Vehiculos por hora y par de zonas: un sorteo de Poisson alrededor de lo esperado."""
    rng = np.random.default_rng(semilla)
    zonas = matriz.zonas()
    conteos = []
    for h in range(desde, hasta):
        n = rng.poisson(matriz.matriz(h).to_numpy() * escala)
        for i, j in zip(*np.nonzero(n)):
            conteos.append((h, zonas[i], zonas[j], int(n[i, j])))
    return conteos


def escribir_relaciones(conteos: list[tuple[int, str, str, int]], destino: Path):
    """Conteos en formato tazRelation, un intervalo por hora."""
    lineas = ['<?xml version="1.0" encoding="UTF-8"?>', "<data>"]
    for h in sorted({c[0] for c in conteos}):
        lineas.append(f'    <interval id="h{h:02d}" begin="{h * 3600}" end="{(h + 1) * 3600}">')
        lineas += [f'        <tazRelation from="{o}" to="{d}" count="{n}"/>'
                   for hh, o, d, n in conteos if hh == h]
        lineas.append("    </interval>")
    lineas += ["</data>", ""]
    destino.write_text("\n".join(lineas), encoding="utf-8")


def correr_od2trips(taz: Path, relaciones: Path, salida: Path, semilla: int, advertencia: str):
    """od2trips elige la calle de origen y destino y el segundo de salida de cada vehiculo."""
    if "--" in advertencia:
        raise ValueError("La advertencia del archivo de viajes no puede contener '--'.")
    cmd = ["od2trips", "--taz-files", str(taz), "--tazrelation-files", str(relaciones),
           "--output-file", str(salida), "--seed", str(semilla), "--spread.uniform",
           "--different-source-sink", "--vtype", "privado", "--prefix", "od",
           "--departlane", "best", "--departspeed", "max", "--no-step-log"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise ErrorPipeline(f"od2trips fallo:\n{(r.stdout + r.stderr)[-2000:]}")
    texto = salida.read_text(encoding="utf-8")
    inicio = texto.index("?>") + 2 if texto.startswith("<?xml") else 0
    salida.write_text(texto[:inicio] + f"\n<!--{advertencia}-->" + texto[inicio:], encoding="utf-8")
