"""Archivo .sumocfg: reune red, demanda y tipos de vehiculo en un solo archivo."""

from __future__ import annotations

import os
from pathlib import Path


def _relativa(ruta: Path, base: Path) -> str:
    return Path(os.path.relpath(ruta, base)).as_posix()


def escribir_sumocfg(destino: Path, red: Path, rutas_rou: Path, adicionales: Path,
                     desde_h: int, hasta_h: int, nota: str):
    base = destino.parent
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<!-- {nota} -->
<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/sumoConfiguration.xsd">
    <input>
        <net-file value="{_relativa(red, base)}"/>
        <route-files value="{_relativa(rutas_rou, base)}"/>
        <additional-files value="{_relativa(adicionales, base)}"/>
    </input>
    <time>
        <begin value="{desde_h * 3600}"/>
        <end value="{hasta_h * 3600}"/>
        <step-length value="1.0"/>
    </time>
    <processing>
        <!-- Habilita el modelo sublane, que es lo que permite a la moto
             filtrarse entre carriles. Sin esto los parametros latAlignment
             y minGapLat de vtypes.add.xml se ignoran por completo. -->
        <lateral-resolution value="0.8"/>
        <ignore-route-errors value="true"/>
        <time-to-teleport value="300"/>
    </processing>
    <report>
        <verbose value="true"/>
        <no-step-log value="true"/>
        <duration-log.statistics value="true"/>
    </report>
</configuration>
""", encoding="utf-8")
