# Calidad de la red vial — Barbosa

Generado automáticamente por `python main.py construir-red`. No editar a mano:
se sobrescribe en cada corrida.

- Fuente: OpenStreetMap.
  - Barbosa: relación 1307290 (DIVIPOLA 05079), `barbosa_city.osm.xml`, datos al 2026-10-05T00:55:49Z.
- Red: `barbosa.net.xml` (podada) y `barbosa_sin_podar.net.xml` (antes de podar).
- Tolerancia de unión de intersecciones: 15 m. `tls.guess`: desactivado.

## Resumen

|  | valor |
|---|---:|
| Nodos (intersecciones y extremos) | 934 |
| Aristas (un sentido cada una) | 1955 |
| Longitud total por sentido | 892.4 km |
| Carril-km | 948.4 |
| Semáforos (controladores) | 0 |
| Advertencias al cargar en sumo | 0 |

Los kilómetros se cuentan por sentido: una vía de doble sentido aporta dos veces
su longitud. Es la medida que importa para capacidad.

## Vías por tipo y carriles

| tipo | aristas | km | carriles/sentido (media) | carriles por defecto | velocidad por defecto |
|---|---:|---:|---:|---:|---:|
| unclassified | 728 | 465.7 | 1.00 | 702 (95.4 % de km) | 728 (100.0 % de km) |
| residential | 804 | 156.0 | 1.00 | 764 (98.2 % de km) | 804 (100.0 % de km) |
| tertiary | 108 | 79.5 | 1.00 | 82 (68.8 % de km) | 98 (83.6 % de km) |
| primary | 174 | 75.6 | 1.14 | 18 (0.4 % de km) | 170 (97.9 % de km) |
| secondary | 36 | 69.4 | 1.00 | 16 (45.3 % de km) | 36 (100.0 % de km) |
| trunk | 86 | 44.8 | 2.28 | 0 (0.0 % de km) | 64 (62.8 % de km) |
| trunk_link | 18 | 1.4 | 1.50 | 2 (5.8 % de km) | 18 (100.0 % de km) |
| primary_link | 1 | 0.0 | 1.00 | 0 (0.0 % de km) | 1 (100.0 % de km) |

**1584 de 1955 aristas (76.6 % de los km) no tienen `lanes` en OSM** y netconvert les puso el valor del typemap (1 carril por sentido en secundaria, terciaria y locales; 2 en primaria y troncal). En la red arterial (troncal a terciaria) la cifra es 118 de 423 aristas (32.0 % de los km).

| carriles por sentido | km | % de la red |
|---|---:|---:|
| 1 | 845.0 | 94.7 % |
| 2 | 38.7 | 4.3 % |
| 3 o más | 8.6 | 1.0 % |

Relevancia para la moto: con `lateral-resolution` 0,8 m el modelo sublane deja
que la moto se filtre entre filas en vías de dos o más carriles por sentido. En
vías de un carril solo puede adelantar dentro del mismo carril si el ancho lo
permite; OSM casi nunca trae `width`, así que los anchos de carril quedan en el valor por defecto (distribución: 3.2 m: 2041, 2.5 m: 62).
Ningún parámetro del vType `moto` se tocó.

**Calles de carril compartido: 22 aristas, 16.07 km.** Vienen de vías con `lanes=1` y doble sentido en OSM, sin `width`. netconvert las partía en dos carriles de 1.6 m, más angostos que un auto (1.8 m); se ensancharon a 2.5 m por sentido (ver supuesto `carril_compartido`). Si alguna calle resulta ser de un solo sentido o más ancha, corregirla en OSM es mejor que ajustarla aquí:

