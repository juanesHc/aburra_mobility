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


def demanda_od(red: Path, beta: float | None, escala: float, desde: int, hasta: int,
               semilla: int) -> Path:
    """Demanda estimada con modelo gravitacional + Furness, sorteada con una semilla."""
    import pandas as pd

    from .demanda.gravitacional import (BETA, MatrizODGravitacional, gravitacional, resumen,
                                        sensibilidad, vehiculos_privados_dia)
    from .demanda.impedancia import tiempos_entre_zonas
    from .demanda.muestreo import (ADVERTENCIA, correr_od2trips, escribir_relaciones,
                                   sortear)
    from .demanda.reporte_od import DatosDemanda, escribir_reporte, supuestos_demanda
    from .red.conectividad import analizar_conectividad
    from .simulacion.configuracion import escribir_sumocfg
    from .zonas.limites import descargar_limites
    from .zonas.macrozonas import marginales, zonas_modelo
    from .zonas.taz import aristas_por_zona, escribir_taz

    titulo("DEMANDA ESTIMADA — modelo gravitacional + Furness")
    beta = BETA if beta is None else beta
    entorno.requerir_sumo("od2trips", "sumo")
    entorno.requerir_pyproj()
    import sumolib

    _requerir_archivos(rutas.PERFIL_SALIDAS, rutas.VTYPES, comando="preparar-insumos")
    _requerir_archivos(rutas.PROCESADOS / "macrozonas_od.csv", comando="extraer-encuesta")
    if not red.exists():
        raise ErrorPipeline(f"no existe {red}\nCorre primero: python main.py construir-red valle")
    carpeta = rutas.DEMANDA_OD
    carpeta.mkdir(parents=True, exist_ok=True)

    print(f"\n[1/5] Zonas sobre {red.name}")
    zonas = zonas_modelo()
    limites = descargar_limites([z.relacion_osm for z in zonas], rutas.LIMITES_ZONAS)
    net = sumolib.net.readNet(str(red))
    nucleo = analizar_conectividad(net).fuertes[0]
    por_zona = aristas_por_zona(net, zonas, limites, nucleo)
    nombres = {z.id: z.nombre for z in zonas}
    sin_calles = [nombres[z.id] for z in zonas if z.id not in por_zona]
    taz = carpeta / "zonas.taz.xml"
    escribir_taz(por_zona, taz)
    print(f"  {len(por_zona)} de {len(zonas)} zonas con calles en la red -> {taz.name}")
    if sin_calles:
        print(f"  AVISO: sin calles en esta red: {', '.join(sin_calles)}. Sus viajes se omiten.")
    if len(por_zona) < 2:
        raise ErrorPipeline("la red cubre menos de dos zonas: usa la red del valle "
                            "(python main.py construir-red valle)")

    print("\n[2/5] Tiempos entre zonas (flujo libre)")
    tiempos = tiempos_entre_zonas(net, por_zona)
    if tiempos.isna().to_numpy().any():
        raise ErrorPipeline("hay pares de zonas sin camino en la red")
    tiempos.round(2).to_csv(carpeta / "tiempos_entre_zonas.csv", encoding="utf-8")
    print(f"  entre {tiempos.to_numpy().min():.1f} y {tiempos.to_numpy().max():.1f} min")

    print("\n[3/5] Matriz OD diaria")
    marg = marginales(rutas.PROCESADOS)
    viajes, iteraciones = gravitacional(tiempos, marg, beta)
    perfil = pd.read_csv(rutas.PERFIL_SALIDAS).set_index("hora")["w_privado"]
    matriz = MatrizODGravitacional(viajes, vehiculos_privados_dia(rutas.PROCESADOS), perfil, beta)
    matriz.validar()
    matriz.matriz().round(3).to_csv(carpeta / "matriz_od_diaria.csv", encoding="utf-8")
    r = resumen(viajes, tiempos)
    print(f"  beta = {beta}/min, Furness en {iteraciones} iteraciones")
    print(f"  {matriz.matriz().to_numpy().sum():,.0f} vehiculos privados/dia, "
          f"{r['intrazonal']:.1%} dentro de su zona")
    print(f"  tiempo medio a flujo libre {r['tiempo_libre_min']:.1f} min "
          f"(factor implicito {r['factor_implicito']:.2f})")

    print(f"\n[4/5] Sorteo de la semilla {semilla} ({escala:.0%}, {desde}:00-{hasta}:00)")
    conteos = sortear(matriz, desde, hasta, escala, semilla)
    relaciones = carpeta / "vehiculos_por_hora.xml"
    escribir_relaciones(conteos, relaciones)
    viajes_xml = carpeta / "demanda_od.trips.xml"
    advertencia = ADVERTENCIA.format(beta=beta, zonas=len(por_zona), escala=f"{escala:.0%}",
                                     semilla=semilla)
    correr_od2trips(taz, relaciones, viajes_xml, semilla, advertencia)
    sorteados = sum(c[3] for c in conteos)
    print(f"  {sorteados:,} vehiculos -> {viajes_xml.name}")

    print("\n[5/5] Configuracion y reporte")
    cfg = carpeta / "demanda_od.sumocfg"
    escribir_sumocfg(cfg, red, viajes_xml, rutas.VTYPES, desde, hasta,
                     nota=f"Demanda ESTIMADA. Ver la advertencia en {viajes_xml.name}")
    reporte = carpeta / "demanda_od.md"
    escribir_reporte(reporte, DatosDemanda(
        red=red, nombres=nombres,
        km_por_zona={z: sum(e.getLength() for e in es) / 1000 for z, es in por_zona.items()},
        sin_calles=sin_calles, marg=marg, tiempos=tiempos, matriz=matriz,
        iteraciones=iteraciones, sensibilidad=sensibilidad(tiempos, marg), desde=desde,
        hasta=hasta, escala=escala, semilla=semilla, sorteados=sorteados,
    ), supuestos_demanda(beta, escala))
    print(f"  {cfg}\n  {reporte}")
    print("\nRECORDATORIO: matriz estimada con beta sin calibrar; ver el reporte.")
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
    if cfg.parent == rutas.DEMANDA_OD:
        print("\nRECORDATORIO: la matriz es estimada y la demanda va a escala sin reducir la "
              "capacidad de las vias; ver demanda_od.md.")
    else:
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
