# Calidad de la red vial — Bello

Generado automáticamente por `python main.py construir-red`. No editar a mano:
se sobrescribe en cada corrida.

- Fuente: OpenStreetMap.
  - Bello: relación 1307262 (DIVIPOLA 05088), `bello_city.osm.xml`, datos al 2026-10-04T03:29:59Z.
- Red: `bello.net.xml` (podada) y `bello_sin_podar.net.xml` (antes de podar).
- Tolerancia de unión de intersecciones: 15 m. `tls.guess`: desactivado.

## Resumen

|  | valor |
|---|---:|
| Nodos (intersecciones y extremos) | 3135 |
| Aristas (un sentido cada una) | 7193 |
| Longitud total por sentido | 866.6 km |
| Carril-km | 958.3 |
| Semáforos (controladores) | 57 |
| Advertencias al cargar en sumo | 0 |

Los kilómetros se cuentan por sentido: una vía de doble sentido aporta dos veces
su longitud. Es la medida que importa para capacidad.

## Vías por tipo y carriles

| tipo | aristas | km | carriles/sentido (media) | carriles por defecto | velocidad por defecto |
|---|---:|---:|---:|---:|---:|
| residential | 5008 | 411.6 | 1.05 | 3484 (75.4 % de km) | 4850 (95.7 % de km) |
| unclassified | 845 | 301.6 | 1.00 | 839 (99.2 % de km) | 839 (99.2 % de km) |
| secondary | 607 | 83.3 | 1.51 | 152 (64.7 % de km) | 520 (68.3 % de km) |
| tertiary | 536 | 36.3 | 1.40 | 57 (12.3 % de km) | 528 (98.6 % de km) |
| trunk | 84 | 25.1 | 2.57 | 0 (0.0 % de km) | 55 (51.1 % de km) |
| primary | 68 | 6.6 | 2.35 | 3 (7.2 % de km) | 0 (0.0 % de km) |
| living_street | 10 | 0.9 | 1.00 | 10 (100.0 % de km) | 10 (100.0 % de km) |
| trunk_link | 16 | 0.9 | 1.38 | 0 (0.0 % de km) | 14 (66.9 % de km) |
| primary_link | 9 | 0.3 | 1.44 | 2 (15.0 % de km) | 6 (24.6 % de km) |
| secondary_link | 9 | 0.1 | 1.00 | 1 (15.2 % de km) | 9 (100.0 % de km) |
| tertiary_link | 1 | 0.0 | 1.00 | 0 (0.0 % de km) | 0 (0.0 % de km) |

**4548 de 7193 aristas (77.3 % de los km) no tienen `lanes` en OSM** y netconvert les puso el valor del typemap (1 carril por sentido en secundaria, terciaria y locales; 2 en primaria y troncal). En la red arterial (troncal a terciaria) la cifra es 215 de 1330 aristas (38.6 % de los km).

| carriles por sentido | km | % de la red |
|---|---:|---:|
| 1 | 783.1 | 90.4 % |
| 2 | 76.1 | 8.8 % |
| 3 o más | 7.5 | 0.9 % |

Relevancia para la moto: con `lateral-resolution` 0,8 m el modelo sublane deja
que la moto se filtre entre filas en vías de dos o más carriles por sentido. En
vías de un carril solo puede adelantar dentro del mismo carril si el ancho lo
permite; OSM casi nunca trae `width`, así que los anchos de carril quedan en el valor por defecto (distribución: 3.2 m: 8048, 2.5 m: 154, 2.0 m: 8, 3.5 m: 4).
Ningún parámetro del vType `moto` se tocó.

**Calles de carril compartido: 154 aristas, 13.10 km.** Vienen de vías con `lanes=1` y doble sentido en OSM, sin `width`. netconvert las partía en dos carriles de 1.0 m, más angostos que un auto (1.8 m); se ensancharon a 2.5 m por sentido (ver supuesto `carril_compartido`). Si alguna calle resulta ser de un solo sentido o más ancha, corregirla en OSM es mejor que ajustarla aquí:

- [29874143](https://www.openstreetmap.org/way/29874143), [29875909](https://www.openstreetmap.org/way/29875909), [29880205](https://www.openstreetmap.org/way/29880205), [29881321](https://www.openstreetmap.org/way/29881321), [29881358](https://www.openstreetmap.org/way/29881358), [29881491](https://www.openstreetmap.org/way/29881491), [29978696](https://www.openstreetmap.org/way/29978696), [29978699](https://www.openstreetmap.org/way/29978699), [29998292](https://www.openstreetmap.org/way/29998292), [29999158](https://www.openstreetmap.org/way/29999158), [29999203](https://www.openstreetmap.org/way/29999203), [30002041](https://www.openstreetmap.org/way/30002041), [119183691](https://www.openstreetmap.org/way/119183691), [183374493](https://www.openstreetmap.org/way/183374493), [196400025](https://www.openstreetmap.org/way/196400025), [273077631](https://www.openstreetmap.org/way/273077631), [273078667](https://www.openstreetmap.org/way/273078667), [273078676](https://www.openstreetmap.org/way/273078676), [273116745](https://www.openstreetmap.org/way/273116745), [273116748](https://www.openstreetmap.org/way/273116748), [273116749](https://www.openstreetmap.org/way/273116749), [273135617](https://www.openstreetmap.org/way/273135617), [273197831](https://www.openstreetmap.org/way/273197831), [273197832](https://www.openstreetmap.org/way/273197832), [273547467](https://www.openstreetmap.org/way/273547467), [273547468](https://www.openstreetmap.org/way/273547468), [273547479](https://www.openstreetmap.org/way/273547479), [273735870](https://www.openstreetmap.org/way/273735870), [275398235](https://www.openstreetmap.org/way/275398235), [307774910](https://www.openstreetmap.org/way/307774910), [307774911](https://www.openstreetmap.org/way/307774911), [402783206](https://www.openstreetmap.org/way/402783206), [403191883](https://www.openstreetmap.org/way/403191883), [410294665](https://www.openstreetmap.org/way/410294665), [441084607](https://www.openstreetmap.org/way/441084607), [441084608](https://www.openstreetmap.org/way/441084608), [559877422](https://www.openstreetmap.org/way/559877422), [560107413](https://www.openstreetmap.org/way/560107413), [566145689](https://www.openstreetmap.org/way/566145689), [566145693](https://www.openstreetmap.org/way/566145693)
- … y 15 más

Tras el ajuste no queda ningún carril más angosto que un auto.

## Semáforos

|  | valor |
|---|---:|
| Nodos semáforo en OSM: `highway=traffic_signals` | 99 |
| Nodos semáforo en OSM: solo `crossing=traffic_signals` (peatonal) | 166 |
| Controladores en la red | 57 |
| … ubicados a partir de OSM | 57 |
| … adivinados por `tls.guess` (sin señal OSM a ≤ 35 m) | 0 |
| Cruces controlados (tras `tls.join`) | 61 |
| Señales OSM que no quedaron en ningún semáforo | 5 |
| Controladores con plan real | **0** |

Ciclos generados: mín 90 s, mediana 90 s, máx 90 s. **Todos los planes semafóricos son inventados** por netconvert (tiempos fijos genéricos). Los planes reales de Medellín los tiene el SIMM y no son públicos en formato utilizable. Esto afecta directamente la capacidad de cada intersección semaforizada.

**Señales de OSM descartadas.** `tls.discard-simple` quita los semáforos que no
están en un cruce. Conservarlos no mejora la red: recibirían un plan inventado
(82 s verde, 3 s amarillo, 5 s rojo) y alteran la agrupación de cruces vecinos;
en Sabaneta eso produjo entre 12 y 17 teleports por corrida. Su efecto real
(pasos peatonales con fase propia, control de accesos) queda sin modelar.

| señal OSM | tipo | vía | causa probable |
|---|---:|---:|---:|
| [5758402008](https://www.openstreetmap.org/node/5758402008) | vehicular | Autopista Norte (primary) | semáforo vehicular a mitad de vía |
| [5758402009](https://www.openstreetmap.org/node/5758402009) | vehicular | Autopista Norte (primary) | semáforo vehicular a mitad de vía |
| [1339916397](https://www.openstreetmap.org/node/1339916397) | peatonal | Calle 50 (service) | sobre una vía de servicio, que no entra a la red |
| [1339916402](https://www.openstreetmap.org/node/1339916402) | vehicular | Carrera 49 (service) | sobre una vía de servicio, que no entra a la red |
| [5512719631](https://www.openstreetmap.org/node/5512719631) | vehicular | Carrera 49 (service) | sobre una vía de servicio, que no entra a la red |

## Restricciones de giro y carriles de giro

OSM trae **57 relaciones de restricción de giro** para 2074 intersecciones con al menos dos entradas y dos salidas (2.7 por cada 100). Cualquier giro prohibido que no esté mapeado queda permitido en la simulación.

| tipo | relaciones |
|---|---:|
| no_left_turn | 41 |
| no_right_turn | 10 |
| no_u_turn | 3 |
| only_straight_on | 3 |

netconvert ignoró 1 por referir vías que no están en la descarga o que no son para autos.

Flechas de giro por carril (`turn:lanes`) en OSM, por tipo de vía:

| tipo | vías con turn:lanes | vías del tipo |
|---|---:|---:|
| residential | 5 | 1638 |
| service | 0 | 1188 |
| unclassified | 1 | 394 |
| secondary | 9 | 269 |
| tertiary | 10 | 212 |
| trunk | 2 | 78 |
| primary | 2 | 35 |
| trunk_link | 0 | 19 |
| primary_link | 0 | 10 |
| secondary_link | 0 | 9 |

## Componentes desconectados

Calculado sobre la red **antes de podar**, con las conexiones que puede usar
un auto.

|  | valor |
|---|---:|
| Componentes débilmente conexos | 8 |
| Aristas en el mayor (débil) | 7193 (99.2 %) |
| Componentes fuertemente conexos | 84 |
| Aristas en el mayor (fuerte) | 7065 (97.4 %) |
| Componentes fuertes de más de 1 arista, aparte del mayor | 11 |
| Aristas conservadas | 7193 |
| Aristas podadas: islas (otro componente débil) | 60 |
| Aristas podadas: trampas dentro del componente principal | 0 |

Una arista se conserva si un vehículo puede recorrerla de principio a fin: porque
llega al componente fuerte principal, porque se llega a ella desde él, o porque
está entre una entrada y una salida de la red (vías de paso por el borde).
Se poda lo demás: islas sin conexión vial con el resto y trampas (tramos de
sentido único a los que no se puede llegar o que no llevan a ninguna parte).
Casi siempre son errores de sentido o de conexión en OSM.

Islas: 60 aristas, 45.16 km, en estas vías OSM. Revisar en netedit o corregir en OSM (una isla suele ser una conexión que falta en el mapa, o una vía de un tipo que no se descarga, como `track`):

- [62228930](https://www.openstreetmap.org/way/62228930), [156837478](https://www.openstreetmap.org/way/156837478), [485603895](https://www.openstreetmap.org/way/485603895), [485603896](https://www.openstreetmap.org/way/485603896), [485603897](https://www.openstreetmap.org/way/485603897), [485606800](https://www.openstreetmap.org/way/485606800), [485606801](https://www.openstreetmap.org/way/485606801), [485606802](https://www.openstreetmap.org/way/485606802), [558956689](https://www.openstreetmap.org/way/558956689), [558956690](https://www.openstreetmap.org/way/558956690), [558956691](https://www.openstreetmap.org/way/558956691), [575777960](https://www.openstreetmap.org/way/575777960), [914699849](https://www.openstreetmap.org/way/914699849), [914699850](https://www.openstreetmap.org/way/914699850), [963493705](https://www.openstreetmap.org/way/963493705), [963493709](https://www.openstreetmap.org/way/963493709), [992431347](https://www.openstreetmap.org/way/992431347), [992431348](https://www.openstreetmap.org/way/992431348), [992431349](https://www.openstreetmap.org/way/992431349), [992431350](https://www.openstreetmap.org/way/992431350), [992431351](https://www.openstreetmap.org/way/992431351), [1022060609](https://www.openstreetmap.org/way/1022060609), [1067543750](https://www.openstreetmap.org/way/1067543750), [1076016931](https://www.openstreetmap.org/way/1076016931), [1409358976](https://www.openstreetmap.org/way/1409358976)

## Aristas de entrada y salida (`is_fringe`)

|  | entradas | salidas |
|---|---:|---:|
| Total | 745 | 743 |
| … en vías arteriales (troncal a terciaria) | 17 | 17 |
| … en vías locales | 728 | 726 |

`is_fringe` marca toda arista cuyo nodo extremo no tiene otra continuación.
Eso incluye los cruces reales del límite municipal, pero también las calles
ciegas internas. Las entradas en vías arteriales son casi todas conexiones con
los municipios vecinos; las locales son mayoritariamente calles sin salida.
La demanda sintética de `python main.py prueba-tecnica` se reparte
uniformemente entre todas, así que la mayoría de esos viajes entran y salen
por calles ciegas: otra razón por la que esa demanda no representa nada.

## Advertencias de netconvert

Salida completa en `bello_netconvert.log`.

| mensaje | veces |
|---|---:|
| Not joining junctions % (%). | 99 |
| Found sharp turn with radius % at the % of edge '%'. | 82 |
| Speed of % connection '%' reduced by % due to turning radius of % (length=%, angle=%). | 76 |
| Reducing junction cluster % (%). | 34 |
| Found angle of % degrees at edge '%', segment %. | 25 |
| Removed a road without junctions: %. | 19 |
| Intersecting left turns at junction '%' from lane '%' and lane '%' (increase junction radius to avoid this). | 16 |
| Ambiguity in turnarounds computation at junction '%'. | 10 |
| No way found for reference '%' in relation '%' | 6 |
| Replacing loaded roundabout '%' with '%'. | 6 |
| Discarding unknown compound % in type % (first occurrence for edge %). | 5 |
| No way found for reference % in relation % | 5 |
| Removed a road without junctions: -%. | 5 |
| Ambiguity in turnarounds computation at junction %. | 5 |
| Found angle of % degrees at edge %, segment %. | 5 |

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
