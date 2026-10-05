"""Registro de supuestos."""

from __future__ import annotations

from pathlib import Path


class RegistroSupuestos:
    def __init__(self):
        self._items: list[tuple[str, str]] = []

    def agregar(self, clave: str, texto: str):
        self._items.append((clave, texto))

    def __len__(self) -> int:
        return len(self._items)

    def markdown(self) -> list[str]:
        """Lineas markdown, una subseccion numerada por supuesto."""
        lineas = []
        for i, (clave, texto) in enumerate(self._items, 1):
            lineas += [f"### {i}. `{clave}`", "", texto, ""]
        return lineas


def escribir_supuestos_insumos(destino: Path, cuotas: dict, registro: RegistroSupuestos):
    """SUPUESTOS.md: que sale del informe, que no, y que se supuso."""
    lineas = [
        "# Supuestos y limitaciones del pipeline",
        "",
        "Generado automaticamente por `python main.py preparar-insumos`.",
        "No editar a mano: se sobrescribe en cada corrida.",
        "",
        "## Lo que si sale del informe",
        "",
        "- Perfil horario de inicio de viaje por grupo modal (dato directo).",
        "- Cuotas modales para definir vType (dato directo, con la salvedad de abajo).",
        f"- Volumen total de control: {cuotas['total_viajes']:,.0f} viajes/dia habil.",
        f"- Viajes privados motorizados: {cuotas['viajes_privados']:,.0f}.",
        "- Marginales de origen y de destino por macrozona (67 zonas).",
        "",
        "## Lo que NO sale del informe y bloquea la simulacion",
        "",
        "1. **Matriz OD.** Solo hay marginales independientes: 134 numeros para una",
        "   matriz de 67x67 = 4.489 celdas. La conjunta no es recuperable desde las",
        "   marginales. `od2trips` no se puede alimentar. Este es el bloqueante #1.",
        "2. **Distancia por viaje.** Solo hay duracion en rangos, confundida con el",
        "   modo. Sin distancia no hay funcion de impedancia ni estimacion de",
        "   kilometraje diario (y por tanto no hay SOC).",
        "3. **Zonificacion fina.** 67 macrozonas para 4,06 M de habitantes es escala",
        "   macro. Microsimular con TAZ de ese tamano fabrica cuellos de botella",
        "   inexistentes.",
        "4. **Cadenas de viaje.** 47,16 % de los viajes son 'regreso al hogar', pero",
        "   un agregado no permite enlazar viajes con personas.",
        "5. **Aforos de validacion.** Ninguno. Sin conteos la simulacion no es",
        "   calibrable ni defendible.",
        "",
        "Los cinco se resuelven con una sola cosa: el microdato de la EOD 2025.",
        "",
        "Los supuestos de la red vial van en `redes/<municipio>_calidad.md`.",
        "",
        "## Supuestos tomados",
        "",
    ]
    lineas += registro.markdown()
    destino.write_text("\n".join(lineas), encoding="utf-8")
