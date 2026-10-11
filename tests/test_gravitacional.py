import unittest

import numpy as np
import pandas as pd

from aburra_mobility.demanda.gravitacional import (MatrizODGravitacional, furness,
                                                   gravitacional, resumen)

SEMILLA = np.array([[1, 0.5, 0.2], [0.5, 1, 0.5], [0.2, 0.5, 1]])
SALEN = np.array([100.0, 50, 50])
LLEGAN = np.array([60.0, 80, 60])


class TestFurness(unittest.TestCase):
    def test_respeta_salidas_y_llegadas(self):
        t, _ = furness(SEMILLA, SALEN, LLEGAN)
        np.testing.assert_allclose(t.sum(axis=1), SALEN, rtol=1e-5)
        np.testing.assert_allclose(t.sum(axis=0), LLEGAN, rtol=1e-5)

    def test_primera_ronda_como_en_el_ejemplo(self):
        t = SEMILLA * (SALEN / SEMILLA.sum(axis=1))[:, None]
        np.testing.assert_allclose(t[0], [58.8, 29.4, 11.8], atol=0.05)
        np.testing.assert_allclose(t.sum(axis=0), [77.2, 69.1, 53.7], atol=0.05)

    def test_conserva_la_estructura_de_la_semilla(self):
        t, _ = furness(SEMILLA, SALEN, LLEGAN)
        self.assertLess(t[0, 2], t[0, 1])
        self.assertLess(t[2, 0], t[2, 1])

    def test_semilla_uniforme_da_el_producto_de_marginales(self):
        t, it = furness(np.ones((3, 3)), SALEN, LLEGAN)
        np.testing.assert_allclose(t, np.outer(SALEN, LLEGAN) / SALEN.sum())
        self.assertEqual(it, 1)

    def test_llegadas_con_otro_total_se_reescalan(self):
        t, _ = furness(SEMILLA, SALEN, LLEGAN * 1.1)
        np.testing.assert_allclose(t.sum(axis=0), LLEGAN, rtol=1e-5)

    def test_sin_celdas_negativas(self):
        t, _ = furness(SEMILLA, SALEN, LLEGAN)
        self.assertTrue((t >= 0).all())


class TestGravitacional(unittest.TestCase):
    def setUp(self):
        zonas = ["a", "b", "c"]
        self.tiempos = pd.DataFrame([[2, 10, 30], [10, 2, 10], [30, 10, 2]],
                                    index=zonas, columns=zonas, dtype=float)
        self.marg = pd.DataFrame({"salen": SALEN, "llegan": LLEGAN}, index=zonas)

    def test_beta_mayor_acorta_los_viajes(self):
        corto = resumen(gravitacional(self.tiempos, self.marg, 0.3)[0], self.tiempos)
        largo = resumen(gravitacional(self.tiempos, self.marg, 0.0)[0], self.tiempos)
        self.assertGreater(corto["intrazonal"], largo["intrazonal"])
        self.assertLess(corto["tiempo_libre_min"], largo["tiempo_libre_min"])

    def test_factor_implicito(self):
        r = resumen(gravitacional(self.tiempos, self.marg, 0.1)[0], self.tiempos)
        self.assertAlmostEqual(r["factor_implicito"] * r["tiempo_libre_min"], 39.03)


class TestMatrizODGravitacional(unittest.TestCase):
    def setUp(self):
        zonas = ["a", "b"]
        viajes = pd.DataFrame([[30.0, 10], [20, 40]], index=zonas, columns=zonas)
        perfil = pd.Series({7: 0.25, 8: 0.75})
        self.m = MatrizODGravitacional(viajes, 1000, perfil, 0.1)

    def test_el_dia_suma_los_vehiculos(self):
        self.assertAlmostEqual(self.m.matriz().to_numpy().sum(), 1000)

    def test_la_hora_es_el_dia_por_su_peso(self):
        np.testing.assert_allclose(self.m.matriz(8), self.m.matriz() * 0.75)

    def test_no_es_apta_para_publicar(self):
        self.assertFalse(self.m.procedencia().apta_para_publicar)

    def test_pasa_la_validacion_del_contrato(self):
        self.m.validar()


if __name__ == "__main__":
    unittest.main()
