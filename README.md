# aburra-mobility

Modelo de demanda de movilidad para el Valle de Aburrá, orientado a evaluar el
impacto de la electromovilidad sobre la red eléctrica.

Fuente de datos: informe agregado de la Encuesta Origen-Destino 2025 del Área
Metropolitana del Valle de Aburrá.

## Cómo correrlo

Desde `C:\dev\aburra-mobility`, en PowerShell:

```powershell
venv\Scripts\Activate.ps1       # activar el entorno
python main.py verificar        # revisar que todo esté en orden
python main.py                  # correr el pipeline completo (Sabaneta)
```

Cada etapa también se puede correr por separado. `python main.py <comando> --help`
muestra las opciones de cada una.

| Comando | Entrada | Salida |
|---|---|---|
| `extraer-encuesta` | `data/raw/Informe_*.xlsx` | 20 CSV en `data/processed/` |
| `preparar-insumos` | `data/processed/` | `scenarios/vtypes.add.xml`, `perfil_salidas.csv`, `SUPUESTOS.md` |
| `construir-red [municipio ...]` | OpenStreetMap (caché en `data/osm/`) | `scenarios/redes/<municipios>.net.xml` y `<municipios>_calidad.md` |
| `prueba-tecnica [--municipio ... \| --valle]` | red + insumos | `scenarios/prueba_tecnica/` (demanda **sintética** + `.sumocfg`) |
| `simular [--gui]` | `.sumocfg` | resumen de teleports y tiempos |
| `todo [municipio ...]` | — | las cinco anteriores, en orden |

La palabra `valle` equivale a los diez municipios:

```powershell
python main.py construir-red valle
python main.py prueba-tecnica --valle
python main.py simular --gui
```

`extraer-encuesta` lee las 22 hojas del informe y las normaliza, con chequeos que
fallan ruidosamente si el formato cambia. `preparar-insumos` deriva los insumos de
SUMO que el informe permite construir honestamente.

`construir-red` descarga la red con `osmGet.py`, la convierte con `netconvert`,
poda lo que no es ruteable y escribe un reporte de calidad. Con varios municipios
los convierte juntos en una sola red, con las fronteras conectadas. La descarga se
hace en tres partes por municipio (arterias, locales y servicio) que se guardan por
separado: si Overpass falla, al repetir el comando solo se piden las partes que
faltan. `--descargar` fuerza una descarga nueva, `--osm ARCHIVO` usa un archivo
local y `--adivinar-semaforos` activa `tls.guess`.

`prueba-tecnica` usa por defecto la red OSM de Sabaneta; `--municipio ...` elige
otra red ya construida, `--valle` la del valle completo, `--red NET_XML` un archivo
y `--reticula` una retícula sintética. Su demanda tiene perfil temporal real
y **estructura espacial inventada**: prueba la cadena de herramientas, no modela
Medellín.

## Qué falta

| Pieza | Estado | Depende de |
|---|---|---|
| Extracción del informe | Funciona | — |
| Tipos de vehículo | Funciona, sin calibrar | Aforos |
| Perfil horario | Funciona | — |
| Red vial (`.net.xml`) | Completa: los diez municipios del valle, 8.525 km por sentido | Revisión visual y planes semafóricos reales |
| Matriz OD | **Bloqueado** | Microdato EOD de AMVA |
| Simulación SUMO | Solo prueba técnica | Los dos anteriores |
| Impacto en red eléctrica | No empezado | Simulación |

El bloqueante real es el microdato. El informe agregado trae marginales de
origen y destino por separado, no la matriz conjunta, y esta no es recuperable
desde aquellas. Ver `src/aburra_mobility/demanda/matriz_od.py`, que define la
interfaz donde encajará cuando llegue.

## Estructura

```
main.py                 punto de entrada único
data/raw/               informe original — NO se edita, NO se versiona
data/processed/         CSV de la encuesta — desechables
data/osm/               caché de descargas de OpenStreetMap
scenarios/              todo lo que consume SUMO (se regenera)
  redes/                redes viales y sus reportes de calidad
  prueba_tecnica/       demanda sintética y configuración de prueba
src/aburra_mobility/
  etapas.py             el pipeline: una función por etapa, en orden
  rutas.py              todas las rutas de archivos del proyecto
  entorno.py            verificación de Python, paquetes y SUMO
  supuestos.py          registro de supuestos y SUPUESTOS.md
  errores.py            ErrorPipeline: los módulos lanzan, main.py informa
  encuesta/             lectura del informe agregado
  demanda/              matriz OD (interfaz), perfil horario, demanda sintética
  red/                  municipios, descarga y conversión OSM, conectividad,
                        semáforos, reporte de calidad, retícula
  simulacion/           tipos de vehículo, .sumocfg, ejecución de SUMO
```

Regla de diseño: `etapas.py` orquesta y no contiene lógica de dominio; los
módulos de las subcarpetas hacen el trabajo y no imprimen encabezados ni
terminan el proceso. Leer `etapas.py` de arriba abajo es leer el pipeline.

## Reglas

**Nada en `data/` se versiona.** El microdato de la EOD tiene acuerdo de uso con
AMVA, y una vez que un archivo entra al historial de git es difícil sacarlo de
verdad.

**Los archivos generados no se editan a mano.** Todo lo de `data/processed/` y
`scenarios/` se sobrescribe en la siguiente corrida. Los cambios van en el
código.

**La versión de SUMO se fija (1.27.1).** Los resultados de simulación no son
estables entre versiones: quienes trabajen en el proyecto deben correr la misma.

## Supuestos

`scenarios/SUPUESTOS.md` registra las decisiones de modelado de los insumos y los
cinco bloqueantes; `scenarios/redes/<municipio>_calidad.md` registra los de la
red vial. Ambos se regeneran en cada corrida. Conviene leerlos antes de usar
cualquier resultado.
