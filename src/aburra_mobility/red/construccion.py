"""Construccion de la red vial de un municipio desde OpenStreetMap."""

from __future__ import annotations

from pathlib import Path

from .aristas import carriles_por_defecto, km
from .calidad import DatosReporte, advertencias_al_cargar, escribir_reporte, supuestos_red
from .conectividad import aristas_de_borde, analizar_conectividad
from .conversion_osm import (ANCHO_CARRIL_COMPARTIDO, ajustar_red, carriles_compartidos, convertir,
                             salidas_de_glorieta)
from .datos_osm import leer_osm
from .descarga_osm import obtener_osm
from ..errores import ErrorPipeline
from .municipios import Municipio, clave_red


def construir_red_osm(municipios: list[Municipio], carpeta_osm: Path, carpeta_redes: Path,
                      archivo_osm: Path | None = None, forzar_descarga: bool = False,
                      adivinar_semaforos: bool = False) -> Path:
    """Red de uno o varios municipios."""
    import sumolib

    if archivo_osm and len(municipios) > 1:
        raise ErrorPipeline("--osm solo sirve con un municipio: el archivo local no dice "
                            "a que municipio corresponde cada parte.")
    clave = clave_red(municipios)
    carpeta_redes.mkdir(parents=True, exist_ok=True)
    red = carpeta_redes / f"{clave}.net.xml"
    sin_podar = carpeta_redes / f"{clave}_sin_podar.net.xml"
    log = carpeta_redes / f"{clave}_netconvert.log"
    reporte = carpeta_redes / f"{clave}_calidad.md"

    print("\n[1/4] Datos OSM")
    osms = []
    for mun in municipios:
        if len(municipios) > 1:
            print(f"  {mun.nombre}:")
        osms.append(obtener_osm(mun, carpeta_osm, archivo_osm, forzar_descarga))

    print("\n[2/4] Conversion con netconvert")
    log.write_text("", encoding="utf-8")
    salida = convertir(osms, sin_podar, log, adivinar_semaforos)
    n_adv = sum(1 for l in salida.splitlines() if l.startswith("Warning"))
    print(f"  {sin_podar.name} ({n_adv} lineas de advertencia, ver {log.name})")

    print("\n[3/4] Conectividad")
    net_sin_podar = sumolib.net.readNet(str(sin_podar))
    conect = analizar_conectividad(net_sin_podar)
    print(f"  {len(conect.debiles)} componentes debiles, {len(conect.fuertes)} fuertes; "
          f"el mayor fuerte tiene {len(conect.fuertes[0])} de "
          f"{len(net_sin_podar.getEdges())} aristas")
    compartidos = carriles_compartidos(net_sin_podar, excluir=conect.podar)
    salidas = salidas_de_glorieta(net_sin_podar, excluir=conect.podar)
    ajustar_red(sin_podar, red, conect.podar, compartidos, salidas, log)
    print(f"  {len(conect.podar)} aristas podadas, {len(compartidos)} con carril "
          f"compartido ensanchadas a {ANCHO_CARRIL_COMPARTIDO} m, {len(salidas)} salidas de "
          f"glorieta habilitadas desde el segundo carril -> {red.name}")

    net = sumolib.net.readNet(str(red), withPrograms=True)
    residual = analizar_conectividad(net).podar
    if residual:
        print(f"  AVISO: tras podar quedan {len(residual)} aristas no ruteables.")

    print("\n[4/4] Reporte de calidad")
    datos = DatosReporte(
        municipios=municipios, clave=clave, osms=osms, red=red, red_sin_podar=sin_podar,
        net=net, net_sin_podar=net_sin_podar, resumen_osm=leer_osm(osms),
        conectividad=conect, ensanchadas=sorted(compartidos), salidas_glorieta=salidas,
        salida_netconvert=salida,
        adivinar_semaforos=adivinar_semaforos,
        advertencias_carga=advertencias_al_cargar(red),
        supuestos=supuestos_red(adivinar_semaforos),
    )
    sem, frontera = escribir_reporte(reporte, datos)

    edges = net.getEdges()
    ent, sal = aristas_de_borde(net)
    print(f"  {len(net.getNodes())} nodos, {len(edges)} aristas, "
          f"{km(edges):.1f} km por sentido")
    print(f"  semaforos: {sem.total} ({len(sem.desde_osm)} de OSM, "
          f"{len(sem.adivinados)} adivinados); planes reales: 0")
    print(f"  aristas con carriles por defecto: "
          f"{sum(map(carriles_por_defecto, edges))} de {len(edges)}")
    print(f"  bordes: {len(ent)} entradas, {len(sal)} salidas")
    print(f"  advertencias al cargar en sumo: {len(datos.advertencias_carga)}")
    if frontera:
        for nombre, en_nucleo in frontera.items():
            print(f"  {nombre}: {en_nucleo:.1%} de sus km en el nucleo conectado comun")
    print(f"  Reporte: {reporte}")
    return red
