# Calidad de la red vial — Envigado

Generado automáticamente por `python main.py construir-red`. No editar a mano:
se sobrescribe en cada corrida.

- Fuente: OpenStreetMap.
  - Envigado: relación 1307277 (DIVIPOLA 05266), `envigado_city.osm.xml`, datos al 2026-09-24T16:07:09Z.
- Red: `envigado.net.xml` (podada) y `envigado_sin_podar.net.xml` (antes de podar).
- Tolerancia de unión de intersecciones: 15 m. `tls.guess`: desactivado.

## Resumen

|  | valor |
|---|---:|
| Nodos (intersecciones y extremos) | 2782 |
| Aristas (un sentido cada una) | 5626 |
| Longitud total por sentido | 785.8 km |
| Carril-km | 871.1 |
| Semáforos (controladores) | 67 |
| Advertencias al cargar en sumo | 0 |

Los kilómetros se cuentan por sentido: una vía de doble sentido aporta dos veces
su longitud. Es la medida que importa para capacidad.

## Vías por tipo y carriles

| tipo | aristas | km | carriles/sentido (media) | carriles por defecto | velocidad por defecto |
|---|---:|---:|---:|---:|---:|
| residential | 4066 | 417.9 | 1.04 | 3437 (87.8 % de km) | 3737 (91.6 % de km) |
| unclassified | 573 | 232.8 | 1.00 | 542 (97.7 % de km) | 563 (96.2 % de km) |
| secondary | 340 | 51.4 | 1.62 | 13 (16.4 % de km) | 96 (12.7 % de km) |
| tertiary | 315 | 39.0 | 1.36 | 42 (26.9 % de km) | 230 (88.9 % de km) |
| primary | 232 | 35.0 | 2.20 | 0 (0.0 % de km) | 114 (32.5 % de km) |
| trunk | 22 | 7.4 | 3.00 | 0 (0.0 % de km) | 0 (0.0 % de km) |
| trunk_link | 17 | 0.8 | 1.29 | 0 (0.0 % de km) | 17 (100.0 % de km) |
| primary_link | 31 | 0.7 | 1.45 | 1 (1.2 % de km) | 29 (98.7 % de km) |
| tertiary_link | 16 | 0.4 | 1.06 | 2 (31.7 % de km) | 16 (100.0 % de km) |
| secondary_link | 14 | 0.3 | 1.00 | 2 (11.0 % de km) | 14 (100.0 % de km) |

**4039 de 5626 aristas (78.1 % de los km) no tienen `lanes` en OSM** y netconvert les puso el valor del typemap (1 carril por sentido en secundaria, terciaria y locales; 2 en primaria y troncal). En la red arterial (troncal a terciaria) la cifra es 60 de 987 aristas (14.1 % de los km).

| carriles por sentido | km | % de la red |
|---|---:|---:|
| 1 | 719.0 | 91.5 % |
| 2 | 48.2 | 6.1 % |
| 3 o más | 18.6 | 2.4 % |

Relevancia para la moto: con `lateral-resolution` 0,8 m el modelo sublane deja
que la moto se filtre entre filas en vías de dos o más carriles por sentido. En
vías de un carril solo puede adelantar dentro del mismo carril si el ancho lo
permite; OSM casi nunca trae `width`, así que los anchos de carril quedan en el valor por defecto (distribución: 3.2 m: 6194, 3.0 m: 90, 2.5 m: 76, 2.0 m: 39).
Ningún parámetro del vType `moto` se tocó.

**Calles de carril compartido: 34 aristas, 6.91 km.** Vienen de vías con `lanes=1` y doble sentido en OSM, sin `width`. netconvert las partía en dos carriles de 1.6 m, más angostos que un auto (1.8 m); se ensancharon a 2.5 m por sentido (ver supuesto `carril_compartido`). Si alguna calle resulta ser de un solo sentido o más ancha, corregirla en OSM es mejor que ajustarla aquí:

