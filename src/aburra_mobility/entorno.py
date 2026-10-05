"""Verificacion del entorno y acceso a las herramientas de SUMO."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from . import rutas
from .errores import ErrorPipeline

VERSION_SUMO = "1.27.1"


def sumo_home() -> Path:
    home = os.environ.get("SUMO_HOME")
    if not home or not Path(home).exists():
        raise ErrorPipeline("la variable SUMO_HOME no esta definida o no apunta a una "
                            "instalacion de SUMO.")
    return Path(home)


def habilitar_sumolib():
    """Agrega SUMO_HOME/tools al path si sumolib no se puede importar."""
    try:
        import sumolib
    except ImportError:
        sys.path.append(str(sumo_home() / "tools"))
        try:
            import sumolib
        except ImportError as e:
            raise ErrorPipeline(f"no se pudo importar sumolib desde {sumo_home() / 'tools'}") from e


def requerir_sumo(*ejecutables: str):
    """Falla con un mensaje util si falta SUMO o alguno de sus ejecutables."""
    faltan = [e for e in ejecutables if shutil.which(e) is None]
    if faltan:
        raise ErrorPipeline(f"no estan en el PATH: {', '.join(faltan)}\n"
                            f"Instala SUMO {VERSION_SUMO} y abre una terminal nueva.")
    sumo_home()
    habilitar_sumolib()


def requerir_pyproj():
    try:
        import pyproj
    except ImportError as e:
        raise ErrorPipeline("falta pyproj: pip install -r requirements.txt") from e


def verificar() -> bool:
    """Revision completa del entorno. Devuelve True si todo esta bien."""
    problemas = []

    v = sys.version_info
    ok = (v.major, v.minor) >= (3, 11)
    print(f"\n[{'OK' if ok else '--'}] Python {v.major}.{v.minor}.{v.micro}")
    print(f"     {sys.executable}")
    if not ok:
        problemas.append("Python 3.11 o superior es necesario.")

    en_venv = sys.prefix != sys.base_prefix
    print(f"\n[{'OK' if en_venv else '  '}] Entorno virtual "
          f"{'activado' if en_venv else 'NO activado'}")
    if not en_venv:
        print("     Funciona igual, pero conviene activarlo:")
        print("     venv\\Scripts\\Activate.ps1   (Windows)")

    for paquete in ["pandas", "openpyxl", "pyproj"]:
        try:
            mod = __import__(paquete)
            print(f"\n[OK] {paquete} {getattr(mod, '__version__', '')}")
        except ImportError:
            print(f"\n[--] {paquete} NO instalado")
            problemas.append(f"Falta {paquete}: pip install -r requirements.txt")

    if rutas.INFORME.exists():
        print(f"\n[OK] Informe encontrado ({rutas.INFORME.stat().st_size // 1024} KB)")
    else:
        print("\n[--] Informe NO encontrado")
        print(f"     Se espera en: {rutas.INFORME}")
        problemas.append("Copia el informe .xlsx a data/raw/")

    if shutil.which("sumo"):
        r = subprocess.run(["sumo", "--version"], capture_output=True, text=True)
        version = r.stdout.split("\n")[0] if r.returncode == 0 else "?"
        print(f"\n[OK] SUMO disponible\n     {version}")
        if VERSION_SUMO not in version:
            print(f"     AVISO: el proyecto fija SUMO {VERSION_SUMO}; los resultados "
                  "pueden diferir con otra version.")
        try:
            sumo_home()
            habilitar_sumolib()
            print(f"[OK] SUMO_HOME y sumolib: {sumo_home()}")
        except ErrorPipeline as e:
            print(f"[--] {e}")
            problemas.append(str(e))
    else:
        print("\n[--] SUMO no esta en el PATH")
        print("     Solo corren extraer-encuesta y preparar-insumos sin SUMO.")
        problemas.append(f"Instala SUMO {VERSION_SUMO} para red y simulacion.")

    print()
    if problemas:
        print("HAY QUE RESOLVER:")
        for p in problemas:
            print(f"  - {p}")
        return False
    return True
