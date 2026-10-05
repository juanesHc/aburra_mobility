"""Extraccion del informe agregado de la EOD 2025 (AMVA)."""

import unicodedata
from pathlib import Path

import pandas as pd

from ..errores import ErrorPipeline

HOJAS_SIMPLES = {
    "Duración de Viajes": "duracion_viajes",
    "Frecuencia de Viajes": "frecuencia_viajes",
    "Viajes por Estrato": "viajes_por_estrato",
    "Tiempo por Modo": "tiempo_por_modo",
    "Modo Principal": "modo_principal",
    "Motivo de Viaje": "motivo_viaje",
    "Etapas del Viaje": "etapas_viaje",
    "Grupos Poblacionales": "grupos_poblacionales",
    "Tipología Vehicular": "tipologia_vehicular",
    "Cantidad Vehículos": "cantidad_vehiculos",
    "Modelo Vehicular": "modelo_vehicular",
    "Vehículos por Estrato": "vehiculos_por_estrato",
    "Socio Edad": "socio_edad",
    "Socio Género": "socio_genero",
    "Socio Ocupación": "socio_ocupacion",
    "Socio Escolaridad": "socio_escolaridad",
}

HOJAS_KPI = {
    "KPIs Generales": "kpis_generales",
    "KPIs Motorización": "kpis_motorizacion",
}


def slug(texto: str) -> str:
    """Normaliza un texto a snake_case ASCII, apto para nombres de columna."""
    t = unicodedata.normalize("NFKD", str(texto))
    t = t.encode("ascii", "ignore").decode("ascii").lower().strip()
    for ch in " -/()%.,":
        t = t.replace(ch, "_")
    while "__" in t:
        t = t.replace("__", "_")
    return t.strip("_")


def leer_simple(xlsx: Path, hoja: str) -> pd.DataFrame:
    df = pd.read_excel(xlsx, sheet_name=hoja, header=3).iloc[:, 1:3]
    df.columns = ["categoria", "valor"]
    df = df.dropna()
    df["categoria"] = df["categoria"].astype(str).str.strip()
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    return df.dropna().reset_index(drop=True)


def leer_kpis(xlsx: Path, hoja: str) -> pd.DataFrame:
    """Los KPIs vienen como texto formateado ('6.490.299', '31,59 %', '39,28 min')."""
    df = pd.read_excel(xlsx, sheet_name=hoja, header=3).iloc[:, 1:3]
    df.columns = ["indicador", "valor_texto"]
    df = df.dropna().reset_index(drop=True)
    df["indicador"] = df["indicador"].astype(str).str.strip()

    def parsear(v):
        s = str(v).strip().replace("%", "").replace("min", "").strip()
        if "," in s:
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(".", "")
        try:
            return float(s)
        except ValueError:
            return None

    df["valor_num"] = df["valor_texto"].map(parsear)
    df["clave"] = df["indicador"].map(slug)
    return df[["clave", "indicador", "valor_texto", "valor_num"]]


def leer_horaria(xlsx: Path) -> pd.DataFrame:
    df = pd.read_excel(xlsx, sheet_name="Distribución Horaria", header=3).iloc[:, 1:6]
    df.columns = ["hora", "informal", "publico", "privado", "no_motorizado"]
    df = df.dropna().reset_index(drop=True)
    df["hora"] = df["hora"].astype(int)
    for c in ["informal", "publico", "privado", "no_motorizado"]:
        df[c] = df[c].astype(int)
    df["total"] = df[["informal", "publico", "privado", "no_motorizado"]].sum(axis=1)
    return df


def leer_macrozonas(xlsx: Path) -> pd.DataFrame:
    """Las dos tablas (origen y destino) viven en la misma hoja, apiladas."""
    raw = pd.read_excel(xlsx, sheet_name="Macrozonas OD", header=None)
    encabezados = [i for i, v in raw[1].items() if str(v).startswith("Municipio")]
    if len(encabezados) != 2:
        raise ValueError(
            f"Se esperaban 2 tablas en 'Macrozonas OD', se encontraron {len(encabezados)}"
        )

    partes = []
    for etiqueta, ini, fin in [
        ("origen", encabezados[0], encabezados[1] - 3),
        ("destino", encabezados[1], len(raw)),
    ]:
        t = raw.iloc[ini + 1 : fin, 1:5].dropna().copy()
        t.columns = ["municipio", "macrozona", "viajes", "pct"]
        t["extremo"] = etiqueta
        partes.append(t)

    df = pd.concat(partes, ignore_index=True)
    df["viajes"] = df["viajes"].astype(float).astype(int)
    df["pct"] = df["pct"].astype(float)
    df["taz_id"] = df["municipio"].map(slug) + "__" + df["macrozona"].map(slug)
    return df[["extremo", "taz_id", "municipio", "macrozona", "viajes", "pct"]]


def extraer(xlsx: Path, salida: Path) -> list[tuple[str, int]]:
    """Escribe los 20 CSV y devuelve (nombre, filas) de cada uno."""
    if not xlsx.exists():
        raise ErrorPipeline(f"no se encontro el informe {xlsx}\n"
                            "Copia el .xlsx del AMVA a data/raw/")

    salida.mkdir(parents=True, exist_ok=True)
    escritos = []

    def guardar(df: pd.DataFrame, nombre: str):
        df.to_csv(salida / f"{nombre}.csv", index=False, encoding="utf-8")
        escritos.append((nombre, len(df)))

    for hoja, nombre in HOJAS_KPI.items():
        guardar(leer_kpis(xlsx, hoja), nombre)
    for hoja, nombre in HOJAS_SIMPLES.items():
        guardar(leer_simple(xlsx, hoja), nombre)
    guardar(leer_horaria(xlsx), "distribucion_horaria")
    guardar(leer_macrozonas(xlsx), "macrozonas_od")

    print(f"{len(escritos)} tablas escritas en {salida}/")
    for nombre, n in escritos:
        print(f"  {nombre:28s} {n:4d} filas")

    chequear_consistencia(salida)
    return escritos


def chequear_consistencia(salida: Path):
    """Cruza totales entre hojas."""
    kpi = pd.read_csv(salida / "kpis_generales.csv").set_index("clave")["valor_num"]
    dh = pd.read_csv(salida / "distribucion_horaria.csv")
    mz = pd.read_csv(salida / "macrozonas_od.csv")
    total_kpi = kpi.get("total_de_viajes_en_un_dia_habil")
    total_horaria = dh["total"].sum()

    print("\nChequeos de consistencia")
    if total_kpi is None:
        print("  ADVERTENCIA: no se encontro el KPI de total de viajes.")
        return

    dif = abs(total_kpi - total_horaria)
    print(f"  total KPI      = {total_kpi:>12,.0f}")
    print(f"  total horaria  = {total_horaria:>12,.0f}   dif = {dif:.0f}")
    if dif > 100:
        print("  ADVERTENCIA: discrepancia mayor a la tolerancia de redondeo.")

    for extremo in ["origen", "destino"]:
        s = mz.loc[mz["extremo"] == extremo, "viajes"].sum()
        print(f"  macrozonas {extremo:8s} = {s:>12,.0f}   dif = {abs(s - total_kpi):.0f}")
