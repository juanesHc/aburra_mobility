import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import pandas as pd

from aburra_mobility.errores import ErrorPipeline
from aburra_mobility.zonas.limites import anillos, dentro
from aburra_mobility.zonas.macrozonas import (COMUNAS_MEDELLIN, marginales, zona_de_macrozona,
                                              zonas_modelo)
from aburra_mobility.zonas.taz import escribir_taz
from tests.falsos import AristaFalsa


def via(*puntos):
    return {"type": "way", "role": "outer",
            "geometry": [{"lon": x, "lat": y} for x, y in puntos]}


def relacion(*vias):
    return {"id": 1, "tags": {"name": "prueba"}, "members": list(vias)}


class TestAnillos(unittest.TestCase):
    def test_une_tramos_aunque_vengan_al_reves(self):
        r = relacion(via((0, 0), (1, 0)), via((1, 1), (1, 0)), via((1, 1), (0, 1), (0, 0)))
        (a,) = anillos(r)
        self.assertEqual(tuple(a[0]), tuple(a[-1]))
        self.assertEqual(len(a), 5)

    def test_ignora_los_huecos(self):
        hueco = dict(via((0.4, 0.4), (0.6, 0.4), (0.6, 0.6), (0.4, 0.4)), role="inner")
        r = relacion(via((0, 0), (1, 0), (1, 1), (0, 0)), hueco)
        self.assertEqual(len(anillos(r)), 1)

    def test_falla_si_el_limite_no_cierra(self):
        with self.assertRaises(ErrorPipeline):
            anillos(relacion(via((0, 0), (1, 0)), via((5, 5), (6, 6))))


class TestDentro(unittest.TestCase):
    cuadro = np.array([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)], dtype=float)

    def test_puntos_dentro_y_fuera(self):
        puntos = np.array([(1, 1), (3, 1), (1, -1), (0.1, 1.9), (-5, 5)], dtype=float)
        np.testing.assert_array_equal(dentro(puntos, [self.cuadro]),
                                      [True, False, False, True, False])

    def test_varios_anillos(self):
        otro = self.cuadro + 10
        puntos = np.array([(1, 1), (11, 11), (5, 5)], dtype=float)
        np.testing.assert_array_equal(dentro(puntos, [self.cuadro, otro]), [True, True, False])

    def test_muchos_puntos(self):
        puntos = np.random.default_rng(0).uniform(-1, 3, size=(5000, 2))
        esperado = (puntos > 0).all(axis=1) & (puntos < 2).all(axis=1)
        np.testing.assert_array_equal(dentro(puntos, [self.cuadro]), esperado)


class TestMacrozonas(unittest.TestCase):
    def test_treinta_zonas_sin_repetir(self):
        zonas = zonas_modelo()
        self.assertEqual(len(zonas), 30)
        self.assertEqual(len({z.id for z in zonas}), 30)
        self.assertEqual(len({z.relacion_osm for z in zonas}), 30)

    def test_medellin_por_comuna_y_el_resto_por_municipio(self):
        self.assertEqual(zona_de_macrozona("medellin__belen", "Medellín"), "medellin__belen")
        self.assertEqual(zona_de_macrozona("bello__comuna_04", "Bello"), "bello")
        self.assertEqual(zona_de_macrozona("itagui__rural_itagui", "Itagüí"), "itagui")
        self.assertIsNone(zona_de_macrozona("sin_especificar", "Sin especificar"))

    def _marginales(self, filas):
        with tempfile.TemporaryDirectory() as tmp:
            pd.DataFrame(filas, columns=["extremo", "taz_id", "municipio", "macrozona", "viajes",
                                         "pct"]).to_csv(Path(tmp) / "macrozonas_od.csv",
                                                        index=False)
            return marginales(Path(tmp))

    def test_suma_las_macrozonas_y_omite_sin_especificar(self):
        m = self._marginales([
            ["origen", "bello__comuna_01", "Bello", "Comuna 01", 10, 0],
            ["origen", "bello__comuna_02", "Bello", "Comuna 02", 5, 0],
            ["destino", "bello__comuna_01", "Bello", "Comuna 01", 7, 0],
            ["origen", "medellin__popular", "Medellín", "Popular", 3, 0],
            ["destino", "medellin__popular", "Medellín", "Popular", 4, 0],
            ["origen", "sin_especificar", "Sin especificar", "Sin especificar", 99, 0],
        ])
        self.assertEqual(m.loc["bello", "salen"], 15)
        self.assertEqual(m.loc["bello", "llegan"], 7)
        self.assertNotIn("sin_especificar", m.index)

    def test_falla_con_una_comuna_de_medellin_desconocida(self):
        with self.assertRaises(ErrorPipeline):
            self._marginales([["origen", "medellin__nueva", "Medellín", "Nueva", 1, 0]])

    def test_cubre_las_21_macrozonas_de_medellin(self):
        self.assertEqual(len(COMUNAS_MEDELLIN), 21)


class TestTaz(unittest.TestCase):
    def test_cada_calle_es_origen_y_destino_con_su_largo(self):
        por_zona = {"a": [AristaFalsa("e1", 120.0, [(0, 0), (1, 0)])],
                    "b": [AristaFalsa("e2", 35.5, [(0, 0), (1, 0)])]}
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "zonas.taz.xml"
            escribir_taz(por_zona, ruta)
            tazs = ET.parse(ruta).getroot().findall("taz")
        self.assertEqual([t.get("id") for t in tazs], ["a", "b"])
        fuente, sumidero = tazs[0]
        self.assertEqual((fuente.tag, fuente.get("id"), fuente.get("weight")),
                         ("tazSource", "e1", "120.0"))
        self.assertEqual(sumidero.tag, "tazSink")


if __name__ == "__main__":
    unittest.main()
