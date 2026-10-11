"""Reporte de la demanda estimada: zonas, tiempos, sensibilidad a beta y supuestos."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from ..supuestos import RegistroSupuestos
from .gravitacional import TIEMPO_PRIVADO_INFORME, MatrizODGravitacional


@dataclass
class DatosDemanda:
    red: Path
    nombres: dict[str, str]
    km_por_zona: dict[str, float]
    sin_calles: list[str]
    marg: pd.DataFrame
    tiempos: pd.DataFrame
    matriz: MatrizODGravitacional
    iteraciones: int
    sensibilidad: pd.DataFrame
    desde: int
    hasta: int
    escala: float
    semilla: int
    sorteados: int


def _tabla(encabezado: list[str], filas: list[list]) -> list[str]:
    return (["| " + " | ".join(encabezado) + " |", "|" + "---|" * len(encabezado)]
            + ["| " + " | ".join(str(c) for c in f) + " |" for f in filas] + [""])


def supuestos_demanda(beta: float, escala: float) -> RegistroSupuestos:
    s = RegistroSupuestos()
    s.agregar("matriz_estimada",
              "La matriz no es observada. El informe da cuantos viajes salen y llegan a cada "
              "macrozona, no quien va a donde; el reparto entre pares sale de un modelo "
              "gravitacional doblemente restringido balanceado con Furness. Sirve para que "
              "la demanda tenga estructura espacial razonable, no para afirmar flujos entre zonas.")
    s.agregar("zonificacion_provisional",
              "Se usan 30 zonas: las 16 comunas y 5 corregimientos de Medellin, que estan en OSM, "
              "y un bloque por cada uno de los otros nueve municipios, porque OSM no tiene las "
              "comunas de Bello e Itagui, las zonas de Envigado ni el limite urbano-rural. "
              "Las 46 macrozonas de esos municipios se suman en su bloque. Con los poligonos "
              "oficiales de AMVA se puede volver a las 67.")
    s.agregar("sin_especificar",
              "Los viajes de la macrozona 'Sin especificar' se reparten en proporcion a las "
              "demas zonas.")
    s.agregar("beta_sin_calibrar",
              f"beta = {beta} por minuto no esta calibrado. El unico tiempo del informe para el "
              f"transporte privado ({TIEMPO_PRIVADO_INFORME} min) es puerta a puerta y con "
              "congestion; los tiempos del modelo son de flujo libre sobre la red. Compararlos "
              "exige suponer un factor entre ambos, y beta depende de ese factor (ver la tabla "
              "de sensibilidad). El histograma de duraciones del informe incluye los viajes a pie "
              "y no sirve para el privado.")
    s.agregar("tiempos_flujo_libre",
              "El tiempo entre zonas es el del camino mas rapido entre sus aristas "
              "representativas, a la velocidad maxima de cada calle. Dentro de una zona es el "
              "promedio desde su arista representativa hacia sus calles, ponderado por largo.")
    s.agregar("patron_igual_todo_el_dia",
              "El informe da los totales por zona del dia, no por hora. Todas las horas usan la "
              "misma matriz escalada por el perfil horario del privado: no se distingue la ida "
              "de la manana de la vuelta de la tarde.")
    s.agregar("reparto_modal_uniforme",
              "Las marginales son de todos los modos. Se supone que auto y moto (su cuota en "
              "'Modo Principal') pesan lo mismo en todas las zonas, lo que subestima el privado "
              "en zonas como El Poblado y lo sobreestima en otras.")
    s.agregar("un_vehiculo_por_viaje",
              "Cada viaje privado es un vehiculo: el informe no trae ocupacion vehicular.")
    s.agregar("calles_de_origen",
              "Los viajes empiezan y terminan en calles del nucleo conectado, con probabilidad "
              "proporcional a su largo. Se excluyen autopistas, troncales y tramos de menos de "
              "10 m. No hay datos de donde viven o trabajan las personas dentro de cada zona.")
    s.agregar("escala_sin_capacidad",
              f"Se simula el {escala:.0%} de los vehiculos sin reducir la capacidad de las vias, asi "
              "que la congestion queda subestimada. Sirve para probar la cadena y ver el patron "
              "espacial, no para medir congestion.")
    return s


def escribir_reporte(destino: Path, d: DatosDemanda, supuestos: RegistroSupuestos):
    m = d.matriz
    diaria = m.matriz()
    total = diaria.to_numpy().sum()
    L = ["# Demanda estimada (modelo gravitacional + Furness)", "",
         "Generado por `python main.py demanda`. No editar a mano.", "",
         f"> {m.procedencia().nota} Ver la seccion de supuestos.", "",
         f"Red: `{d.red.name}`", ""]

    L += ["## Zonas", ""]
    filas = []
    for z in diaria.sum(axis=1).sort_values(ascending=False).index:
        filas.append([d.nombres[z], f"{d.km_por_zona[z]:.0f}", f"{d.marg.loc[z, 'salen']:,.0f}",
                      f"{d.marg.loc[z, 'llegan']:,.0f}", f"{diaria.loc[z].sum():,.0f}",
                      f"{d.tiempos.loc[z, z]:.1f}"])
    L += _tabla(["zona", "km de calles", "viajes que salen (informe)", "llegan (informe)",
                 "vehiculos privados/dia que salen", "min dentro de la zona"], filas)
    if d.sin_calles:
        L += [f"Zonas sin calles en esta red (sus viajes se omiten): {', '.join(d.sin_calles)}.", ""]

    L += ["## Matriz", "",
          f"- Vehiculos privados por dia: {total:,.0f} (auto y moto).",
          f"- Furness convergio en {d.iteraciones} iteraciones.",
          f"- Viajes dentro de la misma zona: {np.trace(diaria.to_numpy()) / total:.1%}.", ""]
    pares = diaria.stack().sort_values(ascending=False).head(10)
    L += _tabla(["origen", "destino", "vehiculos/dia", "minutos a flujo libre"],
                [[d.nombres[o], d.nombres[t], f"{v:,.0f}", f"{d.tiempos.loc[o, t]:.1f}"]
                 for (o, t), v in pares.items()])

    L += ["## Sensibilidad a beta", "",
          f"El factor implicito es cuanto habria que multiplicar el tiempo medio a flujo libre "
          f"para llegar a los {TIEMPO_PRIVADO_INFORME} min del informe. Un factor entre 2 y 3 "
          "corresponde a una velocidad puerta a puerta de un tercio a la mitad de la de flujo "
          "libre. Beta mas alto concentra los viajes cerca de su origen.", ""]
    L += _tabla(["beta (1/min)", "minutos a flujo libre", "factor implicito", "viajes internos",
                 "iteraciones"],
                [[f"{r.beta:.2f}" + (" (usado)" if abs(r.beta - m.beta) < 1e-9 else ""),
                  f"{r.tiempo_libre_min:.1f}", f"{r.factor_implicito:.2f}", f"{r.intrazonal:.1%}",
                  int(r.iteraciones)] for r in d.sensibilidad.itertuples()])

    esperados = sum(m.matriz(h).to_numpy().sum() for h in range(d.desde, d.hasta)) * d.escala
    L += ["## Esta corrida", "",
          f"- Ventana: {d.desde}:00 a {d.hasta}:00. Escala: {d.escala:.0%}. Semilla: {d.semilla}.",
          f"- Vehiculos sorteados: {d.sorteados:,} (esperados {esperados:,.0f}).",
          "- Otra semilla da otro sorteo con el mismo patron promedio; la misma semilla repite "
          "la corrida.", ""]

    L += ["## Supuestos", ""] + supuestos.markdown()
    destino.write_text("\n".join(L), encoding="utf-8")

