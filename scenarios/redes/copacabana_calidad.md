# Calidad de la red vial — Copacabana

Generado automáticamente por `python main.py construir-red`. No editar a mano:
se sobrescribe en cada corrida.

- Fuente: OpenStreetMap.
  - Copacabana: relación 1307276 (DIVIPOLA 05212), `copacabana_city.osm.xml`, datos al 2026-10-04T21:03:55Z.
- Red: `copacabana.net.xml` (podada) y `copacabana_sin_podar.net.xml` (antes de podar).
- Tolerancia de unión de intersecciones: 15 m. `tls.guess`: desactivado.

## Resumen

|  | valor |
|---|---:|
| Nodos (intersecciones y extremos) | 1164 |
| Aristas (un sentido cada una) | 2519 |
| Longitud total por sentido | 491.6 km |
| Carril-km | 542.5 |
| Semáforos (controladores) | 2 |
| Advertencias al cargar en sumo | 0 |

Los kilómetros se cuentan por sentido: una vía de doble sentido aporta dos veces
su longitud. Es la medida que importa para capacidad.

## Vías por tipo y carriles

| tipo | aristas | km | carriles/sentido (media) | carriles por defecto | velocidad por defecto |
|---|---:|---:|---:|---:|---:|
| unclassified | 619 | 243.4 | 1.00 | 564 (94.6 % de km) | 609 (98.7 % de km) |
| residential | 1649 | 196.2 | 1.04 | 1387 (90.6 % de km) | 1621 (99.3 % de km) |
| trunk | 95 | 38.5 | 2.39 | 0 (0.0 % de km) | 32 (30.9 % de km) |
| secondary | 87 | 7.9 | 1.20 | 0 (0.0 % de km) | 86 (99.3 % de km) |
| tertiary | 52 | 4.5 | 1.10 | 3 (9.3 % de km) | 51 (98.4 % de km) |
| trunk_link | 12 | 1.1 | 1.50 | 0 (0.0 % de km) | 11 (95.5 % de km) |
| secondary_link | 3 | 0.1 | 1.00 | 2 (35.2 % de km) | 3 (100.0 % de km) |
| living_street | 2 | 0.0 | 1.00 | 2 (100.0 % de km) | 2 (100.0 % de km) |

**1958 de 2519 aristas (83.1 % de los km) no tienen `lanes` en OSM** y netconvert les puso el valor del typemap (1 carril por sentido en secundaria, terciaria y locales; 2 en primaria y troncal). En la red arterial (troncal a terciaria) la cifra es 5 de 249 aristas (0.9 % de los km).

| carriles por sentido | km | % de la red |
|---|---:|---:|
| 1 | 447.9 | 91.1 % |
| 2 | 37.5 | 7.6 % |
| 3 o más | 6.3 | 1.3 % |

Relevancia para la moto: con `lateral-resolution` 0,8 m el modelo sublane deja
que la moto se filtre entre filas en vías de dos o más carriles por sentido. En
vías de un carril solo puede adelantar dentro del mismo carril si el ancho lo
permite; OSM casi nunca trae `width`, así que los anchos de carril quedan en el valor por defecto (distribución: 3.2 m: 2690, 2.5 m: 54, 2.0 m: 2).
Ningún parámetro del vType `moto` se tocó.

**Calles de carril compartido: 54 aristas, 9.57 km.** Vienen de vías con `lanes=1` y doble sentido en OSM, sin `width`. netconvert las partía en dos carriles de 1.6 m, más angostos que un auto (1.8 m); se ensancharon a 2.5 m por sentido (ver supuesto `carril_compartido`). Si alguna calle resulta ser de un solo sentido o más ancha, corregirla en OSM es mejor que ajustarla aquí:

