# Calidad de la red vial — Itagüí

Generado automáticamente por `python main.py construir-red`. No editar a mano:
se sobrescribe en cada corrida.

- Fuente: OpenStreetMap.
  - Itagüí: relación 1343279 (DIVIPOLA 05360), `itagui_city.osm.xml`, datos al 2026-10-02T17:47:21Z.
- Red: `itagui.net.xml` (podada) y `itagui_sin_podar.net.xml` (antes de podar).
- Tolerancia de unión de intersecciones: 15 m. `tls.guess`: desactivado.

## Resumen

|  | valor |
|---|---:|
| Nodos (intersecciones y extremos) | 2068 |
| Aristas (un sentido cada una) | 4256 |
| Longitud total por sentido | 309.2 km |
| Carril-km | 388.5 |
| Semáforos (controladores) | 64 |
| Advertencias al cargar en sumo | 0 |

Los kilómetros se cuentan por sentido: una vía de doble sentido aporta dos veces
su longitud. Es la medida que importa para capacidad.

## Vías por tipo y carriles

| tipo | aristas | km | carriles/sentido (media) | carriles por defecto | velocidad por defecto |
|---|---:|---:|---:|---:|---:|
| residential | 3014 | 203.2 | 1.12 | 2101 (73.9 % de km) | 2618 (88.6 % de km) |
| tertiary | 528 | 39.2 | 1.30 | 19 (6.5 % de km) | 291 (41.8 % de km) |
| unclassified | 284 | 29.5 | 1.13 | 258 (95.4 % de km) | 284 (100.0 % de km) |
| trunk | 79 | 14.3 | 2.57 | 0 (0.0 % de km) | 0 (0.0 % de km) |
| secondary | 185 | 12.1 | 2.02 | 0 (0.0 % de km) | 146 (74.5 % de km) |
| primary | 106 | 7.8 | 2.39 | 0 (0.0 % de km) | 16 (17.6 % de km) |
| trunk_link | 38 | 2.1 | 1.42 | 5 (1.6 % de km) | 33 (95.3 % de km) |
| secondary_link | 14 | 0.5 | 1.50 | 1 (5.7 % de km) | 12 (88.6 % de km) |
| primary_link | 4 | 0.4 | 1.50 | 0 (0.0 % de km) | 4 (100.0 % de km) |
| tertiary_link | 4 | 0.2 | 1.00 | 2 (14.2 % de km) | 4 (100.0 % de km) |

**2386 de 4256 aristas (58.5 % de los km) no tienen `lanes` en OSM** y netconvert les puso el valor del typemap (1 carril por sentido en secundaria, terciaria y locales; 2 en primaria y troncal). En la red arterial (troncal a terciaria) la cifra es 27 de 958 aristas (3.5 % de los km).

| carriles por sentido | km | % de la red |
|---|---:|---:|
| 1 | 241.6 | 78.1 % |
| 2 | 56.6 | 18.3 % |
| 3 o más | 11.0 | 3.6 % |

Relevancia para la moto: con `lateral-resolution` 0,8 m el modelo sublane deja
que la moto se filtre entre filas en vías de dos o más carriles por sentido. En
vías de un carril solo puede adelantar dentro del mismo carril si el ancho lo
permite; OSM casi nunca trae `width`, así que los anchos de carril quedan en el valor por defecto (distribución: 3.2 m: 5268, 2.5 m: 38).
Ningún parámetro del vType `moto` se tocó.

**Calles de carril compartido: 38 aristas, 2.81 km.** Vienen de vías con `lanes=1` y doble sentido en OSM, sin `width`. netconvert las partía en dos carriles de 1.6 m, más angostos que un auto (1.8 m); se ensancharon a 2.5 m por sentido (ver supuesto `carril_compartido`). Si alguna calle resulta ser de un solo sentido o más ancha, corregirla en OSM es mejor que ajustarla aquí:

