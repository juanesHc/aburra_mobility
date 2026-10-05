"""Tipos de vehiculo (vTypes) de SUMO derivados del informe."""

from pathlib import Path

import pandas as pd

from ..supuestos import RegistroSupuestos


def cuotas_vehiculares(procesados: Path, supuestos: RegistroSupuestos) -> dict:
    """Deriva las cuotas de vType desde la hoja de Modo Principal."""
    modo = pd.read_csv(procesados / "modo_principal.csv").set_index("categoria")["valor"]
    horaria = pd.read_csv(procesados / "distribucion_horaria.csv")

    total = horaria["total"].sum()

    auto = modo["Automóvil"]
    moto = modo["Motocicleta"]
    taxi = modo["Taxi"]
    privado_modo = auto + moto
    privado_horaria = horaria["privado"].sum() / total * 100

    print("Reconciliacion de taxonomias modales")
    print(f"  privado segun 'Modo Principal' (auto+moto) : {privado_modo:.2f} %")
    print(f"  privado segun hoja horaria (4 grupos)      : {privado_horaria:.2f} %")
    print(f"  discrepancia                               : "
          f"{abs(privado_modo - privado_horaria):.2f} pp")
    print(f"  categoria 'Otros' sin desagregar           : {modo['Otros']:.2f} %")

    supuestos.agregar(
        "taxonomia_modal",
        f"El informe da dos reparticiones modales incompatibles: 'Modo Principal' "
        f"(8 categorias) implica {privado_modo:.2f} % de viajes en modo privado "
        f"motorizado, mientras la hoja horaria (4 grupos) implica "
        f"{privado_horaria:.2f} %. La diferencia de "
        f"{abs(privado_modo - privado_horaria):.2f} pp queda sin explicar porque la "
        f"categoria 'Otros' ({modo['Otros']:.2f} %) no esta desagregada. Se adopta "
        f"'Modo Principal' para las cuotas de vType y la hoja horaria para el perfil "
        f"temporal. Resolver esto requiere el microdato.",
    )

    return {
        "pct_auto": auto,
        "pct_moto": moto,
        "pct_taxi": taxi,
        "pct_privado_total": privado_modo,
        "share_auto": auto / privado_modo,
        "share_moto": moto / privado_modo,
        "total_viajes": total,
        "viajes_privados": total * privado_modo / 100,
    }


def escribir_vtypes(cuotas: dict, destino: Path, supuestos: RegistroSupuestos):
    """vTypeDistribution para el trafico privado motorizado."""
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!--
  Tipos de vehiculo derivados del informe EOD 2025 AMVA.

  Cuotas (fuente: hoja 'Modo Principal' del informe):
    Automovil    {cuotas['pct_auto']:.2f} % de los viajes totales
    Motocicleta  {cuotas['pct_moto']:.2f} % de los viajes totales
    -> dentro del privado motorizado: {cuotas['share_auto']*100:.1f} % auto /
       {cuotas['share_moto']*100:.1f} % moto

  ADVERTENCIA: los parametros laterales de la motocicleta NO ESTAN CALIBRADOS.
  Son valores de arranque. El filtrado entre filas define la capacidad real de
  las vias del Valle de Aburra y requiere el modelo sublane
  (lateral-resolution) calibrado contra aforos locales.
-->
<additional xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/additional_file.xsd">

    <vTypeDistribution id="privado">
        <vType id="auto" vClass="passenger" probability="{cuotas['share_auto']:.4f}"
               length="4.3" minGap="2.5" maxSpeed="45.0" accel="2.6" decel="4.5"
               sigma="0.5" carFollowModel="Krauss" color="0.8,0.2,0.2"/>
        <vType id="moto" vClass="motorcycle" probability="{cuotas['share_moto']:.4f}"
               length="2.2" minGap="1.0" maxSpeed="38.0" accel="3.5" decel="6.0"
               sigma="0.6" carFollowModel="Krauss" color="0.9,0.7,0.1"
               latAlignment="arbitrary" minGapLat="0.4" maxSpeedLat="1.2"/>
    </vTypeDistribution>

    <vType id="taxi" vClass="taxi" length="4.3" minGap="2.5" maxSpeed="45.0"
           color="0.9,0.9,0.1"/>

    <!--
      Version electrica del automovil, para la fase de impacto en red.
      Los valores son plantillas del modelo battery de SUMO y deben
      reemplazarse por especificaciones reales de la flota objetivo.
    -->
    <vType id="auto_bev" vClass="passenger" length="4.3" minGap="2.5" maxSpeed="45.0"
           emissionClass="Energy" color="0.1,0.7,0.3">
        <param key="has.battery.device" value="true"/>
        <param key="maximumBatteryCapacity" value="50000"/>
        <param key="maximumPower" value="100000"/>
        <param key="vehicleMass" value="1600"/>
        <param key="frontSurfaceArea" value="2.6"/>
        <param key="airDragCoefficient" value="0.35"/>
        <param key="rollDragCoefficient" value="0.01"/>
        <param key="propulsionEfficiency" value="0.9"/>
        <param key="recuperationEfficiency" value="0.7"/>
    </vType>

</additional>
"""
    destino.write_text(xml, encoding="utf-8")

    supuestos.agregar(
        "moto_sin_calibrar",
        "La motocicleta es el 59,94 % del parque y el 14,57 % de los viajes. Los "
        "parametros laterales del vType 'moto' son valores de arranque, no "
        "calibrados. Sin calibrar el modelo sublane contra aforos locales, la "
        "simulacion sobreestimara la congestion de forma severa.",
    )
    supuestos.agregar(
        "bev_plantilla",
        "El vType 'auto_bev' usa parametros de plantilla del modelo battery de SUMO. "
        "El informe solo dice que 5,04 % del parque opera con 'tecnologias limpias', "
        "sin aclarar si eso incluye GNV e hibridos o solo electricos puros. Esa "
        "definicion hay que confirmarla con AMVA antes de usar el dato.",
    )