- [89062155](https://www.openstreetmap.org/way/89062155), [89062156](https://www.openstreetmap.org/way/89062156), [172540551](https://www.openstreetmap.org/way/172540551), [315063885](https://www.openstreetmap.org/way/315063885), [315063888](https://www.openstreetmap.org/way/315063888), [392616374](https://www.openstreetmap.org/way/392616374), [432421552](https://www.openstreetmap.org/way/432421552), [432532798](https://www.openstreetmap.org/way/432532798), [558401313](https://www.openstreetmap.org/way/558401313), [573767465](https://www.openstreetmap.org/way/573767465), [1018396859](https://www.openstreetmap.org/way/1018396859), [1018396860](https://www.openstreetmap.org/way/1018396860), [1022544896](https://www.openstreetmap.org/way/1022544896), [1053926714](https://www.openstreetmap.org/way/1053926714), [1416679396](https://www.openstreetmap.org/way/1416679396), [1498921050](https://www.openstreetmap.org/way/1498921050), [1498921055](https://www.openstreetmap.org/way/1498921055)

Tras el ajuste no queda ningún carril más angosto que un auto.

## Semáforos

|  | valor |
|---|---:|
| Nodos semáforo en OSM: `highway=traffic_signals` | 3 |
| Nodos semáforo en OSM: solo `crossing=traffic_signals` (peatonal) | 8 |
| Controladores en la red | 2 |
| … ubicados a partir de OSM | 2 |
| … adivinados por `tls.guess` (sin señal OSM a ≤ 35 m) | 0 |
| Cruces controlados (tras `tls.join`) | 2 |
| Señales OSM que no quedaron en ningún semáforo | 0 |
| Controladores con plan real | **0** |

Ciclos generados: mín 90 s, mediana 90 s, máx 90 s. **Todos los planes semafóricos son inventados** por netconvert (tiempos fijos genéricos). Los planes reales de Medellín los tiene el SIMM y no son públicos en formato utilizable. Esto afecta directamente la capacidad de cada intersección semaforizada.

## Restricciones de giro y carriles de giro

OSM trae **2 relaciones de restricción de giro** para 697 intersecciones con al menos dos entradas y dos salidas (0.3 por cada 100). Cualquier giro prohibido que no esté mapeado queda permitido en la simulación.

| tipo | relaciones |
|---|---:|
| only_right_turn | 1 |
| only_straight_on | 1 |

Flechas de giro por carril (`turn:lanes`) en OSM, por tipo de vía:

| tipo | vías con turn:lanes | vías del tipo |
|---|---:|---:|
| residential | 0 | 671 |
| service | 0 | 500 |
| unclassified | 0 | 197 |
| trunk | 2 | 55 |
| secondary | 0 | 32 |
| tertiary | 0 | 27 |
| trunk_link | 0 | 13 |

## Componentes desconectados

Calculado sobre la red **antes de podar**, con las conexiones que puede usar
un auto.

|  | valor |
|---|---:|
| Componentes débilmente conexos | 4 |
| Aristas en el mayor (débil) | 2519 (97.7 %) |
| Componentes fuertemente conexos | 78 |
| Aristas en el mayor (fuerte) | 2252 (87.4 %) |
| Componentes fuertes de más de 1 arista, aparte del mayor | 8 |
| Aristas conservadas | 2519 |
| Aristas podadas: islas (otro componente débil) | 58 |
| Aristas podadas: trampas dentro del componente principal | 0 |

Una arista se conserva si un vehículo puede recorrerla de principio a fin: porque
llega al componente fuerte principal, porque se llega a ella desde él, o porque
está entre una entrada y una salida de la red (vías de paso por el borde).
Se poda lo demás: islas sin conexión vial con el resto y trampas (tramos de
sentido único a los que no se puede llegar o que no llevan a ninguna parte).
Casi siempre son errores de sentido o de conexión en OSM.

Islas: 58 aristas, 48.50 km, en estas vías OSM. Revisar en netedit o corregir en OSM (una isla suele ser una conexión que falta en el mapa, o una vía de un tipo que no se descarga, como `track`):

- [155811746](https://www.openstreetmap.org/way/155811746), [155811749](https://www.openstreetmap.org/way/155811749), [155812823](https://www.openstreetmap.org/way/155812823), [258907860](https://www.openstreetmap.org/way/258907860), [258907864](https://www.openstreetmap.org/way/258907864), [258907870](https://www.openstreetmap.org/way/258907870), [258934208](https://www.openstreetmap.org/way/258934208), [259032373](https://www.openstreetmap.org/way/259032373), [389213850](https://www.openstreetmap.org/way/389213850), [389401873](https://www.openstreetmap.org/way/389401873), [429328458](https://www.openstreetmap.org/way/429328458), [540969304](https://www.openstreetmap.org/way/540969304), [549843249](https://www.openstreetmap.org/way/549843249), [549843250](https://www.openstreetmap.org/way/549843250), [556612788](https://www.openstreetmap.org/way/556612788), [556612794](https://www.openstreetmap.org/way/556612794), [556612795](https://www.openstreetmap.org/way/556612795), [556612796](https://www.openstreetmap.org/way/556612796), [654842716](https://www.openstreetmap.org/way/654842716), [1017072782](https://www.openstreetmap.org/way/1017072782), [1017097932](https://www.openstreetmap.org/way/1017097932), [1079370754](https://www.openstreetmap.org/way/1079370754), [1101374552](https://www.openstreetmap.org/way/1101374552), [1101374553](https://www.openstreetmap.org/way/1101374553), [1101374554](https://www.openstreetmap.org/way/1101374554), [1101374566](https://www.openstreetmap.org/way/1101374566), [1101374567](https://www.openstreetmap.org/way/1101374567), [1409734546](https://www.openstreetmap.org/way/1409734546)

## Aristas de entrada y salida (`is_fringe`)

|  | entradas | salidas |
|---|---:|---:|
| Total | 366 | 365 |
| … en vías arteriales (troncal a terciaria) | 5 | 4 |
| … en vías locales | 361 | 361 |

`is_fringe` marca toda arista cuyo nodo extremo no tiene otra continuación.
Eso incluye los cruces reales del límite municipal, pero también las calles
ciegas internas. Las entradas en vías arteriales son casi todas conexiones con
los municipios vecinos; las locales son mayoritariamente calles sin salida.
La demanda sintética de `python main.py prueba-tecnica` se reparte
uniformemente entre todas, así que la mayoría de esos viajes entran y salen
por calles ciegas: otra razón por la que esa demanda no representa nada.

## Advertencias de netconvert

Salida completa en `copacabana_netconvert.log`.

| mensaje | veces |
|---|---:|
| Not joining junctions % (%). | 23 |
| Speed of % connection '%' reduced by % due to turning radius of % (length=%, angle=%). | 22 |
| Intersecting left turns at junction '%' from lane '%' and lane '%' (increase junction radius to avoid this). | 10 |
| Removed a road without junctions: %. | 8 |
| Speed of straight connection % reduced by % due to turning radius of % (length=%, angle=%). | 5 |
| Intersecting left turns at junction % from lane % and lane % (increase junction radius to avoid this). | 5 |
| Found sharp turn with radius % at the % of edge '%'. | 5 |
| Ambiguity in turnarounds computation at junction %. | 4 |
| Found sharp turn with radius % at the start of edge %. | 3 |
| Discarding unknown compound % in type % (first occurrence for edge %). | 2 |
| Removed a road without junctions: -%. | 2 |
| Reducing junction cluster %,%,% (parallel incoming -%,%). | 2 |
| Not joining junctions %,% (parallel outgoing %,%). | 2 |
| Found angle of % degrees at edge %, segment %. | 2 |
| Found sharp turn with radius % at the end of edge %. | 2 |

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
