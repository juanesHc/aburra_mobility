# Calidad de la red vial — Sabaneta

Generado automáticamente por `python main.py construir-red`. No editar a mano:
se sobrescribe en cada corrida.

- Fuente: OpenStreetMap.
  - Sabaneta: relación 1307270 (DIVIPOLA 05631), `sabaneta_city.osm.xml`, datos al 2026-09-24T02:33:48Z.
- Red: `sabaneta.net.xml` (podada) y `sabaneta_sin_podar.net.xml` (antes de podar).
- Tolerancia de unión de intersecciones: 15 m. `tls.guess`: desactivado.

## Resumen

|  | valor |
|---|---:|
| Nodos (intersecciones y extremos) | 822 |
| Aristas (un sentido cada una) | 1583 |
| Longitud total por sentido | 169.0 km |
| Carril-km | 221.2 |
| Semáforos (controladores) | 17 |
| Advertencias al cargar en sumo | 0 |

Los kilómetros se cuentan por sentido: una vía de doble sentido aporta dos veces
su longitud. Es la medida que importa para capacidad.

## Vías por tipo y carriles

| tipo | aristas | km | carriles/sentido (media) | carriles por defecto | velocidad por defecto |
|---|---:|---:|---:|---:|---:|
| residential | 1254 | 122.6 | 1.17 | 782 (73.4 % de km) | 1108 (88.9 % de km) |
| unclassified | 24 | 14.0 | 1.08 | 18 (90.5 % de km) | 24 (100.0 % de km) |
| trunk | 36 | 12.8 | 2.64 | 0 (0.0 % de km) | 2 (1.2 % de km) |
| tertiary | 136 | 10.7 | 1.54 | 7 (17.6 % de km) | 82 (61.2 % de km) |
| primary | 50 | 4.5 | 3.04 | 0 (0.0 % de km) | 0 (0.0 % de km) |
| secondary | 39 | 2.8 | 1.95 | 0 (0.0 % de km) | 14 (44.3 % de km) |
| trunk_link | 20 | 0.8 | 1.40 | 2 (1.3 % de km) | 20 (100.0 % de km) |
| primary_link | 20 | 0.6 | 1.35 | 0 (0.0 % de km) | 18 (85.5 % de km) |
| tertiary_link | 2 | 0.2 | 1.00 | 0 (0.0 % de km) | 1 (2.8 % de km) |
| secondary_link | 2 | 0.0 | 2.00 | 0 (0.0 % de km) | 2 (100.0 % de km) |

**809 de 1583 aristas (61.8 % de los km) no tienen `lanes` en OSM** y netconvert les puso el valor del typemap (1 carril por sentido en secundaria, terciaria y locales; 2 en primaria y troncal). En la red arterial (troncal a terciaria) la cifra es 9 de 305 aristas (5.8 % de los km).

| carriles por sentido | km | % de la red |
|---|---:|---:|
| 1 | 130.4 | 77.1 % |
| 2 | 25.2 | 14.9 % |
| 3 o más | 13.4 | 8.0 % |

Relevancia para la moto: con `lateral-resolution` 0,8 m el modelo sublane deja
que la moto se filtre entre filas en vías de dos o más carriles por sentido. En
vías de un carril solo puede adelantar dentro del mismo carril si el ancho lo
permite; OSM casi nunca trae `width`, así que los anchos de carril quedan en el valor por defecto (distribución: 3.2 m: 2022, 2.5 m: 52, 3.0 m: 10, 4.0 m: 2).
Ningún parámetro del vType `moto` se tocó.

**Calles de carril compartido: 44 aristas, 3.64 km.** Vienen de vías con `lanes=1` y doble sentido en OSM, sin `width`. netconvert las partía en dos carriles de 1.6 m, más angostos que un auto (1.8 m); se ensancharon a 2.5 m por sentido (ver supuesto `carril_compartido`). Si alguna calle resulta ser de un solo sentido o más ancha, corregirla en OSM es mejor que ajustarla aquí:

