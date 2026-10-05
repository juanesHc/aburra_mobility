# Calidad de la red vial — Caldas

Generado automáticamente por `python main.py construir-red`. No editar a mano:
se sobrescribe en cada corrida.

- Fuente: OpenStreetMap.
  - Caldas: relación 1307283 (DIVIPOLA 05129), `caldas_city.osm.xml`, datos al 2026-10-03T16:17:36Z.
- Red: `caldas.net.xml` (podada) y `caldas_sin_podar.net.xml` (antes de podar).
- Tolerancia de unión de intersecciones: 15 m. `tls.guess`: desactivado.

## Resumen

|  | valor |
|---|---:|
| Nodos (intersecciones y extremos) | 837 |
| Aristas (un sentido cada una) | 1903 |
| Longitud total por sentido | 398.8 km |
| Carril-km | 420.2 |
| Semáforos (controladores) | 7 |
| Advertencias al cargar en sumo | 0 |

Los kilómetros se cuentan por sentido: una vía de doble sentido aporta dos veces
su longitud. Es la medida que importa para capacidad.

## Vías por tipo y carriles

| tipo | aristas | km | carriles/sentido (media) | carriles por defecto | velocidad por defecto |
|---|---:|---:|---:|---:|---:|
| unclassified | 170 | 143.2 | 1.00 | 170 (100.0 % de km) | 166 (96.4 % de km) |
| residential | 1444 | 136.3 | 1.01 | 1297 (94.9 % de km) | 1440 (99.9 % de km) |
| tertiary | 62 | 53.5 | 1.06 | 47 (98.3 % de km) | 60 (99.9 % de km) |
| primary | 24 | 29.3 | 1.00 | 0 (0.0 % de km) | 0 (0.0 % de km) |
| trunk | 71 | 25.0 | 1.82 | 0 (0.0 % de km) | 57 (81.6 % de km) |
| secondary | 105 | 9.1 | 1.06 | 11 (8.2 % de km) | 85 (71.2 % de km) |
| trunk_link | 27 | 2.4 | 1.41 | 2 (5.1 % de km) | 9 (64.5 % de km) |

**1527 de 1903 aristas (81.8 % de los km) no tienen `lanes` en OSM** y netconvert les puso el valor del typemap (1 carril por sentido en secundaria, terciaria y locales; 2 en primaria y troncal). En la red arterial (troncal a terciaria) la cifra es 60 de 289 aristas (44.8 % de los km).

| carriles por sentido | km | % de la red |
|---|---:|---:|
| 1 | 377.6 | 94.7 % |
| 2 | 21.0 | 5.3 % |
| 3 o más | 0.2 | 0.1 % |

Relevancia para la moto: con `lateral-resolution` 0,8 m el modelo sublane deja
que la moto se filtre entre filas en vías de dos o más carriles por sentido. En
vías de un carril solo puede adelantar dentro del mismo carril si el ancho lo
permite; OSM casi nunca trae `width`, así que los anchos de carril quedan en el valor por defecto (distribución: 3.2 m: 1985, 2.5 m: 6).
Ningún parámetro del vType `moto` se tocó.

**Calles de carril compartido: 6 aristas, 0.25 km.** Vienen de vías con `lanes=1` y doble sentido en OSM, sin `width`. netconvert las partía en dos carriles de 1.6 m, más angostos que un auto (1.8 m); se ensancharon a 2.5 m por sentido (ver supuesto `carril_compartido`). Si alguna calle resulta ser de un solo sentido o más ancha, corregirla en OSM es mejor que ajustarla aquí:

- [990505011](https://www.openstreetmap.org/way/990505011), [1528035894](https://www.openstreetmap.org/way/1528035894), [1529214485](https://www.openstreetmap.org/way/1529214485)

Tras el ajuste no queda ningún carril más angosto que un auto.

## Semáforos

|  | valor |
|---|---:|
| Nodos semáforo en OSM: `highway=traffic_signals` | 9 |
| Nodos semáforo en OSM: solo `crossing=traffic_signals` (peatonal) | 12 |
| Controladores en la red | 7 |
| … ubicados a partir de OSM | 7 |
| … adivinados por `tls.guess` (sin señal OSM a ≤ 35 m) | 0 |
| Cruces controlados (tras `tls.join`) | 7 |
| Señales OSM que no quedaron en ningún semáforo | 0 |
| Controladores con plan real | **0** |

Ciclos generados: mín 90 s, mediana 90 s, máx 90 s. **Todos los planes semafóricos son inventados** por netconvert (tiempos fijos genéricos). Los planes reales de Medellín los tiene el SIMM y no son públicos en formato utilizable. Esto afecta directamente la capacidad de cada intersección semaforizada.

## Restricciones de giro y carriles de giro

OSM trae **4 relaciones de restricción de giro** para 557 intersecciones con al menos dos entradas y dos salidas (0.7 por cada 100). Cualquier giro prohibido que no esté mapeado queda permitido en la simulación.

| tipo | relaciones |
|---|---:|
| no_u_turn | 2 |
| no_left_turn | 1 |
| no_straight_on | 1 |

Flechas de giro por carril (`turn:lanes`) en OSM, por tipo de vía:

| tipo | vías con turn:lanes | vías del tipo |
|---|---:|---:|
| service | 0 | 599 |
| residential | 1 | 492 |
| unclassified | 0 | 85 |
| trunk | 0 | 66 |
| tertiary | 0 | 33 |
| trunk_link | 0 | 18 |
| secondary | 0 | 14 |
| primary | 0 | 7 |

## Componentes desconectados

Calculado sobre la red **antes de podar**, con las conexiones que puede usar
un auto.

|  | valor |
|---|---:|
| Componentes débilmente conexos | 2 |
| Aristas en el mayor (débil) | 1903 (99.4 %) |
| Componentes fuertemente conexos | 21 |
| Aristas en el mayor (fuerte) | 1884 (98.4 %) |
| Componentes fuertes de más de 1 arista, aparte del mayor | 1 |
| Aristas conservadas | 1903 |
| Aristas podadas: islas (otro componente débil) | 12 |
| Aristas podadas: trampas dentro del componente principal | 0 |

Una arista se conserva si un vehículo puede recorrerla de principio a fin: porque
llega al componente fuerte principal, porque se llega a ella desde él, o porque
está entre una entrada y una salida de la red (vías de paso por el borde).
Se poda lo demás: islas sin conexión vial con el resto y trampas (tramos de
sentido único a los que no se puede llegar o que no llevan a ninguna parte).
Casi siempre son errores de sentido o de conexión en OSM.

Islas: 12 aristas, 5.76 km, en estas vías OSM. Revisar en netedit o corregir en OSM (una isla suele ser una conexión que falta en el mapa, o una vía de un tipo que no se descarga, como `track`):

- [253852289](https://www.openstreetmap.org/way/253852289), [253874849](https://www.openstreetmap.org/way/253874849), [1077898733](https://www.openstreetmap.org/way/1077898733), [1077904239](https://www.openstreetmap.org/way/1077904239)

## Aristas de entrada y salida (`is_fringe`)

|  | entradas | salidas |
|---|---:|---:|
| Total | 227 | 227 |
| … en vías arteriales (troncal a terciaria) | 6 | 6 |
| … en vías locales | 221 | 221 |

`is_fringe` marca toda arista cuyo nodo extremo no tiene otra continuación.
Eso incluye los cruces reales del límite municipal, pero también las calles
ciegas internas. Las entradas en vías arteriales son casi todas conexiones con
los municipios vecinos; las locales son mayoritariamente calles sin salida.
La demanda sintética de `python main.py prueba-tecnica` se reparte
uniformemente entre todas, así que la mayoría de esos viajes entran y salen
por calles ciegas: otra razón por la que esa demanda no representa nada.

## Advertencias de netconvert

Salida completa en `caldas_netconvert.log`.

| mensaje | veces |
|---|---:|
| Speed of % connection '%' reduced by % due to turning radius of % (length=%, angle=%). | 38 |
| Not joining junctions % (%). | 21 |
| Intersecting left turns at junction '%' from lane '%' and lane '%' (increase junction radius to avoid this). | 9 |
| Reducing junction cluster % (%). | 9 |
| Found sharp turn with radius % at the % of edge '%'. | 7 |
| Speed of straight connection % reduced by % due to turning radius of % (length=%, angle=%). | 5 |
| Intersecting left turns at junction % from lane % and lane % (increase junction radius to avoid this). | 5 |
| Removed a road without junctions: %. | 5 |
| Found angle of % degrees at edge %, segment %. | 4 |
| Found sharp turn with radius % at the start of edge %. | 4 |
| Removed a road without junctions: -%. | 3 |
| Ambiguity in turnarounds computation at junction %. | 3 |
| Discarding unknown compound % in type % (first occurrence for edge %). | 2 |
| Removed a road without junctions: -%,-%. | 2 |
| Reducing junction cluster %,%,%,%,%,% (parallel incoming -%,%). | 1 |

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
