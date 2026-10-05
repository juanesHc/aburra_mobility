# Calidad de la red vial — La Estrella

Generado automáticamente por `python main.py construir-red`. No editar a mano:
se sobrescribe en cada corrida.

- Fuente: OpenStreetMap.
  - La Estrella: relación 1307284 (DIVIPOLA 05380), `la_estrella_city.osm.xml`, datos al 2026-10-03T15:40:01Z.
- Red: `la_estrella.net.xml` (podada) y `la_estrella_sin_podar.net.xml` (antes de podar).
- Tolerancia de unión de intersecciones: 15 m. `tls.guess`: desactivado.

## Resumen

|  | valor |
|---|---:|
| Nodos (intersecciones y extremos) | 829 |
| Aristas (un sentido cada una) | 1755 |
| Longitud total por sentido | 235.4 km |
| Carril-km | 255.6 |
| Semáforos (controladores) | 3 |
| Advertencias al cargar en sumo | 0 |

Los kilómetros se cuentan por sentido: una vía de doble sentido aporta dos veces
su longitud. Es la medida que importa para capacidad.

## Vías por tipo y carriles

| tipo | aristas | km | carriles/sentido (media) | carriles por defecto | velocidad por defecto |
|---|---:|---:|---:|---:|---:|
| residential | 1292 | 165.8 | 1.02 | 1148 (92.7 % de km) | 1143 (94.0 % de km) |
| unclassified | 79 | 26.3 | 1.00 | 76 (99.2 % de km) | 79 (100.0 % de km) |
| tertiary | 249 | 21.5 | 1.26 | 36 (30.0 % de km) | 89 (41.3 % de km) |
| trunk | 41 | 10.5 | 2.17 | 0 (0.0 % de km) | 2 (1.0 % de km) |
| secondary | 79 | 10.4 | 1.05 | 0 (0.0 % de km) | 77 (97.5 % de km) |
| trunk_link | 12 | 0.9 | 1.08 | 1 (2.6 % de km) | 12 (100.0 % de km) |
| tertiary_link | 3 | 0.0 | 1.33 | 1 (37.9 % de km) | 2 (62.1 % de km) |

**1262 de 1755 aristas (79.1 % de los km) no tienen `lanes` en OSM** y netconvert les puso el valor del typemap (1 carril por sentido en secundaria, terciaria y locales; 2 en primaria y troncal). En la red arterial (troncal a terciaria) la cifra es 38 de 384 aristas (15.0 % de los km).

| carriles por sentido | km | % de la red |
|---|---:|---:|
| 1 | 216.4 | 91.9 % |
| 2 | 17.9 | 7.6 % |
| 3 o más | 1.2 | 0.5 % |

Relevancia para la moto: con `lateral-resolution` 0,8 m el modelo sublane deja
que la moto se filtre entre filas en vías de dos o más carriles por sentido. En
vías de un carril solo puede adelantar dentro del mismo carril si el ancho lo
permite; OSM casi nunca trae `width`, así que los anchos de carril quedan en el valor por defecto (distribución: 3.2 m: 1830, 2.5 m: 50, 3.0 m: 14, 2.0 m: 4).
Ningún parámetro del vType `moto` se tocó.

**Calles de carril compartido: 32 aristas, 1.53 km.** Vienen de vías con `lanes=1` y doble sentido en OSM, sin `width`. netconvert las partía en dos carriles de 1.6 m, más angostos que un auto (1.8 m); se ensancharon a 2.5 m por sentido (ver supuesto `carril_compartido`). Si alguna calle resulta ser de un solo sentido o más ancha, corregirla en OSM es mejor que ajustarla aquí:

- [460789868](https://www.openstreetmap.org/way/460789868), [499710905](https://www.openstreetmap.org/way/499710905), [1263138810](https://www.openstreetmap.org/way/1263138810), [1263138811](https://www.openstreetmap.org/way/1263138811), [1263138816](https://www.openstreetmap.org/way/1263138816), [1286697159](https://www.openstreetmap.org/way/1286697159), [1286697160](https://www.openstreetmap.org/way/1286697160), [1349457509](https://www.openstreetmap.org/way/1349457509), [1381823227](https://www.openstreetmap.org/way/1381823227), [1452865928](https://www.openstreetmap.org/way/1452865928)

Tras el ajuste no queda ningún carril más angosto que un auto.

## Semáforos

|  | valor |
|---|---:|
| Nodos semáforo en OSM: `highway=traffic_signals` | 7 |
| Nodos semáforo en OSM: solo `crossing=traffic_signals` (peatonal) | 5 |
| Controladores en la red | 3 |
| … ubicados a partir de OSM | 3 |
| … adivinados por `tls.guess` (sin señal OSM a ≤ 35 m) | 0 |
| Cruces controlados (tras `tls.join`) | 4 |
| Señales OSM que no quedaron en ningún semáforo | 4 |
| Controladores con plan real | **0** |

Ciclos generados: mín 90 s, mediana 90 s, máx 90 s. **Todos los planes semafóricos son inventados** por netconvert (tiempos fijos genéricos). Los planes reales de Medellín los tiene el SIMM y no son públicos en formato utilizable. Esto afecta directamente la capacidad de cada intersección semaforizada.

**Señales de OSM descartadas.** `tls.discard-simple` quita los semáforos que no
están en un cruce. Conservarlos no mejora la red: recibirían un plan inventado
(82 s verde, 3 s amarillo, 5 s rojo) y alteran la agrupación de cruces vecinos;
en Sabaneta eso produjo entre 12 y 17 teleports por corrida. Su efecto real
(pasos peatonales con fase propia, control de accesos) queda sin modelar.

| señal OSM | tipo | vía | causa probable |
|---|---:|---:|---:|
| [322010920](https://www.openstreetmap.org/node/322010920) | vehicular | Avenida Carrera 42 (trunk) | en el extremo de una vía (borde de la red o calle ciega) |
| [538256579](https://www.openstreetmap.org/node/538256579) | vehicular | Carrera 52D (tertiary) | en el extremo de una vía (borde de la red o calle ciega) |
| [4382694465](https://www.openstreetmap.org/node/4382694465) | peatonal | Avenida Carrera 42 (trunk) | paso peatonal a mitad de cuadra |
| [4382694466](https://www.openstreetmap.org/node/4382694466) | peatonal | Avenida Carrera 42 (trunk) | paso peatonal a mitad de cuadra |

## Restricciones de giro y carriles de giro

OSM trae **6 relaciones de restricción de giro** para 476 intersecciones con al menos dos entradas y dos salidas (1.3 por cada 100). Cualquier giro prohibido que no esté mapeado queda permitido en la simulación.

| tipo | relaciones |
|---|---:|
| no_left_turn | 6 |

netconvert ignoró 6 por referir vías que no están en la descarga o que no son para autos.

Flechas de giro por carril (`turn:lanes`) en OSM, por tipo de vía:

| tipo | vías con turn:lanes | vías del tipo |
|---|---:|---:|
| residential | 0 | 561 |
| service | 0 | 518 |
| tertiary | 3 | 106 |
| unclassified | 0 | 27 |
| trunk | 0 | 22 |
| trunk_link | 0 | 12 |
| secondary | 0 | 12 |
| tertiary_link | 0 | 5 |

## Componentes desconectados

Calculado sobre la red **antes de podar**, con las conexiones que puede usar
un auto.

|  | valor |
|---|---:|
| Componentes débilmente conexos | 3 |
| Aristas en el mayor (débil) | 1755 (98.5 %) |
| Componentes fuertemente conexos | 49 |
| Aristas en el mayor (fuerte) | 1705 (95.7 %) |
| Componentes fuertes de más de 1 arista, aparte del mayor | 4 |
| Aristas conservadas | 1755 |
| Aristas podadas: islas (otro componente débil) | 26 |
| Aristas podadas: trampas dentro del componente principal | 0 |

Una arista se conserva si un vehículo puede recorrerla de principio a fin: porque
llega al componente fuerte principal, porque se llega a ella desde él, o porque
está entre una entrada y una salida de la red (vías de paso por el borde).
Se poda lo demás: islas sin conexión vial con el resto y trampas (tramos de
sentido único a los que no se puede llegar o que no llevan a ninguna parte).
Casi siempre son errores de sentido o de conexión en OSM.

Islas: 26 aristas, 1.52 km, en estas vías OSM. Revisar en netedit o corregir en OSM (una isla suele ser una conexión que falta en el mapa, o una vía de un tipo que no se descarga, como `track`):

- [234907855](https://www.openstreetmap.org/way/234907855), [440529002](https://www.openstreetmap.org/way/440529002), [440529006](https://www.openstreetmap.org/way/440529006), [440529009](https://www.openstreetmap.org/way/440529009), [626743027](https://www.openstreetmap.org/way/626743027), [914667947](https://www.openstreetmap.org/way/914667947), [914667948](https://www.openstreetmap.org/way/914667948), [1017110430](https://www.openstreetmap.org/way/1017110430), [1017763600](https://www.openstreetmap.org/way/1017763600), [1464418409](https://www.openstreetmap.org/way/1464418409), [1464418410](https://www.openstreetmap.org/way/1464418410)

## Aristas de entrada y salida (`is_fringe`)

|  | entradas | salidas |
|---|---:|---:|
| Total | 274 | 274 |
| … en vías arteriales (troncal a terciaria) | 11 | 11 |
| … en vías locales | 263 | 263 |

`is_fringe` marca toda arista cuyo nodo extremo no tiene otra continuación.
Eso incluye los cruces reales del límite municipal, pero también las calles
ciegas internas. Las entradas en vías arteriales son casi todas conexiones con
los municipios vecinos; las locales son mayoritariamente calles sin salida.
La demanda sintética de `python main.py prueba-tecnica` se reparte
uniformemente entre todas, así que la mayoría de esos viajes entran y salen
por calles ciegas: otra razón por la que esa demanda no representa nada.

## Advertencias de netconvert

Salida completa en `la_estrella_netconvert.log`.

| mensaje | veces |
|---|---:|
| Speed of % connection '%' reduced by % due to turning radius of % (length=%, angle=%). | 23 |
| Not joining junctions % (%). | 20 |
| Found sharp turn with radius % at the % of edge '%'. | 14 |
| Reducing junction cluster % (%). | 11 |
| Value of key % is not numeric (%) in edge %. | 5 |
| Speed of straight connection % reduced by % due to turning radius of % (length=%, angle=%). | 5 |
| Intersecting left turns at junction % from lane % and lane % (increase junction radius to avoid this). | 5 |
| No way found for reference % in relation % | 4 |
| Removed a road without junctions: %. | 4 |
| Found angle of % degrees at edge %, segment %. | 4 |
| Removed a road without junctions: -%. | 3 |
| Found sharp turn with radius % at the start of edge %. | 3 |
| Discarding unknown compound % in type % (first occurrence for edge %). | 2 |
| Ignoring restriction relation % with unknown from-way. | 2 |
| Ignoring restriction relation % with unknown to-way. | 2 |

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
