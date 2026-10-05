# Calidad de la red vial — Girardota

Generado automáticamente por `python main.py construir-red`. No editar a mano:
se sobrescribe en cada corrida.

- Fuente: OpenStreetMap.
  - Girardota: relación 1307263 (DIVIPOLA 05308), `girardota_city.osm.xml`, datos al 2026-10-05T00:21:21Z.
- Red: `girardota.net.xml` (podada) y `girardota_sin_podar.net.xml` (antes de podar).
- Tolerancia de unión de intersecciones: 15 m. `tls.guess`: desactivado.

## Resumen

|  | valor |
|---|---:|
| Nodos (intersecciones y extremos) | 953 |
| Aristas (un sentido cada una) | 2044 |
| Longitud total por sentido | 582.3 km |
| Carril-km | 606.4 |
| Semáforos (controladores) | 1 |
| Advertencias al cargar en sumo | 0 |

Los kilómetros se cuentan por sentido: una vía de doble sentido aporta dos veces
su longitud. Es la medida que importa para capacidad.

## Vías por tipo y carriles

| tipo | aristas | km | carriles/sentido (media) | carriles por defecto | velocidad por defecto |
|---|---:|---:|---:|---:|---:|
| unclassified | 840 | 357.3 | 1.00 | 832 (99.0 % de km) | 838 (99.8 % de km) |
| residential | 1015 | 142.4 | 1.00 | 1013 (99.9 % de km) | 1001 (97.9 % de km) |
| tertiary | 125 | 66.9 | 1.00 | 105 (76.4 % de km) | 117 (92.9 % de km) |
| trunk | 41 | 14.4 | 2.71 | 0 (0.0 % de km) | 41 (100.0 % de km) |
| trunk_link | 23 | 1.4 | 1.17 | 0 (0.0 % de km) | 13 (53.6 % de km) |

**1950 de 2044 aristas (94.0 % de los km) no tienen `lanes` en OSM** y netconvert les puso el valor del typemap (1 carril por sentido en secundaria, terciaria y locales; 2 en primaria y troncal). En la red arterial (troncal a terciaria) la cifra es 105 de 189 aristas (61.8 % de los km).

| carriles por sentido | km | % de la red |
|---|---:|---:|
| 1 | 567.3 | 97.4 % |
| 2 | 5.9 | 1.0 % |
| 3 o más | 9.1 | 1.6 % |

Relevancia para la moto: con `lateral-resolution` 0,8 m el modelo sublane deja
que la moto se filtre entre filas en vías de dos o más carriles por sentido. En
vías de un carril solo puede adelantar dentro del mismo carril si el ancho lo
permite; OSM casi nunca trae `width`, así que los anchos de carril quedan en el valor por defecto (distribución: 3.2 m: 2112, 2.5 m: 8).
Ningún parámetro del vType `moto` se tocó.

**Calles de carril compartido: 8 aristas, 2.05 km.** Vienen de vías con `lanes=1` y doble sentido en OSM, sin `width`. netconvert las partía en dos carriles de 0.5 m, más angostos que un auto (1.8 m); se ensancharon a 2.5 m por sentido (ver supuesto `carril_compartido`). Si alguna calle resulta ser de un solo sentido o más ancha, corregirla en OSM es mejor que ajustarla aquí:

