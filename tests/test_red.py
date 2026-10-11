import unittest

from aburra_mobility.demanda.impedancia import _dijkstra, arista_representativa
from aburra_mobility.errores import ErrorPipeline
from aburra_mobility.red.conectividad import componentes_debiles, componentes_fuertes
from aburra_mobility.red.municipios import (MUNICIPIOS, buscar_municipios, clave_municipio,
                                            clave_red, es_valle_completo)
from tests.falsos import AristaFalsa


class TestMunicipios(unittest.TestCase):
    def test_clave_sin_tildes_ni_espacios(self):
        self.assertEqual(clave_municipio("Itagüí"), "itagui")
        self.assertEqual(clave_municipio(" La Estrella "), "la_estrella")

    def test_valle_son_los_diez(self):
        municipios = buscar_municipios(["valle"])
        self.assertEqual(len(municipios), 10)
        self.assertTrue(es_valle_completo(municipios))

    def test_sin_repetir_y_en_orden(self):
        municipios = buscar_municipios(["Sabaneta", "envigado", "sabaneta"])
        self.assertEqual(clave_red(municipios), "envigado_sabaneta")
        self.assertFalse(es_valle_completo(municipios))

    def test_municipio_desconocido(self):
        with self.assertRaises(ErrorPipeline):
            buscar_municipios(["Rionegro"])

    def test_relaciones_osm_distintas(self):
        self.assertEqual(len({m.relacion_osm for m in MUNICIPIOS.values()}), 10)


class TestConectividad(unittest.TestCase):
    sig = {"a": {"b"}, "b": {"c"}, "c": {"a", "d"}, "d": set(), "x": {"y"}, "y": set()}

    def test_componentes_fuertes(self):
        fuertes = componentes_fuertes(self.sig)
        self.assertEqual(fuertes[0], {"a", "b", "c"})
        self.assertEqual(len(fuertes), 4)

    def test_componentes_debiles(self):
        self.assertEqual(componentes_debiles(self.sig), [{"a", "b", "c", "d"}, {"x", "y"}])

    def test_cadena_larga_sin_desbordar_la_recursion(self):
        n = 20_000
        sig = {str(i): {str((i + 1) % n)} for i in range(n)}
        self.assertEqual(len(componentes_fuertes(sig)[0]), n)


class TestImpedancia(unittest.TestCase):
    def test_dijkstra_elige_el_camino_mas_rapido(self):
        siguientes = {"o": {"lento", "r1"}, "lento": {"d"}, "r1": {"r2"}, "r2": {"d"}, "d": set()}
        tiempo = {"o": 0, "lento": 100, "r1": 10, "r2": 10, "d": 5}
        dist = _dijkstra("o", siguientes, tiempo)
        self.assertEqual(dist["d"], 25)
        self.assertNotIn("x", dist)

    def test_representativa_es_la_mas_cercana_al_centro(self):
        aristas = [AristaFalsa("izq", 100, [(0, 0), (0, 0)]),
                   AristaFalsa("centro", 10, [(5, 0), (5, 0)]),
                   AristaFalsa("der", 100, [(10, 0), (10, 0)])]
        self.assertEqual(arista_representativa(aristas).getID(), "centro")

    def test_representativa_pondera_por_largo(self):
        aristas = [AristaFalsa("larga", 1000, [(0, 0), (0, 0)]),
                   AristaFalsa("corta", 1, [(10, 0), (10, 0)])]
        self.assertEqual(arista_representativa(aristas).getID(), "larga")


if __name__ == "__main__":
    unittest.main()
