"""Ejecucion de SUMO y lectura de sus estadisticas."""

from __future__ import annotations

import shutil
import subprocess
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

from ..errores import ErrorPipeline

UMBRAL_TELEPORTS = 0.01


@dataclass
class Estadisticas:
    cargados: int
    insertados: int
    en_ruta_al_final: int
    teleports: int
    teleports_atasco: int
    colisiones: int
    duracion_media_s: float
    perdida_media_s: float

    @property
    def fraccion_teleports(self) -> float:
        return self.teleports / self.insertados if self.insertados else 0.0

    @property
    def teleports_en_masa(self) -> bool:
        return self.fraccion_teleports > UMBRAL_TELEPORTS


def _leer_estadisticas(xml: Path) -> Estadisticas:
    raiz = ET.parse(xml).getroot()
    veh = raiz.find("vehicles")
    tel = raiz.find("teleports")
    viajes = raiz.find("vehicleTripStatistics")
    if veh is None or tel is None or viajes is None:
        raise ErrorPipeline(f"SUMO no escribio estadisticas completas en {xml}")
    return Estadisticas(
        cargados=int(veh.get("loaded")),
        insertados=int(veh.get("inserted")),
        en_ruta_al_final=int(veh.get("running")),
        teleports=int(tel.get("total")),
        teleports_atasco=int(tel.get("jam")),
        colisiones=int(raiz.find("safety").get("collisions")),
        duracion_media_s=float(viajes.get("duration")),
        perdida_media_s=float(viajes.get("timeLoss")),
    )


def correr_sumo(sumocfg: Path) -> Estadisticas:
    """Corre la simulacion sin interfaz y devuelve sus estadisticas."""
    if not sumocfg.exists():
        raise ErrorPipeline(f"no existe {sumocfg}\nCorre primero: python main.py prueba-tecnica")
    stats = sumocfg.with_name(sumocfg.stem + "_estadisticas.xml")
    log = sumocfg.with_name(sumocfg.stem + "_sumo.log")
    r = subprocess.run(["sumo", "-c", sumocfg.name, "--statistic-output", stats.name],
                       cwd=sumocfg.parent, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    log.write_text(r.stdout + r.stderr, encoding="utf-8")
    if r.returncode != 0:
        errores = [l for l in (r.stdout + r.stderr).splitlines() if l.startswith("Error")]
        raise ErrorPipeline("SUMO termino con error:\n  " + "\n  ".join(errores[:5])
                            + f"\nSalida completa en {log}")
    return _leer_estadisticas(stats)


def abrir_gui(sumocfg: Path):
    gui = shutil.which("sumo-gui")
    if gui is None:
        raise ErrorPipeline("no se encontro 'sumo-gui' en el PATH.")
    subprocess.Popen([gui, "-c", sumocfg.name], cwd=sumocfg.parent)