- [240589357](https://www.openstreetmap.org/way/240589357), [595619661](https://www.openstreetmap.org/way/595619661), [1414558853](https://www.openstreetmap.org/way/1414558853), [1414558855](https://www.openstreetmap.org/way/1414558855)

Tras el ajuste no queda ningún carril más angosto que un auto.

## Semáforos

|  | valor |
|---|---:|
| Nodos semáforo en OSM: `highway=traffic_signals` | 0 |
| Nodos semáforo en OSM: solo `crossing=traffic_signals` (peatonal) | 0 |
| Controladores en la red | 0 |
| … ubicados a partir de OSM | 0 |
| … adivinados por `tls.guess` (sin señal OSM a ≤ 35 m) | 0 |
| Cruces controlados (tras `tls.join`) | 0 |
| Señales OSM que no quedaron en ningún semáforo | 0 |
| Controladores con plan real | **0** |

## Restricciones de giro y carriles de giro

OSM trae **0 relaciones de restricción de giro** para 518 intersecciones con al menos dos entradas y dos salidas (0.0 por cada 100). Cualquier giro prohibido que no esté mapeado queda permitido en la simulación.

Flechas de giro por carril (`turn:lanes`) en OSM, por tipo de vía:

| tipo | vías con turn:lanes | vías del tipo |
|---|---:|---:|
| service | 0 | 432 |
| residential | 0 | 386 |
| unclassified | 0 | 339 |
| trunk | 2 | 59 |
| primary | 0 | 56 |
| tertiary | 0 | 45 |
| secondary | 0 | 23 |
| trunk_link | 0 | 18 |

## Componentes desconectados

Calculado sobre la red **antes de podar**, con las conexiones que puede usar
un auto.

|  | valor |
|---|---:|
| Componentes débilmente conexos | 3 |
| Aristas en el mayor (débil) | 1955 (98.1 %) |
| Componentes fuertemente conexos | 13 |
| Aristas en el mayor (fuerte) | 1945 (97.6 %) |
| Componentes fuertes de más de 1 arista, aparte del mayor | 2 |
| Aristas conservadas | 1955 |
| Aristas podadas: islas (otro componente débil) | 38 |
| Aristas podadas: trampas dentro del componente principal | 0 |

Una arista se conserva si un vehículo puede recorrerla de principio a fin: porque
llega al componente fuerte principal, porque se llega a ella desde él, o porque
está entre una entrada y una salida de la red (vías de paso por el borde).
Se poda lo demás: islas sin conexión vial con el resto y trampas (tramos de
sentido único a los que no se puede llegar o que no llevan a ninguna parte).
Casi siempre son errores de sentido o de conexión en OSM.

Islas: 38 aristas, 67.66 km, en estas vías OSM. Revisar en netedit o corregir en OSM (una isla suele ser una conexión que falta en el mapa, o una vía de un tipo que no se descarga, como `track`):

- [318895019](https://www.openstreetmap.org/way/318895019), [429320672](https://www.openstreetmap.org/way/429320672), [429320677](https://www.openstreetmap.org/way/429320677), [533073068](https://www.openstreetmap.org/way/533073068), [533073070](https://www.openstreetmap.org/way/533073070), [533073071](https://www.openstreetmap.org/way/533073071), [533073074](https://www.openstreetmap.org/way/533073074), [533073093](https://www.openstreetmap.org/way/533073093), [533073094](https://www.openstreetmap.org/way/533073094), [533073098](https://www.openstreetmap.org/way/533073098), [534174875](https://www.openstreetmap.org/way/534174875), [534175047](https://www.openstreetmap.org/way/534175047), [1076528447](https://www.openstreetmap.org/way/1076528447)

## Aristas de entrada y salida (`is_fringe`)

|  | entradas | salidas |
|---|---:|---:|
| Total | 355 | 353 |
| … en vías arteriales (troncal a terciaria) | 13 | 11 |
| … en vías locales | 342 | 342 |

`is_fringe` marca toda arista cuyo nodo extremo no tiene otra continuación.
Eso incluye los cruces reales del límite municipal, pero también las calles
ciegas internas. Las entradas en vías arteriales son casi todas conexiones con
los municipios vecinos; las locales son mayoritariamente calles sin salida.
La demanda sintética de `python main.py prueba-tecnica` se reparte
uniformemente entre todas, así que la mayoría de esos viajes entran y salen
por calles ciegas: otra razón por la que esa demanda no representa nada.

## Advertencias de netconvert

Salida completa en `barbosa_netconvert.log`.

| mensaje | veces |
|---|---:|
| Speed of % connection '%' reduced by % due to turning radius of % (length=%, angle=%). | 24 |
| Found sharp turn with radius % at the % of edge '%'. | 13 |
| Removed a road without junctions: %. | 7 |
| Ambiguity in turnarounds computation at junction %. | 5 |
| Found angle of % degrees at edge %, segment %. | 5 |
| Speed of straight connection % reduced by % due to turning radius of % (length=%, angle=%). | 5 |
| Intersecting left turns at junction % from lane % and lane % (increase junction radius to avoid this). | 5 |
| Removed a road without junctions: -%. | 3 |
| Found sharp turn with radius % at the end of edge %. | 3 |
| Found angle of % degrees at edge '%', segment %. | 3 |
| Removed a road without junctions: -%,-%. | 2 |
| Not joining junctions %,% (parallel incoming -%,-%). | 2 |
| Found sharp turn with radius % at the start of edge %. | 2 |
| Ignoring unsupported placement value % for edge %. | 1 |
| Discarding unknown compound % in type % (first occurrence for edge %). | 1 |

## Carga en sumo

La red carga en `sumo` sin advertencias ni errores.

## Supuestos tomados

### 1. `semaforos_ubicacion`

Solo hay semaforos donde OSM los tiene (tls.guess desactivado). Si OSM omite un semaforo real, esa interseccion funciona con prioridad y su capacidad queda sobreestimada. Se prefirio omitir antes que inventar: en Sabaneta tls.guess agregaba 19 semaforos a los 17 de OSM. Ver la seccion Semaforos para el conteo.

### 2. `semaforos_planes`

Ningun semaforo tiene plan real. netconvert genera ciclos fijos genericos. Los planes del SIMM no son de acceso publico. Cualquier medida de demora o capacidad en intersecciones semaforizadas depende de este supuesto.

### 3. `semaforos_descartados`

Los semaforos de OSM que no estan en un cruce (pasos peatonales y semaforos a mitad de via) se descartan con tls.discard-simple. Sus detenciones reales no se modelan, asi que la capacidad de esas vias queda sobreestimada. Las glorietas semaforizadas funcionan como glorietas con prelacion hasta que se les construya el plan a mano. Ver la tabla en la seccion Semaforos.

### 4. `carriles_por_defecto`

Donde OSM no trae 'lanes', netconvert usa el typemap base: 1 carril por sentido en secundaria, terciaria y locales; 2 en primaria y troncal. No se corrigio ninguno a mano. El conteo esta en la seccion de carriles.

### 5. `carril_compartido`

Las calles con lanes=1 y doble sentido en OSM (un carril que comparten ambos sentidos) se modelan como dos carriles de 2.5 m, uno por sentido. OSM no trae su ancho real. En la realidad dos carros que se cruzan en esas calles frenan o se ceden el paso; en la simulacion se cruzan sin frenar, asi que su capacidad queda sobreestimada. La moto no puede adelantar a un auto dentro de esos carriles.

### 6. `velocidad_urbana`

Donde OSM no trae 'maxspeed' se usa 50 km/h (capa osmNetconvertUrbanDe), el limite general urbano en Colombia. Corredores con limite mayor senalizado pero no mapeado quedan subestimados.

### 7. `sin_vias_de_servicio`

Las vias highway=service (parqueaderos, accesos, vias internas de unidades cerradas) se excluyen porque el typemap no las habilita para autos. Los viajes que empiezan dentro de una unidad cerrada tendran que inyectarse en la calle publica mas cercana.

### 8. `sin_pendiente`

La red no tiene elevacion: OSM casi no trae 'ele' y no se cargo un modelo digital de terreno. En el valle, con laderas fuertes, esto subestima el consumo energetico de los vehiculos electricos. Antes de la fase de impacto en red electrica hay que agregar un DEM (netconvert heightmap.geotiff).

### 9. `poda_conectividad`

Se eliminan las aristas que no estan en ningun camino que pase por el componente fuertemente conexo principal. Si alguna era una via real mal conectada en OSM, su demanda se pierde hasta que se corrija el dato.
