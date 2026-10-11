"""Construccion de la demanda estimada: zonas, tiempos, matriz, sorteo y reporte."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from ..errores import ErrorPipeline
from ..red.conectividad import analizar_conectividad
from ..simulacion.configuracion import escribir_sumocfg
from ..zonas.limites import descargar_limites
from ..zonas.macrozonas import marginales, zonas_modelo
from ..zonas.taz import aristas_por_zona, escribir_taz
from .gravitacional import (MatrizODGravitacional, gravitacional, resumen, sensibilidad,
                            vehiculos_privados_dia)
from .impedancia import tiempos_entre_zonas
from .muestreo import ADVERTENCIA, correr_od2trips, escribir_relaciones, sortear
from .reporte_od import DatosDemanda, escribir_reporte, supuestos_demanda


def construir_demanda_od(red: Path, carpeta: Path, procesados: Path, perfil_csv: Path,
                         vtypes: Path, cache_limites: Path, beta: float, escala: float,
                         desde: int, hasta: int, semilla: int) -> Path:
    """Escribe en la carpeta la demanda de una semilla y su .sumocfg; devuelve el .sumocfg."""
    import sumolib

    carpeta.mkdir(parents=True, exist_ok=True)

    print(f"\n[1/5] Zonas sobre {red.name}")
    zonas = zonas_modelo()
    limites = descargar_limites([z.relacion_osm for z in zonas], cache_limites)
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
    marg = marginales(procesados)
    viajes, iteraciones = gravitacional(tiempos, marg, beta)
    perfil = pd.read_csv(perfil_csv).set_index("hora")["w_privado"]
    matriz = MatrizODGravitacional(viajes, vehiculos_privados_dia(procesados), perfil, beta)
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
    escribir_sumocfg(cfg, red, viajes_xml, vtypes, desde, hasta,
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
    return cfg
