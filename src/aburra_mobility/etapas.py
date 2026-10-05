"""El pipeline, etapa por etapa."""

from __future__ import annotations

import shutil
from pathlib import Path

from . import entorno, rutas
from .errores import ErrorPipeline


def titulo(texto: str):
    print("\n" + "=" * 62)
    print(texto)
    print("=" * 62)


def _requerir_archivos(*archivos: Path, comando: str):
    faltan = [a for a in archivos if not a.exists()]
    if faltan:
        raise ErrorPipeline("faltan insumos:\n  " + "\n  ".join(str(f) for f in faltan)
                            + f"\nCorre primero: python main.py {comando}")


def extraer_encuesta():
    from .encuesta.informe_agregado import extraer

    titulo("EXTRACCION DE LA ENCUESTA — informe .xlsx -> CSV")
    extraer(rutas.INFORME, rutas.PROCESADOS)


def preparar_insumos():
    from .demanda.perfil_horario import calcular_perfil
    from .simulacion.tipos_vehiculo import cuotas_vehiculares, escribir_vtypes
    from .supuestos import RegistroSupuestos, escribir_supuestos_insumos

    titulo("INSUMOS SUMO — tipos de vehiculo y perfil horario")
    _requerir_archivos(rutas.PROCESADOS / "modo_principal.csv",
                       rutas.PROCESADOS / "distribucion_horaria.csv",
                       comando="extraer-encuesta")
    rutas.ESCENARIOS.mkdir(parents=True, exist_ok=True)

    supuestos = RegistroSupuestos()
    cuotas = cuotas_vehiculares(rutas.PROCESADOS, supuestos)
    print()
    perfil = calcular_perfil(rutas.PROCESADOS, rutas.PERFIL_SALIDAS, supuestos)
    escribir_vtypes(cuotas, rutas.VTYPES, supuestos)
    escribir_supuestos_insumos(rutas.SUPUESTOS, cuotas, supuestos)

    print(f"Composicion del privado motorizado: "
          f"{cuotas['share_auto']*100:.1f} % auto / {cuotas['share_moto']*100:.1f} % moto")
    print(f"Volumen privado a simular: {cuotas['viajes_privados']:,.0f} viajes/dia")
    pico = perfil.loc[perfil["w_privado"].idxmax()]
    print(f"Hora pico del privado: {int(pico['hora'])}:00 "
          f"({pico['w_privado']*100:.1f} % de las salidas del dia)")
    print(f"\nEscritos en {rutas.ESCENARIOS}/: {rutas.VTYPES.name}, "
          f"{rutas.PERFIL_SALIDAS.name}, {rutas.SUPUESTOS.name}")
    print(f"{len(supuestos)} supuestos registrados.")


def construir_red(municipios: list[str], archivo_osm: Path | None = None,
                  forzar_descarga: bool = False, adivinar_semaforos: bool = False) -> Path:
    """Red de uno o varios municipios; con varios queda una sola red conectada."""
    from .red.municipios import buscar_municipios

    titulo("RED VIAL — OPENSTREETMAP -> SUMO")
    entorno.requerir_sumo("netconvert", "sumo")
    entorno.requerir_pyproj()
    from .red.construccion import construir_red_osm

    red = construir_red_osm(buscar_municipios(municipios), rutas.OSM, rutas.REDES,
                            archivo_osm, forzar_descarga, adivinar_semaforos)
    print("\nRevisa el reporte de calidad antes de usar la red.")
    return red


def prueba_tecnica(red: Path | None = None) -> Path:
    """Escenario de prueba sobre una red: perfil temporal real, espacio inventado."""
    from .demanda.demanda_sintetica import DESDE, HASTA, escribir_flujos
    from .red.conectividad import ids_de_borde
    from .red.reticula import generar_reticula
    from .simulacion.configuracion import escribir_sumocfg

    titulo("PRUEBA TECNICA — demanda sintetica sobre la red")
    _requerir_archivos(rutas.PERFIL_SALIDAS, rutas.VTYPES, comando="preparar-insumos")
    if red is None:
        entorno.requerir_sumo("netgenerate")
        red = generar_reticula(rutas.RETICULA)
    else:
        entorno.requerir_sumo()
        if not red.exists():
            raise ErrorPipeline(f"no existe {red}\nPara la red OSM corre: "
                                "python main.py construir-red")
        print(f"Red: {red}")

    entradas, salidas = ids_de_borde(red)
    print(f"  {len(entradas)} aristas de entrada, {len(salidas)} de salida")

    print("\nGenerando demanda desde el perfil horario real...")
    rou = rutas.PRUEBA_TECNICA / "demanda_sintetica.rou.xml"
    info = escribir_flujos(entradas, salidas, rutas.PERFIL_SALIDAS, rou, red)
    print(f"  ventana {DESDE}:00-{HASTA}:00")
    print(f"  {info['flows']} flows, {info['viajes']} viajes")
    print(f"  hora pico: {info['pico_hora']}:00 con {info['pico_viajes']} viajes")

    cfg = rutas.PRUEBA_TECNICA / "prueba_tecnica.sumocfg"
    escribir_sumocfg(cfg, red, rou, rutas.VTYPES, DESDE, HASTA,
                     nota=f"Configuracion de PRUEBA TECNICA. Ver la advertencia en {rou.name}")
    print(f"\nConfiguracion escrita: {cfg}")
    print("\nRECORDATORIO: perfil temporal real, estructura espacial inventada.")
    print("Es una prueba tecnica, no un modelo de Medellin.")
    return cfg


def simular(cfg: Path | None = None, gui: bool = False):
    from .simulacion.ejecucion import UMBRAL_TELEPORTS, abrir_gui, correr_sumo

    cfg = cfg or rutas.PRUEBA_TECNICA / "prueba_tecnica.sumocfg"
    titulo("SIMULACION")
    entorno.requerir_sumo("sumo")
    if gui:
        print(f"Abriendo sumo-gui con {cfg.name}...")
        abrir_gui(cfg)
        return

    print(f"Corriendo {cfg.name} (sin interfaz)...")
    e = correr_sumo(cfg)
    print(f"  vehiculos insertados : {e.insertados} de {e.cargados}")
    print(f"  en ruta al terminar  : {e.en_ruta_al_final}")
    print(f"  teleports            : {e.teleports} ({e.fraccion_teleports:.1%}; "
          f"{e.teleports_atasco} por atasco)")
    print(f"  colisiones           : {e.colisiones}")
    print(f"  duracion media       : {e.duracion_media_s:.0f} s "
          f"(perdida {e.perdida_media_s:.0f} s)")
    if e.teleports_en_masa:
        print(f"\nAVISO: mas del {UMBRAL_TELEPORTS:.0%} de los vehiculos se teletransporto. "
              "Revisa el reporte de calidad de la red antes de interpretar nada.")
    print("\nRECORDATORIO: la demanda es sintetica; estas cifras solo prueban la "
          "cadena de herramientas.")
    return e


def limpiar():
    """Borra lo regenerable de data/processed y los __pycache__."""
    borrados = 0
    for csv in rutas.PROCESADOS.glob("*.csv"):
        csv.unlink()
        borrados += 1
    for cache in rutas.RAIZ.rglob("__pycache__"):
        if "venv" not in cache.parts:
            shutil.rmtree(cache, ignore_errors=True)
    print(f"{borrados} CSV borrados. data/raw/, data/osm/ y scenarios/ intactos.")