- [320911469](https://www.openstreetmap.org/way/320911469), [455579551](https://www.openstreetmap.org/way/455579551), [455579552](https://www.openstreetmap.org/way/455579552), [456703485](https://www.openstreetmap.org/way/456703485), [456703487](https://www.openstreetmap.org/way/456703487), [457124576](https://www.openstreetmap.org/way/457124576), [561300007](https://www.openstreetmap.org/way/561300007), [567571027](https://www.openstreetmap.org/way/567571027), [578270390](https://www.openstreetmap.org/way/578270390), [578270392](https://www.openstreetmap.org/way/578270392), [578283519](https://www.openstreetmap.org/way/578283519), [578295782](https://www.openstreetmap.org/way/578295782), [1018545358](https://www.openstreetmap.org/way/1018545358), [1052911603](https://www.openstreetmap.org/way/1052911603), [1074482954](https://www.openstreetmap.org/way/1074482954), [1134777269](https://www.openstreetmap.org/way/1134777269), [1136665166](https://www.openstreetmap.org/way/1136665166), [1179903908](https://www.openstreetmap.org/way/1179903908), [1306627566](https://www.openstreetmap.org/way/1306627566)

Tras el ajuste no queda ningún carril más angosto que un auto.

## Semáforos

|  | valor |
|---|---:|
| Nodos semáforo en OSM: `highway=traffic_signals` | 36 |
| Nodos semáforo en OSM: solo `crossing=traffic_signals` (peatonal) | 41 |
| Controladores en la red | 17 |
| … ubicados a partir de OSM | 17 |
| … adivinados por `tls.guess` (sin señal OSM a ≤ 35 m) | 0 |
| Cruces controlados (tras `tls.join`) | 21 |
| Señales OSM que no quedaron en ningún semáforo | 11 |
| Controladores con plan real | **0** |

Ciclos generados: mín 90 s, mediana 90 s, máx 90 s. **Todos los planes semafóricos son inventados** por netconvert (tiempos fijos genéricos). Los planes reales de Medellín los tiene el SIMM y no son públicos en formato utilizable. Esto afecta directamente la capacidad de cada intersección semaforizada.

**Señales de OSM descartadas.** `tls.discard-simple` quita los semáforos que no
están en un cruce. Conservarlos no mejora la red: recibirían un plan inventado
(82 s verde, 3 s amarillo, 5 s rojo) y alteran la agrupación de cruces vecinos;
en Sabaneta eso produjo entre 12 y 17 teleports por corrida. Su efecto real
(pasos peatonales con fase propia, control de accesos) queda sin modelar.

| señal OSM | tipo | vía | causa probable |
|---|---:|---:|---:|
| [5476158295](https://www.openstreetmap.org/node/5476158295) | peatonal | Avenida Las Vegas (primary) | paso peatonal a mitad de cuadra |
| [11986681102](https://www.openstreetmap.org/node/11986681102) | peatonal | Avenida Las Vegas (primary) | paso peatonal a mitad de cuadra |
| [11986681103](https://www.openstreetmap.org/node/11986681103) | peatonal | Avenida Las Vegas (primary) | paso peatonal a mitad de cuadra |
| [7204279970](https://www.openstreetmap.org/node/7204279970) | peatonal | Calle 52 Sur (residential) | paso peatonal a mitad de cuadra |
| [11986681088](https://www.openstreetmap.org/node/11986681088) | peatonal | Calle 68 Sur (tertiary) | paso peatonal a mitad de cuadra |
| [4065415184](https://www.openstreetmap.org/node/4065415184) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [5476158279](https://www.openstreetmap.org/node/5476158279) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [11943800084](https://www.openstreetmap.org/node/11943800084) | vehicular | Carrera 43A (secondary) | semáforo vehicular a mitad de vía |
| [13070224788](https://www.openstreetmap.org/node/13070224788) | vehicular | Carrera 43A (secondary) | semáforo vehicular a mitad de vía |
| [1379569805](https://www.openstreetmap.org/node/1379569805) | vehicular | Rotonda Mayorca (primary) | sobre el anillo de una glorieta |
| [3887482977](https://www.openstreetmap.org/node/3887482977) | vehicular | Rotonda Mayorca (primary) | sobre el anillo de una glorieta |

**Glorietas con semáforos en el anillo: Rotonda Mayorca.** En la red funcionan como glorietas con prelación para quien va dentro, y en la realidad están semaforizadas. El plan semafórico de una glorieta no se puede adivinar: hay que construirlo a mano en netedit con los tiempos reales.

## Restricciones de giro y carriles de giro

OSM trae **25 relaciones de restricción de giro** para 410 intersecciones con al menos dos entradas y dos salidas (6.1 por cada 100). Cualquier giro prohibido que no esté mapeado queda permitido en la simulación.

| tipo | relaciones |
|---|---:|
| no_left_turn | 7 |
| only_straight_on | 7 |
| only_left_turn | 6 |
| no_right_turn | 3 |
| no_u_turn | 2 |

netconvert ignoró 1 por referir vías que no están en la descarga o que no son para autos.

Flechas de giro por carril (`turn:lanes`) en OSM, por tipo de vía:

| tipo | vías con turn:lanes | vías del tipo |
|---|---:|---:|
| residential | 1 | 587 |
| service | 0 | 488 |
| tertiary | 1 | 64 |
| secondary | 0 | 56 |
| primary | 1 | 28 |
| primary_link | 1 | 17 |
| trunk_link | 0 | 17 |
| trunk | 0 | 14 |
| unclassified | 0 | 14 |

## Componentes desconectados

Calculado sobre la red **antes de podar**, con las conexiones que puede usar
un auto.

|  | valor |
|---|---:|
| Componentes débilmente conexos | 2 |
| Aristas en el mayor (débil) | 1583 (99.1 %) |
| Componentes fuertemente conexos | 69 |
| Aristas en el mayor (fuerte) | 1513 (94.7 %) |
| Componentes fuertes de más de 1 arista, aparte del mayor | 2 |
| Aristas conservadas | 1583 |
| Aristas podadas: islas (otro componente débil) | 14 |
| Aristas podadas: trampas dentro del componente principal | 0 |

Una arista se conserva si un vehículo puede recorrerla de principio a fin: porque
llega al componente fuerte principal, porque se llega a ella desde él, o porque
está entre una entrada y una salida de la red (vías de paso por el borde).
Se poda lo demás: islas sin conexión vial con el resto y trampas (tramos de
sentido único a los que no se puede llegar o que no llevan a ninguna parte).
Casi siempre son errores de sentido o de conexión en OSM.

Islas: 14 aristas, 2.90 km, en estas vías OSM. Revisar en netedit o corregir en OSM (una isla suele ser una conexión que falta en el mapa, o una vía de un tipo que no se descarga, como `track`):

- [915029783](https://www.openstreetmap.org/way/915029783), [915029784](https://www.openstreetmap.org/way/915029784), [915029785](https://www.openstreetmap.org/way/915029785), [1031597073](https://www.openstreetmap.org/way/1031597073)

## Salidas de glorieta

|  | valor |
|---|---:|
| Glorietas en la red | 7 |
| Glorietas de dos o más carriles | 3 |
| Salidas habilitadas también desde el segundo carril | 10 |

netconvert solo permite salir de una glorieta desde el carril exterior. En las de
varios carriles, un vehículo que va por el segundo carril tiene que cambiarse en el
tramo del anillo antes de su salida, que a veces mide menos de 10 m, y termina en
una frenada de emergencia. En las glorietas del valle se sale también desde el
segundo carril, así que esas salidas se habilitan desde ahí (ver el supuesto
`salidas_glorieta`). Desde el tercer carril no se habilita.

Glorietas con más salidas habilitadas: (sin nombre) (4), Rotonda El Carmelo II (3), Rotonda Mayorca (3).

## Aristas de entrada y salida (`is_fringe`)

|  | entradas | salidas |
|---|---:|---:|
| Total | 190 | 197 |
| … en vías arteriales (troncal a terciaria) | 6 | 10 |
| … en vías locales | 184 | 187 |

`is_fringe` marca toda arista cuyo nodo extremo no tiene otra continuación.
Eso incluye los cruces reales del límite municipal, pero también las calles
ciegas internas. Las entradas en vías arteriales son casi todas conexiones con
los municipios vecinos; las locales son mayoritariamente calles sin salida.
La demanda sintética de `python main.py prueba-tecnica` se reparte
uniformemente entre todas, así que la mayoría de esos viajes entran y salen
por calles ciegas: otra razón por la que esa demanda no representa nada.

## Advertencias de netconvert

Salida completa en `sabaneta_netconvert.log`.

| mensaje | veces |
|---|---:|
| Not joining junctions % (%). | 34 |
| Value of key % is not numeric (%) in edge %. | 14 |
| Speed of % connection '%' reduced by % due to turning radius of % (length=%, angle=%). | 12 |
| Speed of straight connection % reduced by % due to turning radius of % (length=%, angle=%). | 5 |
| Reducing junction cluster % (%). | 5 |
| Discarding unknown compound % in type % (first occurrence for edge %). | 4 |
| Found sharp turn with radius % at the end of edge %. | 3 |
| Found sharp turn with radius % at the % of edge '%'. | 3 |
| Discarding unusable type % (first occurrence for edge %). | 2 |
| Could not find corresponding edge or compatible lane for free-floating pt stop % (La Estrella). Thus, it will be removed! | 2 |
| Could not find corresponding edge or compatible lane for free-floating pt stop % (Sabaneta). Thus, it will be removed! | 2 |
| Ambiguity in turnarounds computation at junction %. | 2 |
| Found sharp turn with radius % at the start of edge %. | 2 |
| Replacing loaded roundabout % with %. | 2 |
| Ignoring restriction relation % with unknown to-way. | 1 |

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

### 10. `salidas_glorieta`

En las glorietas de dos o mas carriles, las salidas que netconvert solo permite desde el carril exterior se habilitan tambien desde el segundo. Desde el tercero no se habilitan. Esto aproxima como se conduce en el valle (por ejemplo, la Rotonda de Laureles); no viene de un dato y habria que confirmarlo con las señales y marcas viales reales.