- [43117446](https://www.openstreetmap.org/way/43117446), [224703156](https://www.openstreetmap.org/way/224703156), [224706882](https://www.openstreetmap.org/way/224706882), [224706884](https://www.openstreetmap.org/way/224706884), [395859053](https://www.openstreetmap.org/way/395859053), [499710907](https://www.openstreetmap.org/way/499710907), [558414975](https://www.openstreetmap.org/way/558414975), [566756792](https://www.openstreetmap.org/way/566756792), [571030040](https://www.openstreetmap.org/way/571030040), [706406973](https://www.openstreetmap.org/way/706406973), [1016813936](https://www.openstreetmap.org/way/1016813936), [1016850089](https://www.openstreetmap.org/way/1016850089), [1016850091](https://www.openstreetmap.org/way/1016850091), [1293138078](https://www.openstreetmap.org/way/1293138078)

Tras el ajuste no queda ningún carril más angosto que un auto.

## Semáforos

|  | valor |
|---|---:|
| Nodos semáforo en OSM: `highway=traffic_signals` | 129 |
| Nodos semáforo en OSM: solo `crossing=traffic_signals` (peatonal) | 175 |
| Controladores en la red | 64 |
| … ubicados a partir de OSM | 64 |
| … adivinados por `tls.guess` (sin señal OSM a ≤ 35 m) | 0 |
| Cruces controlados (tras `tls.join`) | 78 |
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
| [348413119](https://www.openstreetmap.org/node/348413119) | vehicular | Calle 87 (residential) | en el extremo de una vía (borde de la red o calle ciega) |
| [538256579](https://www.openstreetmap.org/node/538256579) | vehicular | Carrera 52D (tertiary) | en el extremo de una vía (borde de la red o calle ciega) |
| [11988049451](https://www.openstreetmap.org/node/11988049451) | peatonal | Avenida 80 (primary) | paso peatonal a mitad de cuadra |
| [4382694465](https://www.openstreetmap.org/node/4382694465) | peatonal | Avenida Carrera 42 (trunk) | paso peatonal a mitad de cuadra |
| [4382694466](https://www.openstreetmap.org/node/4382694466) | peatonal | Avenida Carrera 42 (trunk) | paso peatonal a mitad de cuadra |
| [11933215254](https://www.openstreetmap.org/node/11933215254) | peatonal | Avenida Carrera 42 (trunk) | paso peatonal a mitad de cuadra |
| [11933215255](https://www.openstreetmap.org/node/11933215255) | peatonal | Avenida Carrera 42 (trunk) | paso peatonal a mitad de cuadra |
| [10557729213](https://www.openstreetmap.org/node/10557729213) | peatonal | Calle 76 (tertiary) | paso peatonal a mitad de cuadra |
| [10557707897](https://www.openstreetmap.org/node/10557707897) | peatonal | Calle 80 (residential) | paso peatonal a mitad de cuadra |
| [10557707907](https://www.openstreetmap.org/node/10557707907) | peatonal | Carrera 52D (primary) | paso peatonal a mitad de cuadra |
| [12164646632](https://www.openstreetmap.org/node/12164646632) | vehicular | (sin nombre) (tertiary) | semáforo vehicular a mitad de vía |
| [344804238](https://www.openstreetmap.org/node/344804238) | vehicular | Avenida 80 (primary) | semáforo vehicular a mitad de vía |
| [538255105](https://www.openstreetmap.org/node/538255105) | vehicular | Avenida Carrera 42 (trunk) | semáforo vehicular a mitad de vía |
| [3424987432](https://www.openstreetmap.org/node/3424987432) | vehicular | Avenida Carrera 42 (trunk) | semáforo vehicular a mitad de vía |
| [536505936](https://www.openstreetmap.org/node/536505936) | vehicular | Calle 36 (secondary) | semáforo vehicular a mitad de vía |
| [537623040](https://www.openstreetmap.org/node/537623040) | vehicular | Calle 36 (secondary) | semáforo vehicular a mitad de vía |
| [3980411913](https://www.openstreetmap.org/node/3980411913) | vehicular | Calle 36 (secondary) | semáforo vehicular a mitad de vía |
| [3980412269](https://www.openstreetmap.org/node/3980412269) | vehicular | Calle 36 (secondary) | semáforo vehicular a mitad de vía |
| [5497617231](https://www.openstreetmap.org/node/5497617231) | vehicular | Calle 36 (secondary) | semáforo vehicular a mitad de vía |
| [5497617237](https://www.openstreetmap.org/node/5497617237) | vehicular | Calle 36 (secondary) | semáforo vehicular a mitad de vía |
| [9395509539](https://www.openstreetmap.org/node/9395509539) | vehicular | Calle 37B (secondary) | semáforo vehicular a mitad de vía |
| [9395509540](https://www.openstreetmap.org/node/9395509540) | vehicular | Calle 37B (secondary) | semáforo vehicular a mitad de vía |
| [538871806](https://www.openstreetmap.org/node/538871806) | vehicular | Carrera 50A (secondary) | semáforo vehicular a mitad de vía |
| [540666908](https://www.openstreetmap.org/node/540666908) | vehicular | Carrera 50A (secondary) | semáforo vehicular a mitad de vía |
| [3579307775](https://www.openstreetmap.org/node/3579307775) | vehicular | Carrera 50A (secondary) | semáforo vehicular a mitad de vía |
| [9388098739](https://www.openstreetmap.org/node/9388098739) | vehicular | Carrera 50A (secondary) | semáforo vehicular a mitad de vía |
| [9397553651](https://www.openstreetmap.org/node/9397553651) | vehicular | Carrera 50A (secondary) | semáforo vehicular a mitad de vía |
| [5529636936](https://www.openstreetmap.org/node/5529636936) | vehicular | Carrera 52 (primary) | semáforo vehicular a mitad de vía |
| [5529636937](https://www.openstreetmap.org/node/5529636937) | vehicular | Carrera 52 (primary) | semáforo vehicular a mitad de vía |
| [9400329486](https://www.openstreetmap.org/node/9400329486) | vehicular | Carrera 52 (secondary) | semáforo vehicular a mitad de vía |
| [9400329487](https://www.openstreetmap.org/node/9400329487) | vehicular | Carrera 52 (secondary) | semáforo vehicular a mitad de vía |
| [9408098541](https://www.openstreetmap.org/node/9408098541) | vehicular | Carrera 52 (primary) | semáforo vehicular a mitad de vía |
| [9408098542](https://www.openstreetmap.org/node/9408098542) | vehicular | Carrera 52 (primary) | semáforo vehicular a mitad de vía |
| [9408219442](https://www.openstreetmap.org/node/9408219442) | vehicular | Carrera 52 (primary) | semáforo vehicular a mitad de vía |
| [9408219443](https://www.openstreetmap.org/node/9408219443) | vehicular | Carrera 52 (primary) | semáforo vehicular a mitad de vía |
| [9401025944](https://www.openstreetmap.org/node/9401025944) | vehicular | Carrera 52D (primary) | semáforo vehicular a mitad de vía |
| [12164646633](https://www.openstreetmap.org/node/12164646633) | vehicular | Carrera 55A (tertiary) | semáforo vehicular a mitad de vía |

## Restricciones de giro y carriles de giro

OSM trae **52 relaciones de restricción de giro** para 1208 intersecciones con al menos dos entradas y dos salidas (4.3 por cada 100). Cualquier giro prohibido que no esté mapeado queda permitido en la simulación.

| tipo | relaciones |
|---|---:|
| no_left_turn | 36 |
| no_right_turn | 14 |
| only_straight_on | 1 |
| only_left_turn | 1 |

netconvert ignoró 7 por referir vías que no están en la descarga o que no son para autos.

Flechas de giro por carril (`turn:lanes`) en OSM, por tipo de vía:

| tipo | vías con turn:lanes | vías del tipo |
|---|---:|---:|
| residential | 22 | 1318 |
| service | 0 | 808 |
| tertiary | 27 | 218 |
| unclassified | 0 | 163 |
| secondary | 20 | 129 |
| primary | 4 | 71 |
| trunk | 1 | 33 |
| trunk_link | 0 | 32 |
| secondary_link | 0 | 13 |
| primary_link | 0 | 9 |
| tertiary_link | 0 | 9 |

## Componentes desconectados

Calculado sobre la red **antes de podar**, con las conexiones que puede usar
un auto.

|  | valor |
|---|---:|
| Componentes débilmente conexos | 2 |
| Aristas en el mayor (débil) | 4256 (99.9 %) |
| Componentes fuertemente conexos | 74 |
| Aristas en el mayor (fuerte) | 4184 (98.2 %) |
| Componentes fuertes de más de 1 arista, aparte del mayor | 1 |
| Aristas conservadas | 4256 |
| Aristas podadas: islas (otro componente débil) | 6 |
| Aristas podadas: trampas dentro del componente principal | 0 |

Una arista se conserva si un vehículo puede recorrerla de principio a fin: porque
llega al componente fuerte principal, porque se llega a ella desde él, o porque
está entre una entrada y una salida de la red (vías de paso por el borde).
Se poda lo demás: islas sin conexión vial con el resto y trampas (tramos de
sentido único a los que no se puede llegar o que no llevan a ninguna parte).
Casi siempre son errores de sentido o de conexión en OSM.

Islas: 6 aristas, 0.48 km, en estas vías OSM. Revisar en netedit o corregir en OSM (una isla suele ser una conexión que falta en el mapa, o una vía de un tipo que no se descarga, como `track`):

- [915035460](https://www.openstreetmap.org/way/915035460), [915035461](https://www.openstreetmap.org/way/915035461), [915035462](https://www.openstreetmap.org/way/915035462), [1170553638](https://www.openstreetmap.org/way/1170553638), [1211282013](https://www.openstreetmap.org/way/1211282013)

## Aristas de entrada y salida (`is_fringe`)

|  | entradas | salidas |
|---|---:|---:|
| Total | 363 | 365 |
| … en vías arteriales (troncal a terciaria) | 18 | 17 |
| … en vías locales | 345 | 348 |

`is_fringe` marca toda arista cuyo nodo extremo no tiene otra continuación.
Eso incluye los cruces reales del límite municipal, pero también las calles
ciegas internas. Las entradas en vías arteriales son casi todas conexiones con
los municipios vecinos; las locales son mayoritariamente calles sin salida.
La demanda sintética de `python main.py prueba-tecnica` se reparte
uniformemente entre todas, así que la mayoría de esos viajes entran y salen
por calles ciegas: otra razón por la que esa demanda no representa nada.

## Advertencias de netconvert

Salida completa en `itagui_netconvert.log`.

| mensaje | veces |
|---|---:|
| Not joining junctions % (%). | 80 |
| Speed of % connection '%' reduced by % due to turning radius of % (length=%, angle=%). | 42 |
| Reducing junction cluster % (%). | 18 |
| Intersecting left turns at junction '%' from lane '%' and lane '%' (increase junction radius to avoid this). | 10 |
| Ignoring turn sign information for % lanes on edge % with % driving lanes | 8 |
| Found sharp turn with radius % at the % of edge '%'. | 7 |
| Cannot apply turn sign information for edge '%' because there are % signed directions but only % targets | 6 |
| No way found for reference % in relation % | 5 |
| Not joining junctions %,% (parallel incoming %,%). | 5 |
| Cannot apply turn sign information for edge % because there are % signed directions but only % targets | 5 |
| Cannot apply turn sign information for edge % because there are % signed connections with directions % but target edge % has only % suitable lanes | 5 |
| Speed of straight connection % reduced by % due to turning radius of % (length=%, angle=%). | 5 |
| Intersecting left turns at junction % from lane % and lane % (increase junction radius to avoid this). | 5 |
| Replacing loaded roundabout % with %. | 4 |
| Ignoring unsupported placement value % for edge %. | 3 |

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
