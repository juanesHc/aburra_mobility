"""Matriz OD estimada: modelo gravitacional doblemente restringido, balanceado con Furness."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .matriz_od import MatrizOD, ProcedenciaOD

BETA = 0.10
TIEMPO_PRIVADO_INFORME = 39.03
TOLERANCIA = 1e-6
MAX_ITERACIONES = 1000


def furness(semilla: np.ndarray, salen: np.ndarray, llegan: np.ndarray) -> tuple[np.ndarray, int]:
    """Escala filas y columnas por turnos hasta que la matriz respeta ambos totales."""
    t = semilla.astype(float).copy()
    llegan = llegan * salen.sum() / llegan.sum()
    for i in range(1, MAX_ITERACIONES + 1):
        t *= (salen / t.sum(axis=1))[:, None]
        t *= (llegan / t.sum(axis=0))[None, :]
        if np.abs(t.sum(axis=1) - salen).max() <= TOLERANCIA * salen.max():
            return t, i
    raise ValueError(f"Furness no convergio en {MAX_ITERACIONES} iteraciones")


def gravitacional(tiempos: pd.DataFrame, marg: pd.DataFrame, beta: float) -> tuple[pd.DataFrame, int]:
    """Viajes diarios por par de zonas con semilla exp(-beta * minutos)."""
    zonas = list(tiempos.index)
    m = marg.loc[zonas]
    t, it = furness(np.exp(-beta * tiempos.to_numpy()), m["salen"].to_numpy(float),
                    m["llegan"].to_numpy(float))
    return pd.DataFrame(t, index=zonas, columns=zonas), it


def resumen(viajes: pd.DataFrame, tiempos: pd.DataFrame) -> dict:
    """Tiempo medio a flujo libre, factor que lo lleva al tiempo del informe y viajes internos."""
    medio = float((viajes * tiempos).to_numpy().sum() / viajes.to_numpy().sum())
    return {"tiempo_libre_min": medio,
            "factor_implicito": TIEMPO_PRIVADO_INFORME / medio,
            "intrazonal": float(np.trace(viajes.to_numpy()) / viajes.to_numpy().sum())}


def sensibilidad(tiempos: pd.DataFrame, marg: pd.DataFrame,
                 betas=(0.0, 0.05, 0.10, 0.15, 0.20, 0.30)) -> pd.DataFrame:
    filas = []
    for b in betas:
        viajes, it = gravitacional(tiempos, marg, b)
        filas.append({"beta": b, "iteraciones": it, **resumen(viajes, tiempos)})
    return pd.DataFrame(filas)


def vehiculos_privados_dia(procesados: Path) -> float:
    """Viajes diarios en auto y moto: total de la hoja horaria por la cuota de 'Modo Principal'."""
    modo = pd.read_csv(procesados / "modo_principal.csv").set_index("categoria")["valor"]
    total = pd.read_csv(procesados / "distribucion_horaria.csv")["total"].sum()
    return total * (modo["Automóvil"] + modo["Motocicleta"]) / 100


class MatrizODGravitacional(MatrizOD):
    """Vehiculos privados esperados por par de zonas, en el dia o en una hora."""

    def __init__(self, viajes: pd.DataFrame, vehiculos_dia: float, perfil: pd.Series, beta: float):
        self._diaria = viajes / viajes.to_numpy().sum() * vehiculos_dia
        self._perfil = perfil
        self.beta = beta

    def procedencia(self) -> ProcedenciaOD:
        return ProcedenciaOD(
            fuente="modelo gravitacional + Furness sobre las marginales del informe EOD 2025",
            apta_para_publicar=False,
            nota=f"Matriz ESTIMADA, no observada (beta = {self.beta} por minuto, sin calibrar).",
        )

    def zonas(self) -> list[str]:
        return list(self._diaria.index)

    def matriz(self, periodo: int | None = None) -> pd.DataFrame:
        """Sin periodo, el dia completo; con periodo, la hora que empieza en esa hora del dia."""
        return self._diaria if periodo is None else self._diaria * self._perfil[periodo]
