"""Perfil horario de salidas por grupo modal."""

from pathlib import Path

import pandas as pd

from ..supuestos import RegistroSupuestos

GRUPOS = ["informal", "publico", "privado", "no_motorizado"]


def calcular_perfil(procesados: Path, destino: Path,
                    supuestos: RegistroSupuestos) -> pd.DataFrame:
    """Pesos horarios de salida, normalizados por grupo modal. Dato directo."""
    h = pd.read_csv(procesados / "distribucion_horaria.csv")
    perfil = h[["hora"]].copy()
    for c in GRUPOS:
        perfil[f"w_{c}"] = h[c] / h[c].sum()
    perfil.to_csv(destino, index=False, encoding="utf-8")

    supuestos.agregar(
        "perfil_privado_compartido",
        "La hoja horaria agrega automovil y motocicleta en un solo grupo 'privado'. "
        "Al no existir curvas separadas, ambos vType heredan el mismo perfil de "
        "salida. Es un supuesto fuerte: los patrones de salida de auto y moto "
        "difieren, y esto sesga cualquier estimacion de composicion vehicular por "
        "hora. Corregible solo con el microdato.",
    )
    supuestos.agregar(
        "hora_inicio_no_es_hora_de_carga",
        "El perfil horario describe la hora de INICIO DEL VIAJE, no la hora de "
        "conexion a un cargador. No debe usarse directamente como perfil de carga "
        "electrica. Para eso hace falta modelar el fin del ultimo viaje del dia por "
        "vehiculo, lo que exige cadenas de viaje encadenadas por persona.",
    )
    return perfil
