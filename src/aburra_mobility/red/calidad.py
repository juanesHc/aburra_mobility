"""Reporte de calidad de la red vial: redes/<municipio>_calidad.md."""

from __future__ import annotations

import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

from ..supuestos import RegistroSupuestos
from .aristas import (
    ANCHO_AUTO, carriles_por_defecto, es_arterial, km, mas_angosta_que_un_auto,
    tipo_corto, velocidad_por_defecto, vias_osm,
)
from .conectividad import Conectividad, aristas_de_borde
from .conversion_osm import ANCHO_CARRIL_COMPARTIDO, JOIN_DIST
from .datos_osm import ResumenOSM
from .municipios import Municipio
from .semaforos import DIST_SENAL_OSM, Semaforos, clasificar_semaforos

MAX_ENLACES = 40


@dataclass
class DatosReporte:
    municipios: list[Municipio]
    clave: str
    osms: list[Path]
    red: Path
    red_sin_podar: Path
    net: object
    net_sin_podar: object
    resumen_osm: ResumenOSM
    conectividad: Conectividad
    ensanchadas: list[str]
    salida_netconvert: str
    adivinar_semaforos: bool
    advertencias_carga: list[str]
    supuestos: RegistroSupuestos


def _tabla(encabezado: list[str], filas: list[list]) -> list[str]:
    lineas = ["| " + " | ".join(encabezado) + " |",
              "|" + "|".join("---" if i == 0 else "---:" for i in range(len(encabezado))) + "|"]
    lineas += ["| " + " | ".join(str(c) for c in f) + " |" for f in filas]
    return lineas + [""]


def _pct(a, b) -> str:
    return f"{100 * a / b:.1f} %" if b else "—"


def _enlaces_osm(ids, tipo: str, maximo: int = MAX_ENLACES) -> list[str]:
    ids = list(ids)
    lineas = ["- " + ", ".join(f"[{i}](https://www.openstreetmap.org/{tipo}/{i})"
                               for i in ids[:maximo])]
    if len(ids) > maximo:
        lineas.append(f"- … y {len(ids) - maximo} más")
    return lineas + [""]


