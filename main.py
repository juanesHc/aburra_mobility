import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from aburra_mobility import entorno, etapas, rutas
from aburra_mobility.errores import ErrorPipeline
from aburra_mobility.red.municipios import POR_DEFECTO, VALLE, buscar_municipios, clave_red, es_valle_completo


def _cmd_verificar(a):
    etapas.titulo("VERIFICACION DEL ENTORNO")
    if not entorno.verificar():
        return 1
    print("Todo listo.")
    return 0


def _cmd_extraer(a):
    etapas.extraer_encuesta()
    return "preparar-insumos"


def _cmd_insumos(a):
    etapas.preparar_insumos()
    return "construir-red"


def _cmd_red(a):
    etapas.construir_red(a.municipios, a.osm, a.descargar, a.adivinar_semaforos)
    municipios = buscar_municipios(a.municipios)
    if es_valle_completo(municipios):
        return "prueba-tecnica --valle"
    return "prueba-tecnica --municipio " + " ".join(m.clave for m in municipios)


def _red_elegida(a):
    if a.reticula:
        return None
    if a.red:
        return a.red.resolve()
    if a.valle:
        return rutas.red_municipio(clave_red(buscar_municipios([VALLE])))
    return rutas.red_municipio(clave_red(buscar_municipios(a.municipio)))


def _cmd_prueba(a):
    etapas.prueba_tecnica(_red_elegida(a))
    return "simular"


def _cmd_simular(a):
    etapas.simular(gui=a.gui)
    return None if a.gui else "simular --gui   (para verla)"


def _cmd_todo(a):
    etapas.extraer_encuesta()
    etapas.preparar_insumos()
    red = etapas.construir_red(a.municipios)
    etapas.prueba_tecnica(red)
    etapas.simular(gui=a.gui)
    etapas.titulo("PIPELINE COMPLETO")
    print(f"  CSV:        {rutas.PROCESADOS}")
    print(f"  Insumos:    {rutas.ESCENARIOS}")
    print(f"  Red:        {red}")
    print(f"  Escenario:  {rutas.PRUEBA_TECNICA}")
    print("\nAntes de usar cualquier resultado, lee scenarios/SUPUESTOS.md y el")
    print(f"reporte de calidad de la red ({red.name.removesuffix('.net.xml')}_calidad.md).")
    return None


def _cmd_limpiar(a):
    etapas.limpiar()
    return None


def construir_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python main.py",
        description="Pipeline de movilidad del Valle de Aburra (EOD 2025 + OSM + SUMO).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Sin comando corre 'todo' para Sabaneta.",
    )
    sub = p.add_subparsers(dest="comando", metavar="comando")

    sub.add_parser("verificar", help="revisa Python, paquetes, informe y SUMO"
                   ).set_defaults(func=_cmd_verificar)
    sub.add_parser("extraer-encuesta", help="informe .xlsx -> data/processed/*.csv"
                   ).set_defaults(func=_cmd_extraer)
    sub.add_parser("preparar-insumos", help="CSV -> vtypes, perfil horario, SUPUESTOS.md"
                   ).set_defaults(func=_cmd_insumos)

    r = sub.add_parser("construir-red", help="OpenStreetMap -> red SUMO + reporte de calidad")
    r.add_argument("municipios", nargs="*", default=[POR_DEFECTO], metavar="municipio",
                   help="uno o varios municipios del valle; varios se unen en una sola "
                        f"red conectada; '{VALLE}' son los diez (por defecto: {POR_DEFECTO})")
    r.add_argument("--osm", type=Path, metavar="ARCHIVO",
                   help="usar un .osm local en vez del cache o la descarga")
    r.add_argument("--descargar", action="store_true",
                   help="descargar de nuevo aunque haya cache")
    r.add_argument("--adivinar-semaforos", action="store_true",
                   help="activar tls.guess (inventa semaforos donde OSM no tiene)")
    r.set_defaults(func=_cmd_red)

    t = sub.add_parser("prueba-tecnica", help="demanda SINTETICA sobre la red + .sumocfg")
    cual = t.add_mutually_exclusive_group()
    cual.add_argument("--municipio", nargs="+", default=[POR_DEFECTO],
                      help="usar la red OSM de este municipio o de esta union de "
                           f"municipios; '{VALLE}' son los diez (por defecto: {POR_DEFECTO})")
    cual.add_argument("--valle", action="store_true",
                      help="usar la red del valle completo (los diez municipios)")
    cual.add_argument("--red", type=Path, metavar="NET_XML", help="usar este .net.xml")
    cual.add_argument("--reticula", action="store_true",
                      help="usar una reticula sintetica en vez de una red real")
    t.set_defaults(func=_cmd_prueba)

    s = sub.add_parser("simular", help="corre SUMO y resume teleports y tiempos")
    s.add_argument("--gui", action="store_true", help="abrir en sumo-gui en vez de correr")
    s.set_defaults(func=_cmd_simular)

    todo = sub.add_parser("todo", help="pipeline completo, en orden")
    todo.add_argument("municipios", nargs="*", default=[POR_DEFECTO], metavar="municipio",
                      help=f"municipios a incluir; '{VALLE}' son los diez (por defecto: {POR_DEFECTO})")
    todo.add_argument("--gui", action="store_true", help="terminar abriendo sumo-gui")
    todo.set_defaults(func=_cmd_todo)

    sub.add_parser("limpiar", help="borra lo regenerable (no toca data/raw)"
                   ).set_defaults(func=_cmd_limpiar)
    return p


def main(argv=None) -> int:
    parser = construir_parser()
    args = parser.parse_args(argv)
    if args.comando is None:
        args = parser.parse_args(["todo"])
    try:
        siguiente = args.func(args)
    except ErrorPipeline as e:
        print(f"\nERROR: {e}")
        return 1
    if isinstance(siguiente, int):
        return siguiente
    if siguiente:
        print(f"\nPaso siguiente: python main.py {siguiente}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
