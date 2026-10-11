import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import pandas as pd

from aburra_mobility.demanda.gravitacional import MatrizODGravitacional
from aburra_mobility.demanda.muestreo import ADVERTENCIA, escribir_relaciones, sortear


def matriz(vehiculos=2400.0):
    zonas = ["a", "b", "c"]
    viajes = pd.DataFrame([[5.0, 3, 2], [3, 4, 3], [2, 3, 5]], index=zonas, columns=zonas)
    perfil = pd.Series({h: 1 / 24 for h in range(24)})
    return MatrizODGravitacional(viajes, vehiculos, perfil, 0.1)


def total(conteos):
    return sum(c[3] for c in conteos)


class TestSortear(unittest.TestCase):
    def test_misma_semilla_mismo_sorteo(self):
        self.assertEqual(sortear(matriz(), 6, 9, 1.0, 7), sortear(matriz(), 6, 9, 1.0, 7))

    def test_otra_semilla_otro_sorteo(self):
        self.assertNotEqual(sortear(matriz(), 6, 9, 1.0, 7), sortear(matriz(), 6, 9, 1.0, 8))

    def test_solo_horas_de_la_ventana(self):
        self.assertEqual({c[0] for c in sortear(matriz(), 6, 9, 1.0, 1)}, {6, 7, 8})

    def test_el_promedio_se_acerca_a_lo_esperado(self):
        m = matriz(240_000)
        medias = np.mean([total(sortear(m, 0, 24, 1.0, s)) for s in range(20)])
        self.assertAlmostEqual(medias / 240_000, 1, delta=0.01)

    def test_la_escala_reduce_los_vehiculos(self):
        m = matriz(240_000)
        self.assertAlmostEqual(total(sortear(m, 0, 24, 0.1, 3)) / 24_000, 1, delta=0.05)

    def test_conteos_enteros_y_positivos(self):
        for _, _, _, n in sortear(matriz(), 0, 24, 1.0, 1):
            self.assertIsInstance(n, int)
            self.assertGreater(n, 0)


class TestRelaciones(unittest.TestCase):
    def test_un_intervalo_por_hora_con_sus_conteos(self):
        conteos = [(6, "a", "b", 3), (6, "b", "a", 1), (7, "a", "a", 2)]
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "rel.xml"
            escribir_relaciones(conteos, ruta)
            raiz = ET.parse(ruta).getroot()
        intervalos = raiz.findall("interval")
        self.assertEqual([(i.get("begin"), i.get("end")) for i in intervalos],
                         [("21600", "25200"), ("25200", "28800")])
        self.assertEqual([r.get("count") for r in intervalos[0]], ["3", "1"])

    def test_la_advertencia_no_rompe_un_comentario_xml(self):
        texto = ADVERTENCIA.format(beta=0.1, zonas=30, escala="2%", semilla=1)
        self.assertNotIn("--", texto)


if __name__ == "__main__":
    unittest.main()