def advertencias_al_cargar(red: Path) -> list[str]:
    """Carga la red en sumo como lo haria sumo-gui y devuelve las advertencias y errores."""
    r = subprocess.run(["sumo", "--net-file", str(red), "--end", "1",
                        "--no-step-log", "true"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    lineas = [l for l in (r.stdout + r.stderr).splitlines()
              if l.startswith(("Warning", "Error"))]
    if r.returncode != 0:
        lineas.insert(0, f"Error: sumo termino con codigo {r.returncode}")
    return lineas


def resumen_advertencias(salida: str) -> list[tuple[str, int]]:
    """Agrupa las advertencias de netconvert por tipo de mensaje."""
    tipos = Counter()
    for l in salida.splitlines():
        m = re.match(r"Warning: (\d+) total messages of type: (.*)", l)
        if m:
            tipos[m.group(2)] += int(m.group(1)) - 5
            continue
        if l.startswith("Warning: "):
            patron = re.sub(r"'[^']*'|\b[\w#:.\-]*\d[\w#:.\-]*\b", "%", l[9:])
            tipos[patron] += 1
    return tipos.most_common()


def _encabezado(d: DatosReporte) -> list[str]:
    L = [
        f"# Calidad de la red vial — {' + '.join(m.nombre for m in d.municipios)}",
        "",
        "Generado automáticamente por `python main.py construir-red`. No editar a mano:",
        "se sobrescribe en cada corrida.",
        "",
        "- Fuente: OpenStreetMap.",
    ]
    for m, osm in zip(d.municipios, d.osms):
        L.append(f"  - {m.nombre}: relación {m.relacion_osm} (DIVIPOLA {m.divipola}), "
                 f"`{osm.name}`, datos al {d.resumen_osm.fechas.get(osm.name, 'desconocida')}.")
    return L + [
        f"- Red: `{d.red.name}` (podada) y `{d.red_sin_podar.name}` (antes de podar).",
        f"- Tolerancia de unión de intersecciones: {JOIN_DIST:.0f} m. "
        f"`tls.guess`: {'activado' if d.adivinar_semaforos else 'desactivado'}.",
        "",
    ]


def _seccion_resumen(d: DatosReporte) -> list[str]:
    edges = d.net.getEdges()
    return ["## Resumen", ""] + _tabla(["", "valor"], [
        ["Nodos (intersecciones y extremos)", len(d.net.getNodes())],
        ["Aristas (un sentido cada una)", len(edges)],
        ["Longitud total por sentido", f"{km(edges):.1f} km"],
        ["Carril-km", f"{sum(e.getLength() * e.getLaneNumber() for e in edges) / 1000:.1f}"],
        ["Semáforos (controladores)", len(d.net.getTrafficLights())],
        ["Advertencias al cargar en sumo", len(d.advertencias_carga)],
    ]) + ["Los kilómetros se cuentan por sentido: una vía de doble sentido aporta dos veces",
          "su longitud. Es la medida que importa para capacidad.", ""]


def _seccion_carriles(d: DatosReporte) -> list[str]:
    edges = d.net.getEdges()
    por_tipo = defaultdict(list)
    for e in edges:
        por_tipo[tipo_corto(e)].append(e)

    filas = []
    for t in sorted(por_tipo, key=lambda t: -km(por_tipo[t])):
        es = por_tipo[t]
        sin_carriles = [e for e in es if carriles_por_defecto(e)]
        sin_vel = [e for e in es if velocidad_por_defecto(e)]
        filas.append([t, len(es), f"{km(es):.1f}",
                      f"{sum(e.getLaneNumber() for e in es) / len(es):.2f}",
                      f"{len(sin_carriles)} ({_pct(km(sin_carriles), km(es))} de km)",
                      f"{len(sin_vel)} ({_pct(km(sin_vel), km(es))} de km)"])
    L = ["## Vías por tipo y carriles", ""]
    L += _tabla(["tipo", "aristas", "km", "carriles/sentido (media)",
                 "carriles por defecto", "velocidad por defecto"], filas)

    sin_carriles = [e for e in edges if carriles_por_defecto(e)]
    arterias = [e for e in edges if es_arterial(e)]
    art_sin = [e for e in arterias if carriles_por_defecto(e)]
    L += [
        f"**{len(sin_carriles)} de {len(edges)} aristas ({_pct(km(sin_carriles), km(edges))} "
        f"de los km) no tienen `lanes` en OSM** y netconvert les puso el valor del typemap "
        f"(1 carril por sentido en secundaria, terciaria y locales; 2 en primaria y troncal). "
        f"En la red arterial (troncal a terciaria) la cifra es {len(art_sin)} de "
        f"{len(arterias)} aristas ({_pct(km(art_sin), km(arterias))} de los km).",
        "",
    ]

    por_carriles = Counter()
    for e in edges:
        por_carriles[min(e.getLaneNumber(), 3)] += e.getLength() / 1000
    L += _tabla(["carriles por sentido", "km", "% de la red"], [
        [("3 o más" if n == 3 else n), f"{v:.1f}", _pct(v, km(edges))]
        for n, v in sorted(por_carriles.items())
    ])
    anchos = Counter(round(l.getWidth(), 1) for e in edges for l in e.getLanes())
    L += [
        "Relevancia para la moto: con `lateral-resolution` 0,8 m el modelo sublane deja",
        "que la moto se filtre entre filas en vías de dos o más carriles por sentido. En",
        "vías de un carril solo puede adelantar dentro del mismo carril si el ancho lo",
        f"permite; OSM casi nunca trae `width`, así que los anchos de carril quedan en el "
        f"valor por defecto (distribución: "
        + ", ".join(f"{a} m: {n}" for a, n in anchos.most_common(4)) + ").",
        "Ningún parámetro del vType `moto` se tocó.",
        "",
    ]

    L += _subseccion_carril_compartido(d)
    return L


def _subseccion_carril_compartido(d: DatosReporte) -> list[str]:
    L = []
    if d.ensanchadas:
        originales = [d.net_sin_podar.getEdge(e) for e in d.ensanchadas]
        L += [
            f"**Calles de carril compartido: {len(originales)} aristas, "
            f"{km(originales):.2f} km.** Vienen de vías con `lanes=1` y doble sentido "
            "en OSM, sin `width`. netconvert las partía en dos carriles de "
            f"{min(l.getWidth() for e in originales for l in e.getLanes()):.1f} m, más "
            f"angostos que un auto ({ANCHO_AUTO} m); se ensancharon a "
            f"{ANCHO_CARRIL_COMPARTIDO} m por sentido (ver supuesto `carril_compartido`). "
            "Si alguna calle resulta ser de un solo sentido o más ancha, corregirla en OSM "
            "es mejor que ajustarla aquí:",
            "",
        ]
        L += _enlaces_osm(sorted({i for e in originales for i in vias_osm(e)}, key=int), "way")
    restantes = [e for e in d.net.getEdges() if mas_angosta_que_un_auto(e)]
    if restantes:
        L += [f"**AVISO: {len(restantes)} aristas siguen con carriles más angostos que un "
              "auto después del ajuste.** Revisar:", ""]
        L += _enlaces_osm(sorted({i for e in restantes for i in vias_osm(e)}, key=int), "way")
    elif d.ensanchadas:
        L += ["Tras el ajuste no queda ningún carril más angosto que un auto.", ""]
    return L


def _seccion_semaforos(d: DatosReporte, sem: Semaforos) -> list[str]:
    tipos_senal = Counter(s.tipo for s in d.resumen_osm.senales)
    L = ["## Semáforos", ""]
    L += _tabla(["", "valor"], [
        ["Nodos semáforo en OSM: `highway=traffic_signals`", tipos_senal["vehicular"]],
        ["Nodos semáforo en OSM: solo `crossing=traffic_signals` (peatonal)",
         tipos_senal["peatonal"]],
        ["Controladores en la red", sem.total],
        ["… ubicados a partir de OSM", len(sem.desde_osm)],
        ["… adivinados por `tls.guess` (sin señal OSM a "
         f"≤ {DIST_SENAL_OSM:.0f} m)", len(sem.adivinados)],
        ["Cruces controlados (tras `tls.join`)", sem.cruces_controlados],
        ["Señales OSM que no quedaron en ningún semáforo", len(sem.senales_sin_usar)],
        ["Controladores con plan real", "**0**"],
    ])
    if sem.ciclos:
        c = sorted(sem.ciclos)
        L += [f"Ciclos generados: mín {c[0]:.0f} s, mediana {c[len(c) // 2]:.0f} s, "
              f"máx {c[-1]:.0f} s. **Todos los planes semafóricos son inventados** por "
              "netconvert (tiempos fijos genéricos). Los planes reales de Medellín los "
              "tiene el SIMM y no son públicos en formato utilizable. Esto afecta "
              "directamente la capacidad de cada intersección semaforizada.", ""]
    if sem.senales_sin_usar:
        _marcar_glorietas(d.net, sem.senales_sin_usar)
        L += _subseccion_senales_descartadas(sem)
    return L


def _marcar_glorietas(net, senales):
    """Completa en_glorieta con lo que sabe la red."""
    import warnings

    en_glorieta = {e for r in net.getRoundabouts() for e in r.getEdges()}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for s in senales:
            x, y = net.convertLonLat2XY(s.lon, s.lat)
            if any(e.getID() in en_glorieta for e, _ in net.getNeighboringEdges(x, y, 5)):
                s.en_glorieta = True


def _causa_descarte(s) -> str:
    if s.en_glorieta:
        return "sobre el anillo de una glorieta"
    if s.grado >= 3:
        return "en un cruce (revisar)"
    if s.cruza_servicio:
        if s.grado == 0:
            return "sobre una vía de servicio, que no entra a la red"
        return "en el cruce con una vía de servicio, que no entra a la red"
    if s.grado <= 1:
        return "en el extremo de una vía (borde de la red o calle ciega)"
    if s.tipo == "peatonal":
        return "paso peatonal a mitad de cuadra"
    return "semáforo vehicular a mitad de vía"


def _subseccion_senales_descartadas(sem: Semaforos) -> list[str]:
    L = ["**Señales de OSM descartadas.** `tls.discard-simple` quita los semáforos que no",
         "están en un cruce. Conservarlos no mejora la red: recibirían un plan inventado",
         "(82 s verde, 3 s amarillo, 5 s rojo) y alteran la agrupación de cruces vecinos;",
         "en Sabaneta eso produjo entre 12 y 17 teleports por corrida. Su efecto real",
         "(pasos peatonales con fase propia, control de accesos) queda sin modelar.", ""]
    L += _tabla(["señal OSM", "tipo", "vía", "causa probable"], [
        [f"[{s.id}](https://www.openstreetmap.org/node/{s.id})", s.tipo,
         f"{s.via} ({s.tipo_via})", _causa_descarte(s)]
        for s in sorted(sem.senales_sin_usar, key=lambda s: (_causa_descarte(s), s.via))
    ])
    glorietas = sorted({s.via for s in sem.senales_sin_usar if s.en_glorieta})
    if glorietas:
        L += [f"**Glorietas con semáforos en el anillo: {', '.join(glorietas)}.** En la red "
              "funcionan como glorietas con prelación para quien va dentro, y en la realidad "
              "están semaforizadas. El plan semafórico de una glorieta no se puede adivinar: "
              "hay que construirlo a mano en netedit con los tiempos reales.", ""]
    return L


def _seccion_giros(d: DatosReporte) -> list[str]:
    r = d.resumen_osm.restricciones
    vt = d.resumen_osm.vias_por_tipo
    tl = d.resumen_osm.vias_con_turn_lanes
    cruces = sum(1 for n in d.net.getNodes()
                 if len(n.getIncoming()) >= 2 and len(n.getOutgoing()) >= 2)
    L = ["## Restricciones de giro y carriles de giro", ""]
    L += [f"OSM trae **{sum(r.values())} relaciones de restricción de giro** para "
          f"{cruces} intersecciones con al menos dos entradas y dos salidas "
          f"({sum(r.values()) / max(cruces, 1) * 100:.1f} por cada 100). Cualquier giro "
          "prohibido que no esté mapeado queda permitido en la simulación.", ""]
    if r:
        L += _tabla(["tipo", "relaciones"], [[k, v] for k, v in r.most_common()])
    ignoradas = len(re.findall(r"Ignoring restriction relation", d.salida_netconvert))
    if ignoradas:
        L += [f"netconvert ignoró {ignoradas} por referir vías que no están en la descarga "
              "o que no son para autos.", ""]
    L += ["Flechas de giro por carril (`turn:lanes`) en OSM, por tipo de vía:", ""]
    L += _tabla(["tipo", "vías con turn:lanes", "vías del tipo"],
                [[t, tl[t], vt[t]] for t in sorted(vt, key=lambda t: -vt[t]) if vt[t] >= 5])
    return L


def _seccion_conectividad(d: DatosReporte) -> list[str]:
    c = d.conectividad
    deb, fue = c.debiles, c.fuertes
    L = ["## Componentes desconectados", "",
         "Calculado sobre la red **antes de podar**, con las conexiones que puede usar",
         "un auto.", ""]
    L += _tabla(["", "valor"], [
        ["Componentes débilmente conexos", len(deb)],
        ["Aristas en el mayor (débil)", f"{len(deb[0])} ({_pct(len(deb[0]), sum(map(len, deb)))})"],
        ["Componentes fuertemente conexos", len(fue)],
        ["Aristas en el mayor (fuerte)", f"{len(fue[0])} ({_pct(len(fue[0]), sum(map(len, fue)))})"],
        ["Componentes fuertes de más de 1 arista, aparte del mayor",
         sum(1 for x in fue[1:] if len(x) > 1)],
        ["Aristas conservadas", len(c.utiles)],
        ["Aristas podadas: islas (otro componente débil)", len(c.fuera_del_principal)],
        ["Aristas podadas: trampas dentro del componente principal",
         len(c.podar - c.fuera_del_principal)],
    ])
    L += ["Una arista se conserva si un vehículo puede recorrerla de principio a fin: porque",
          "llega al componente fuerte principal, porque se llega a ella desde él, o porque",
          "está entre una entrada y una salida de la red (vías de paso por el borde).",
          "Se poda lo demás: islas sin conexión vial con el resto y trampas (tramos de",
          "sentido único a los que no se puede llegar o que no llevan a ninguna parte).",
          "Casi siempre son errores de sentido o de conexión en OSM.", ""]
    sn = d.net_sin_podar
    for titulo, ids in [("Islas", c.fuera_del_principal),
                        ("Trampas", c.podar - c.fuera_del_principal)]:
        podadas = [sn.getEdge(e) for e in ids if sn.hasEdge(e)]
        if not podadas:
            continue
        L += [f"{titulo}: {len(podadas)} aristas, {km(podadas):.2f} km, en estas vías OSM. "
              "Revisar en netedit o corregir en OSM (una isla suele ser una conexión que "
              "falta en el mapa, o una vía de un tipo que no se descarga, como `track`):", ""]
        L += _enlaces_osm(sorted({i for e in podadas for i in vias_osm(e)}, key=int), "way",
                          maximo=60)
    return L


def _seccion_bordes(d: DatosReporte) -> list[str]:
    ent, sal = aristas_de_borde(d.net)
    L = ["## Aristas de entrada y salida (`is_fringe`)", ""]
    L += _tabla(["", "entradas", "salidas"], [
        ["Total", len(ent), len(sal)],
        ["… en vías arteriales (troncal a terciaria)",
         sum(map(es_arterial, ent)), sum(map(es_arterial, sal))],
        ["… en vías locales", sum(not es_arterial(e) for e in ent),
         sum(not es_arterial(e) for e in sal)],
    ])
    L += ["`is_fringe` marca toda arista cuyo nodo extremo no tiene otra continuación.",
          "Eso incluye los cruces reales del límite municipal, pero también las calles",
          "ciegas internas. Las entradas en vías arteriales son casi todas conexiones con",
          "los municipios vecinos; las locales son mayoritariamente calles sin salida.",
          "La demanda sintética de `python main.py prueba-tecnica` se reparte",
          "uniformemente entre todas, así que la mayoría de esos viajes entran y salen",
          "por calles ciegas: otra razón por la que esa demanda no representa nada.", ""]
    return L


def _seccion_advertencias(d: DatosReporte) -> list[str]:
    L = ["## Advertencias de netconvert", "",
         f"Salida completa en `{d.clave}_netconvert.log`.", ""]
    L += _tabla(["mensaje", "veces"], [[m.replace("|", "/"), n]
                                       for m, n in resumen_advertencias(d.salida_netconvert)[:15]])
    L += ["## Carga en sumo", ""]
    if d.advertencias_carga:
        L += ["```"] + d.advertencias_carga[:20] + ["```", ""]
    else:
        L += ["La red carga en `sumo` sin advertencias ni errores.", ""]
    return L


def _seccion_fronteras(d: DatosReporte) -> tuple[list[str], dict[str, float]]:
    """Verifica que la union de municipios quede conectada."""
    if len(d.municipios) < 2:
        return [], {}
    por_archivo = d.resumen_osm.vias_por_archivo
    nucleo = d.conectividad.fuertes[0]
    edges = d.net.getEdges()

    def archivos(edge) -> set[str]:
        return {a for w in vias_osm(edge) for a, vias in por_archivo.items() if w in vias}

    veces = Counter(w for vias in por_archivo.values() for w in vias)
    compartidas = {w for w, n in veces.items() if n > 1}
    de_frontera = [e for e in edges if len(archivos(e)) > 1]
    filas, fraccion = [], {}
    for m, osm in zip(d.municipios, d.osms):
        propias = [e for e in edges if archivos(e) == {osm.name}]
        en_nucleo = [e for e in propias if e.getID() in nucleo]
        fraccion[m.nombre] = km(en_nucleo) / km(propias) if propias else 0.0
        filas.append([m.nombre, len(propias), f"{km(propias):.1f}", f"{km(en_nucleo):.1f}",
                      _pct(km(en_nucleo), km(propias))])
    frontera_en_nucleo = [e for e in de_frontera if e.getID() in nucleo]
    filas.append(["Vías de frontera (en más de una descarga)", len(de_frontera),
                  f"{km(de_frontera):.1f}", f"{km(frontera_en_nucleo):.1f}",
                  _pct(km(frontera_en_nucleo), km(de_frontera))])

    L = ["## Fronteras entre municipios", "",
         f"La red une {len(d.municipios)} municipios convertidos juntos. Las vías que cruzan",
         f"el límite vienen en más de una descarga ({len(compartidas)} vías OSM compartidas)",
         "y netconvert las toma una sola vez. El núcleo es el componente fuertemente",
         "conexo principal: desde cualquier punto del núcleo se llega a cualquier otro.",
         "Si la frontera no conectara, uno de los municipios tendría casi nada en él.", ""]
    L += _tabla(["", "aristas", "km", "km en el núcleo", "% en el núcleo"], filas)
    L += ["Los límites con municipios que no están en la red siguen cortados: sus vías",
          "aparecen como entradas y salidas (ver la sección de bordes).", ""]
    return L, fraccion


def escribir_reporte(destino: Path, d: DatosReporte) -> tuple[Semaforos, dict[str, float]]:
    sem = clasificar_semaforos(d.net, d.resumen_osm.senales)
    fronteras, fraccion = _seccion_fronteras(d)
    lineas = (
        _encabezado(d)
        + _seccion_resumen(d)
        + fronteras
        + _seccion_carriles(d)
        + _seccion_semaforos(d, sem)
        + _seccion_giros(d)
        + _seccion_conectividad(d)
        + _seccion_bordes(d)
        + _seccion_advertencias(d)
        + ["## Supuestos tomados", ""] + d.supuestos.markdown()
    )
    destino.write_text("\n".join(lineas), encoding="utf-8")
    return sem, fraccion


def supuestos_red(adivinar_semaforos: bool) -> RegistroSupuestos:
    s = RegistroSupuestos()
    s.agregar(
        "semaforos_ubicacion",
        ("Se activo tls.guess: parte de los semaforos NO existen en OSM y fueron "
         "puestos por una regla de netconvert. " if adivinar_semaforos else
         "Solo hay semaforos donde OSM los tiene (tls.guess desactivado). Si OSM "
         "omite un semaforo real, esa interseccion funciona con prioridad y su "
         "capacidad queda sobreestimada. Se prefirio omitir antes que inventar: "
         "en Sabaneta tls.guess agregaba 19 semaforos a los 17 de OSM. ")
        + "Ver la seccion Semaforos para el conteo.",
    )
    s.agregar(
        "semaforos_planes",
        "Ningun semaforo tiene plan real. netconvert genera ciclos fijos "
        "genericos. Los planes del SIMM no son de acceso publico. Cualquier "
        "medida de demora o capacidad en intersecciones semaforizadas depende de "
        "este supuesto.",
    )
    s.agregar(
        "semaforos_descartados",
        "Los semaforos de OSM que no estan en un cruce (pasos peatonales y semaforos "
        "a mitad de via) se descartan con tls.discard-simple. Sus detenciones reales "
        "no se modelan, asi que la capacidad de esas vias queda sobreestimada. Las "
        "glorietas semaforizadas funcionan como glorietas con prelacion hasta que se "
        "les construya el plan a mano. Ver la tabla en la seccion Semaforos.",
    )
    s.agregar(
        "carriles_por_defecto",
        "Donde OSM no trae 'lanes', netconvert usa el typemap base: 1 carril por "
        "sentido en secundaria, terciaria y locales; 2 en primaria y troncal. "
        "No se corrigio ninguno a mano. El conteo esta en la seccion de carriles.",
    )
    s.agregar(
        "carril_compartido",
        f"Las calles con lanes=1 y doble sentido en OSM (un carril que comparten "
        f"ambos sentidos) se modelan como dos carriles de {ANCHO_CARRIL_COMPARTIDO} m, "
        "uno por sentido. OSM no trae su ancho real. En la realidad dos carros que se "
        "cruzan en esas calles frenan o se ceden el paso; en la simulacion se cruzan "
        "sin frenar, asi que su capacidad queda sobreestimada. La moto no puede "
        "adelantar a un auto dentro de esos carriles.",
    )
    s.agregar(
        "velocidad_urbana",
        "Donde OSM no trae 'maxspeed' se usa 50 km/h (capa osmNetconvertUrbanDe), "
        "el limite general urbano en Colombia. Corredores con limite mayor "
        "senalizado pero no mapeado quedan subestimados.",
    )
    s.agregar(
        "sin_vias_de_servicio",
        "Las vias highway=service (parqueaderos, accesos, vias internas de "
        "unidades cerradas) se excluyen porque el typemap no las habilita para "
        "autos. Los viajes que empiezan dentro de una unidad cerrada tendran que "
        "inyectarse en la calle publica mas cercana.",
    )
    s.agregar(
        "sin_pendiente",
        "La red no tiene elevacion: OSM casi no trae 'ele' y no se cargo un "
        "modelo digital de terreno. En el valle, con laderas fuertes, esto "
        "subestima el consumo energetico de los vehiculos electricos. Antes de "
        "la fase de impacto en red electrica hay que agregar un DEM "
        "(netconvert heightmap.geotiff).",
    )
    s.agregar(
        "poda_conectividad",
        "Se eliminan las aristas que no estan en ningun camino que pase por el "
        "componente fuertemente conexo principal. Si alguna era una via real mal "
        "conectada en OSM, su demanda se pierde hasta que se corrija el dato.",
    )
    return s
