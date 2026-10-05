"""Matriz origen-destino: interfaz enchufable."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class ProcedenciaOD:
    """Trazabilidad de una matriz."""

    fuente: str
    apta_para_publicar: bool
    nota: str


class MatrizOD(ABC):
    """Contrato que toda fuente de matriz OD debe cumplir."""

    @abstractmethod
    def procedencia(self) -> ProcedenciaOD:
        ...

    @abstractmethod
    def zonas(self) -> list[str]:
        """Ids de zona, en el mismo vocabulario que el shapefile de TAZ."""

    @abstractmethod
    def matriz(self, periodo: str | None = None) -> pd.DataFrame:
        """DataFrame con indice = origen, columnas = destino, valores = viajes."""

    def validar(self) -> None:
        """Chequeos que aplican a cualquier implementacion."""
        m = self.matriz()
        if (m.values < 0).any():
            raise ValueError("La matriz tiene celdas negativas.")
        if list(m.index) != list(m.columns):
            raise ValueError(
                "Origenes y destinos deben usar el mismo vocabulario de zonas."
            )

    def a_od2trips(self, ruta_salida: str, periodo: str | None = None) -> None:
        """Escribe la matriz en formato O de SUMO, apto para `od2trips`."""
        raise NotImplementedError(
            "Pendiente: implementar cuando exista una matriz real."
        )


class MatrizODMicrodato(MatrizOD):
    """Implementacion real. Pendiente de que AMVA entregue el microdato."""

    def __init__(self, ruta_microdato: str, ruta_zonificacion: str):
        raise NotImplementedError(
            "Bloqueado: falta el microdato de la EOD 2025. "
            "Ver scenarios/SUPUESTOS.md, seccion 'Lo que NO sale del informe'."
        )

    def procedencia(self) -> ProcedenciaOD:
        return ProcedenciaOD(
            fuente="microdato EOD 2025 (AMVA)",
            apta_para_publicar=True,
            nota="Matriz observada, expandida con los factores oficiales.",
        )

    def zonas(self) -> list[str]:
        raise NotImplementedError

    def matriz(self, periodo: str | None = None) -> pd.DataFrame:
        raise NotImplementedError
