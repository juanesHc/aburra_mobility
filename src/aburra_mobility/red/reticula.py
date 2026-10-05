"""Reticula sintetica con netgenerate."""

from __future__ import annotations

import subprocess
from pathlib import Path

from ..errores import ErrorPipeline

LADO = 5
LARGO = 300.0


def generar_reticula(destino: Path) -> Path:
    destino.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "netgenerate",
        "--grid",
        "--grid.number", str(LADO),
        "--grid.length", str(LARGO),
        "--grid.attach-length", "200",
        "--default.lanenumber", "2",
        "--default.speed", "13.89",
        "--tls.guess", "true",
        "--tls.default-type", "static",
        "--no-turnarounds", "true",
        "--output-file", str(destino),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise ErrorPipeline(f"netgenerate fallo:\n{r.stderr}")
    print(f"Reticula generada: {destino.name}  ({LADO}x{LADO}, 2 carriles)")
    return destino