- [457124358](https://www.openstreetmap.org/way/457124358), [457124359](https://www.openstreetmap.org/way/457124359), [559970074](https://www.openstreetmap.org/way/559970074), [559970075](https://www.openstreetmap.org/way/559970075), [1564508771](https://www.openstreetmap.org/way/1564508771)

Tras el ajuste no queda ningún carril más angosto que un auto.

## Semáforos

|  | valor |
|---|---:|
| Nodos semáforo en OSM: `highway=traffic_signals` | 1 |
| Nodos semáforo en OSM: solo `crossing=traffic_signals` (peatonal) | 0 |
| Controladores en la red | 1 |
| … ubicados a partir de OSM | 1 |
| … adivinados por `tls.guess` (sin señal OSM a ≤ 35 m) | 0 |
| Cruces controlados (tras `tls.join`) | 1 |
| Señales OSM que no quedaron en ningún semáforo | 0 |
| Controladores con plan real | **0** |

Ciclos generados: mín 90 s, mediana 90 s, máx 90 s. **Todos los planes semafóricos son inventados** por netconvert (tiempos fijos genéricos). Los planes reales de Medellín los tiene el SIMM y no son públicos en formato utilizable. Esto afecta directamente la capacidad de cada intersección semaforizada.

## Restricciones de giro y carriles de giro

OSM trae **2 relaciones de restricción de giro** para 560 intersecciones con al menos dos entradas y dos salidas (0.4 por cada 100). Cualquier giro prohibido que no esté mapeado queda permitido en la simulación.

| tipo | relaciones |
|---|---:|
| only_straight_on | 1 |
| only_right_turn | 1 |

Flechas de giro por carril (`turn:lanes`) en OSM, por tipo de vía:

| tipo | vías con turn:lanes | vías del tipo |
|---|---:|---:|
| service | 0 | 518 |
| residential | 0 | 436 |
| unclassified | 0 | 273 |
| tertiary | 0 | 40 |
| trunk_link | 0 | 19 |
| trunk | 0 | 12 |

## Componentes desconectados

Calculado sobre la red **antes de podar**, con las conexiones que puede usar
un auto.

|  | valor |
|---|---:|
| Componentes débilmente conexos | 1 |
| Aristas en el mayor (débil) | 2044 (100.0 %) |
| Componentes fuertemente conexos | 9 |
| Aristas en el mayor (fuerte) | 2036 (99.6 %) |
| Componentes fuertes de más de 1 arista, aparte del mayor | 0 |
| Aristas conservadas | 2044 |
| Aristas podadas: islas (otro componente débil) | 0 |
| Aristas podadas: trampas dentro del componente principal | 0 |

Una arista se conserva si un vehículo puede recorrerla de principio a fin: porque
llega al componente fuerte principal, porque se llega a ella desde él, o porque
está entre una entrada y una salida de la red (vías de paso por el borde).
Se poda lo demás: islas sin conexión vial con el resto y trampas (tramos de
sentido único a los que no se puede llegar o que no llevan a ninguna parte).
Casi siempre son errores de sentido o de conexión en OSM.

## Aristas de entrada y salida (`is_fringe`)

|  | entradas | salidas |
|---|---:|---:|
| Total | 354 | 354 |
| … en vías arteriales (troncal a terciaria) | 7 | 7 |
| … en vías locales | 347 | 347 |

`is_fringe` marca toda arista cuyo nodo extremo no tiene otra continuación.
Eso incluye los cruces reales del límite municipal, pero también las calles
ciegas internas. Las entradas en vías arteriales son casi todas conexiones con
los municipios vecinos; las locales son mayoritariamente calles sin salida.
La demanda sintética de `python main.py prueba-tecnica` se reparte
uniformemente entre todas, así que la mayoría de esos viajes entran y salen
por calles ciegas: otra razón por la que esa demanda no representa nada.

## Advertencias de netconvert

Salida completa en `girardota_netconvert.log`.

| mensaje | veces |
|---|---:|
| Speed of % connection '%' reduced by % due to turning radius of % (length=%, angle=%). | 28 |
| Not joining junctions % (%). | 17 |
| Found angle of % degrees at edge '%', segment %. | 11 |
| Found angle of % degrees at edge %, segment %. | 5 |
| Speed of straight connection % reduced by % due to turning radius of % (length=%, angle=%). | 5 |
| Intersecting left turns at junction % from lane % and lane % (increase junction radius to avoid this). | 5 |
| Found sharp turn with radius % at the % of edge '%'. | 4 |
| Removed a road without junctions: -%. | 3 |
| Removed a road without junctions: %. | 3 |
| Ambiguity in turnarounds computation at junction %. | 3 |
| Found sharp turn with radius % at the start of edge %. | 3 |
| Not joining junctions %,% (parallel incoming %,%). | 2 |
| Found sharp turn with radius % at the end of edge %. | 2 |
| Reducing junction cluster %,%,%,%,%,%,% (parallel incoming -%,-%). | 1 |
| Reducing junction cluster %,%,% (parallel outgoing -%,%). | 1 |

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