- [152941086](https://www.openstreetmap.org/way/152941086), [173298643](https://www.openstreetmap.org/way/173298643), [256397530](https://www.openstreetmap.org/way/256397530), [256397531](https://www.openstreetmap.org/way/256397531), [256397532](https://www.openstreetmap.org/way/256397532), [309653824](https://www.openstreetmap.org/way/309653824), [459464049](https://www.openstreetmap.org/way/459464049), [576533563](https://www.openstreetmap.org/way/576533563), [972959707](https://www.openstreetmap.org/way/972959707), [1018601097](https://www.openstreetmap.org/way/1018601097), [1018660524](https://www.openstreetmap.org/way/1018660524), [1018660525](https://www.openstreetmap.org/way/1018660525), [1032351270](https://www.openstreetmap.org/way/1032351270), [1158538200](https://www.openstreetmap.org/way/1158538200)

Tras el ajuste no queda ningún carril más angosto que un auto.

## Semáforos

|  | valor |
|---|---:|
| Nodos semáforo en OSM: `highway=traffic_signals` | 135 |
| Nodos semáforo en OSM: solo `crossing=traffic_signals` (peatonal) | 236 |
| Controladores en la red | 67 |
| … ubicados a partir de OSM | 67 |
| … adivinados por `tls.guess` (sin señal OSM a ≤ 35 m) | 0 |
| Cruces controlados (tras `tls.join`) | 81 |
| Señales OSM que no quedaron en ningún semáforo | 37 |
| Controladores con plan real | **0** |

Ciclos generados: mín 90 s, mediana 90 s, máx 90 s. **Todos los planes semafóricos son inventados** por netconvert (tiempos fijos genéricos). Los planes reales de Medellín los tiene el SIMM y no son públicos en formato utilizable. Esto afecta directamente la capacidad de cada intersección semaforizada.

**Señales de OSM descartadas.** `tls.discard-simple` quita los semáforos que no
están en un cruce. Conservarlos no mejora la red: recibirían un plan inventado
(82 s verde, 3 s amarillo, 5 s rojo) y alteran la agrupación de cruces vecinos;
en Sabaneta eso produjo entre 12 y 17 teleports por corrida. Su efecto real
(pasos peatonales con fase propia, control de accesos) queda sin modelar.

| señal OSM | tipo | vía | causa probable |
|---|---:|---:|---:|
| [429405222](https://www.openstreetmap.org/node/429405222) | vehicular | Avenida Las Vegas (primary) | en el extremo de una vía (borde de la red o calle ciega) |
| [3367065030](https://www.openstreetmap.org/node/3367065030) | vehicular | Avenida Las Vegas (primary) | en el extremo de una vía (borde de la red o calle ciega) |
| [567932575](https://www.openstreetmap.org/node/567932575) | peatonal | Avenida Las Vegas (primary) | paso peatonal a mitad de cuadra |
| [10537074688](https://www.openstreetmap.org/node/10537074688) | peatonal | Avenida Las Vegas (primary) | paso peatonal a mitad de cuadra |
| [10537074689](https://www.openstreetmap.org/node/10537074689) | peatonal | Avenida Las Vegas (primary) | paso peatonal a mitad de cuadra |
| [11986825860](https://www.openstreetmap.org/node/11986825860) | peatonal | Avenida Las Vegas (primary) | paso peatonal a mitad de cuadra |
| [11987895116](https://www.openstreetmap.org/node/11987895116) | peatonal | Avenida Las Vegas (primary) | paso peatonal a mitad de cuadra |
| [10699863700](https://www.openstreetmap.org/node/10699863700) | peatonal | Calle 25 Sur (secondary) | paso peatonal a mitad de cuadra |
| [10699863702](https://www.openstreetmap.org/node/10699863702) | peatonal | Calle 25 Sur (secondary) | paso peatonal a mitad de cuadra |
| [11986825817](https://www.openstreetmap.org/node/11986825817) | peatonal | Calle 26 Sur (residential) | paso peatonal a mitad de cuadra |
| [10313189132](https://www.openstreetmap.org/node/10313189132) | peatonal | Calle 32 Sur (residential) | paso peatonal a mitad de cuadra |
| [10699845192](https://www.openstreetmap.org/node/10699845192) | peatonal | Calle 37 Sur (secondary) | paso peatonal a mitad de cuadra |
| [10724514140](https://www.openstreetmap.org/node/10724514140) | peatonal | Calle 38 Sur (secondary) | paso peatonal a mitad de cuadra |
| [10724514143](https://www.openstreetmap.org/node/10724514143) | peatonal | Calle 38 Sur (secondary) | paso peatonal a mitad de cuadra |
| [5927555379](https://www.openstreetmap.org/node/5927555379) | peatonal | Carrera 43A (primary) | paso peatonal a mitad de cuadra |
| [9395455241](https://www.openstreetmap.org/node/9395455241) | peatonal | Carrera 43A (primary) | paso peatonal a mitad de cuadra |
| [10312139802](https://www.openstreetmap.org/node/10312139802) | peatonal | Carrera 43A (primary) | paso peatonal a mitad de cuadra |
| [10312139803](https://www.openstreetmap.org/node/10312139803) | peatonal | Carrera 43A (primary) | paso peatonal a mitad de cuadra |
| [11935708025](https://www.openstreetmap.org/node/11935708025) | peatonal | Carrera 43A (secondary) | paso peatonal a mitad de cuadra |
| [10699845190](https://www.openstreetmap.org/node/10699845190) | peatonal | Diagonal 31 (secondary) | paso peatonal a mitad de cuadra |
| [3270883958](https://www.openstreetmap.org/node/3270883958) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [9411152884](https://www.openstreetmap.org/node/9411152884) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [9411152885](https://www.openstreetmap.org/node/9411152885) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [10331108517](https://www.openstreetmap.org/node/10331108517) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [10331108518](https://www.openstreetmap.org/node/10331108518) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [1839422348](https://www.openstreetmap.org/node/1839422348) | vehicular | Calle 36D (secondary) | semáforo vehicular a mitad de vía |
| [1863090139](https://www.openstreetmap.org/node/1863090139) | vehicular | Calle 36D (secondary) | semáforo vehicular a mitad de vía |
| [9372774845](https://www.openstreetmap.org/node/9372774845) | vehicular | Calle 36D (secondary) | semáforo vehicular a mitad de vía |
| [9395129450](https://www.openstreetmap.org/node/9395129450) | vehicular | Calle 36D (secondary) | semáforo vehicular a mitad de vía |
| [9395129451](https://www.openstreetmap.org/node/9395129451) | vehicular | Calle 36D (secondary) | semáforo vehicular a mitad de vía |
| [9395129452](https://www.openstreetmap.org/node/9395129452) | vehicular | Calle 36D (secondary) | semáforo vehicular a mitad de vía |
| [330635001](https://www.openstreetmap.org/node/330635001) | vehicular | Calle 38 Sur (secondary) | semáforo vehicular a mitad de vía |
| [1193707831](https://www.openstreetmap.org/node/1193707831) | vehicular | Carrera 43A (primary) | semáforo vehicular a mitad de vía |
| [3501089903](https://www.openstreetmap.org/node/3501089903) | vehicular | Carrera 43A (primary) | semáforo vehicular a mitad de vía |
| [10313189070](https://www.openstreetmap.org/node/10313189070) | vehicular | Carrera 43A (primary) | semáforo vehicular a mitad de vía |
| [10313189071](https://www.openstreetmap.org/node/10313189071) | vehicular | Carrera 43A (primary) | semáforo vehicular a mitad de vía |
| [9892204908](https://www.openstreetmap.org/node/9892204908) | vehicular | Rotonda Mayorca (primary) | sobre el anillo de una glorieta |

**Glorietas con semáforos en el anillo: Rotonda Mayorca.** En la red funcionan como glorietas con prelación para quien va dentro, y en la realidad están semaforizadas. El plan semafórico de una glorieta no se puede adivinar: hay que construirlo a mano en netedit con los tiempos reales.

## Restricciones de giro y carriles de giro

OSM trae **108 relaciones de restricción de giro** para 1519 intersecciones con al menos dos entradas y dos salidas (7.1 por cada 100). Cualquier giro prohibido que no esté mapeado queda permitido en la simulación.

| tipo | relaciones |
|---|---:|
| no_left_turn | 58 |
| no_right_turn | 32 |
| only_straight_on | 11 |
| no_u_turn | 5 |
| no_straight_on | 1 |
| only_right_turn | 1 |

netconvert ignoró 5 por referir vías que no están en la descarga o que no son para autos.

Flechas de giro por carril (`turn:lanes`) en OSM, por tipo de vía:

| tipo | vías con turn:lanes | vías del tipo |
|---|---:|---:|
| residential | 2 | 1901 |
| service | 0 | 1682 |
| unclassified | 0 | 242 |
| tertiary | 1 | 193 |
| secondary | 7 | 184 |
| primary | 22 | 174 |
| primary_link | 3 | 43 |
| secondary_link | 0 | 26 |
| tertiary_link | 0 | 18 |
| trunk_link | 0 | 17 |
| trunk | 0 | 8 |

## Componentes desconectados

Calculado sobre la red **antes de podar**, con las conexiones que puede usar
un auto.

|  | valor |
|---|---:|
| Componentes débilmente conexos | 6 |
| Aristas en el mayor (débil) | 5626 (98.3 %) |
| Componentes fuertemente conexos | 78 |
| Aristas en el mayor (fuerte) | 5558 (97.1 %) |
| Componentes fuertes de más de 1 arista, aparte del mayor | 5 |
| Aristas conservadas | 5626 |
| Aristas podadas: islas (otro componente débil) | 100 |
| Aristas podadas: trampas dentro del componente principal | 0 |

Una arista se conserva si un vehículo puede recorrerla de principio a fin: porque
llega al componente fuerte principal, porque se llega a ella desde él, o porque
está entre una entrada y una salida de la red (vías de paso por el borde).
Se poda lo demás: islas sin conexión vial con el resto y trampas (tramos de
sentido único a los que no se puede llegar o que no llevan a ninguna parte).
Casi siempre son errores de sentido o de conexión en OSM.

Islas: 100 aristas, 16.45 km, en estas vías OSM. Revisar en netedit o corregir en OSM (una isla suele ser una conexión que falta en el mapa, o una vía de un tipo que no se descarga, como `track`):

- [172999668](https://www.openstreetmap.org/way/172999668), [172999670](https://www.openstreetmap.org/way/172999670), [222665941](https://www.openstreetmap.org/way/222665941), [222665944](https://www.openstreetmap.org/way/222665944), [330732838](https://www.openstreetmap.org/way/330732838), [330734265](https://www.openstreetmap.org/way/330734265), [548427461](https://www.openstreetmap.org/way/548427461), [548427462](https://www.openstreetmap.org/way/548427462), [548427463](https://www.openstreetmap.org/way/548427463), [548787965](https://www.openstreetmap.org/way/548787965), [548787966](https://www.openstreetmap.org/way/548787966), [551360222](https://www.openstreetmap.org/way/551360222), [551360230](https://www.openstreetmap.org/way/551360230), [737767013](https://www.openstreetmap.org/way/737767013), [847241456](https://www.openstreetmap.org/way/847241456), [847241457](https://www.openstreetmap.org/way/847241457), [915035458](https://www.openstreetmap.org/way/915035458), [915035459](https://www.openstreetmap.org/way/915035459), [915037939](https://www.openstreetmap.org/way/915037939), [915037940](https://www.openstreetmap.org/way/915037940), [928124863](https://www.openstreetmap.org/way/928124863), [928124865](https://www.openstreetmap.org/way/928124865), [928124866](https://www.openstreetmap.org/way/928124866), [928794621](https://www.openstreetmap.org/way/928794621), [928794622](https://www.openstreetmap.org/way/928794622), [1014545193](https://www.openstreetmap.org/way/1014545193), [1014545196](https://www.openstreetmap.org/way/1014545196), [1020815166](https://www.openstreetmap.org/way/1020815166), [1078371698](https://www.openstreetmap.org/way/1078371698), [1078371699](https://www.openstreetmap.org/way/1078371699), [1078371700](https://www.openstreetmap.org/way/1078371700), [1078371701](https://www.openstreetmap.org/way/1078371701), [1078371702](https://www.openstreetmap.org/way/1078371702), [1078378834](https://www.openstreetmap.org/way/1078378834), [1175506600](https://www.openstreetmap.org/way/1175506600), [1290148037](https://www.openstreetmap.org/way/1290148037), [1457950324](https://www.openstreetmap.org/way/1457950324), [1551198023](https://www.openstreetmap.org/way/1551198023)

## Aristas de entrada y salida (`is_fringe`)

|  | entradas | salidas |
|---|---:|---:|
| Total | 702 | 699 |
| … en vías arteriales (troncal a terciaria) | 16 | 14 |
| … en vías locales | 686 | 685 |

`is_fringe` marca toda arista cuyo nodo extremo no tiene otra continuación.
Eso incluye los cruces reales del límite municipal, pero también las calles
ciegas internas. Las entradas en vías arteriales son casi todas conexiones con
los municipios vecinos; las locales son mayoritariamente calles sin salida.
La demanda sintética de `python main.py prueba-tecnica` se reparte
uniformemente entre todas, así que la mayoría de esos viajes entran y salen
por calles ciegas: otra razón por la que esa demanda no representa nada.

## Advertencias de netconvert

Salida completa en `envigado_netconvert.log`.

| mensaje | veces |
|---|---:|
| Not joining junctions % (%). | 111 |
| Speed of % connection '%' reduced by % due to turning radius of % (length=%, angle=%). | 65 |
| Reducing junction cluster % (%). | 21 |
| Intersecting left turns at junction '%' from lane '%' and lane '%' (increase junction radius to avoid this). | 20 |
| Found sharp turn with radius % at the % of edge '%'. | 14 |
| Ambiguity in turnarounds computation at junction '%'. | 13 |
| Discarding unknown compound '%' in type '%' (first occurrence for edge '%'). | 8 |
| Discarding unknown compound % in type % (first occurrence for edge %). | 5 |
| Ambiguity in turnarounds computation at junction %. | 5 |
| Found sharp turn with radius % at the start of edge %. | 5 |
| Found angle of % degrees at edge %, segment %. | 5 |
| Shape for junction % has distance % to its given position. | 5 |
| Replacing loaded roundabout % with %. | 5 |
| Cannot apply turn sign information for edge % because there are % signed directions but only % targets | 5 |
| Speed of straight connection % reduced by % due to turning radius of % (length=%, angle=%). | 5 |

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
