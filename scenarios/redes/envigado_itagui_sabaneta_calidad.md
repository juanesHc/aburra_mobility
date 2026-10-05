# Calidad de la red vial — Envigado + Itagüí + Sabaneta

Generado automáticamente por `python main.py construir-red`. No editar a mano:
se sobrescribe en cada corrida.

- Fuente: OpenStreetMap.
  - Envigado: relación 1307277 (DIVIPOLA 05266), `envigado_city.osm.xml`, datos al 2026-09-24T16:07:09Z.
  - Itagüí: relación 1343279 (DIVIPOLA 05360), `itagui_city.osm.xml`, datos al 2026-10-02T17:47:21Z.
  - Sabaneta: relación 1307270 (DIVIPOLA 05631), `sabaneta_city.osm.xml`, datos al 2026-09-24T02:33:48Z.
- Red: `envigado_itagui_sabaneta.net.xml` (podada) y `envigado_itagui_sabaneta_sin_podar.net.xml` (antes de podar).
- Tolerancia de unión de intersecciones: 15 m. `tls.guess`: desactivado.

## Resumen

|  | valor |
|---|---:|
| Nodos (intersecciones y extremos) | 5641 |
| Aristas (un sentido cada una) | 11450 |
| Longitud total por sentido | 1255.9 km |
| Carril-km | 1463.2 |
| Semáforos (controladores) | 147 |
| Advertencias al cargar en sumo | 0 |

Los kilómetros se cuentan por sentido: una vía de doble sentido aporta dos veces
su longitud. Es la medida que importa para capacidad.

## Fronteras entre municipios

La red une 3 municipios convertidos juntos. Las vías que cruzan
el límite vienen en más de una descarga (27 vías OSM compartidas)
y netconvert las toma una sola vez. El núcleo es el componente fuertemente
conexo principal: desde cualquier punto del núcleo se llega a cualquier otro.
Si la frontera no conectara, uno de los municipios tendría casi nada en él.

|  | aristas | km | km en el núcleo | % en el núcleo |
|---|---:|---:|---:|---:|
| Envigado | 5584 | 775.4 | 765.6 | 98.7 % |
| Itagüí | 4248 | 307.1 | 298.8 | 97.3 % |
| Sabaneta | 1557 | 160.8 | 152.2 | 94.7 % |
| Vías de frontera (en más de una descarga) | 61 | 12.6 | 12.4 | 98.4 % |

Los límites con municipios que no están en la red siguen cortados: sus vías
aparecen como entradas y salidas (ver la sección de bordes).

## Vías por tipo y carriles

| tipo | aristas | km | carriles/sentido (media) | carriles por defecto | velocidad por defecto |
|---|---:|---:|---:|---:|---:|
| residential | 8338 | 743.6 | 1.09 | 6328 (81.7 % de km) | 7467 (90.3 % de km) |
| unclassified | 879 | 273.9 | 1.05 | 816 (97.0 % de km) | 869 (96.7 % de km) |
| tertiary | 976 | 88.3 | 1.35 | 68 (16.9 % de km) | 603 (65.3 % de km) |
| secondary | 558 | 65.4 | 1.77 | 13 (12.9 % de km) | 251 (24.4 % de km) |
| primary | 385 | 46.7 | 2.36 | 0 (0.0 % de km) | 129 (26.8 % de km) |
| trunk | 135 | 31.2 | 2.65 | 0 (0.0 % de km) | 2 (0.5 % de km) |
| trunk_link | 73 | 3.4 | 1.37 | 7 (1.3 % de km) | 68 (97.2 % de km) |
| primary_link | 54 | 1.7 | 1.43 | 1 (0.5 % de km) | 51 (94.8 % de km) |
| secondary_link | 30 | 0.8 | 1.30 | 3 (7.6 % de km) | 28 (93.7 % de km) |
| tertiary_link | 22 | 0.8 | 1.05 | 4 (20.3 % de km) | 21 (80.8 % de km) |

**7240 de 11450 aristas (71.4 % de los km) no tienen `lanes` en OSM** y netconvert les puso el valor del typemap (1 carril por sentido en secundaria, terciaria y locales; 2 en primaria y troncal). En la red arterial (troncal a terciaria) la cifra es 96 de 2233 aristas (9.9 % de los km).

| carriles por sentido | km | % de la red |
|---|---:|---:|
| 1 | 1088.5 | 86.7 % |
| 2 | 128.4 | 10.2 % |
| 3 o más | 39.0 | 3.1 % |

Relevancia para la moto: con `lateral-resolution` 0,8 m el modelo sublane deja
que la moto se filtre entre filas en vías de dos o más carriles por sentido. En
vías de un carril solo puede adelantar dentro del mismo carril si el ancho lo
permite; OSM casi nunca trae `width`, así que los anchos de carril quedan en el valor por defecto (distribución: 3.2 m: 13449, 2.5 m: 166, 3.0 m: 100, 2.0 m: 39).
Ningún parámetro del vType `moto` se tocó.

**Calles de carril compartido: 116 aristas, 13.36 km.** Vienen de vías con `lanes=1` y doble sentido en OSM, sin `width`. netconvert las partía en dos carriles de 1.6 m, más angostos que un auto (1.8 m); se ensancharon a 2.5 m por sentido (ver supuesto `carril_compartido`). Si alguna calle resulta ser de un solo sentido o más ancha, corregirla en OSM es mejor que ajustarla aquí:

- [43117446](https://www.openstreetmap.org/way/43117446), [152941086](https://www.openstreetmap.org/way/152941086), [173298643](https://www.openstreetmap.org/way/173298643), [224703156](https://www.openstreetmap.org/way/224703156), [224706882](https://www.openstreetmap.org/way/224706882), [224706884](https://www.openstreetmap.org/way/224706884), [256397530](https://www.openstreetmap.org/way/256397530), [256397531](https://www.openstreetmap.org/way/256397531), [256397532](https://www.openstreetmap.org/way/256397532), [309653824](https://www.openstreetmap.org/way/309653824), [320911469](https://www.openstreetmap.org/way/320911469), [395859053](https://www.openstreetmap.org/way/395859053), [455579551](https://www.openstreetmap.org/way/455579551), [455579552](https://www.openstreetmap.org/way/455579552), [456703485](https://www.openstreetmap.org/way/456703485), [456703487](https://www.openstreetmap.org/way/456703487), [457124576](https://www.openstreetmap.org/way/457124576), [459464049](https://www.openstreetmap.org/way/459464049), [499710907](https://www.openstreetmap.org/way/499710907), [558414975](https://www.openstreetmap.org/way/558414975), [561300007](https://www.openstreetmap.org/way/561300007), [566756792](https://www.openstreetmap.org/way/566756792), [567571027](https://www.openstreetmap.org/way/567571027), [571030040](https://www.openstreetmap.org/way/571030040), [576533563](https://www.openstreetmap.org/way/576533563), [578270390](https://www.openstreetmap.org/way/578270390), [578270392](https://www.openstreetmap.org/way/578270392), [578283519](https://www.openstreetmap.org/way/578283519), [578295782](https://www.openstreetmap.org/way/578295782), [706406973](https://www.openstreetmap.org/way/706406973), [972959707](https://www.openstreetmap.org/way/972959707), [1016813936](https://www.openstreetmap.org/way/1016813936), [1016850089](https://www.openstreetmap.org/way/1016850089), [1016850091](https://www.openstreetmap.org/way/1016850091), [1018545358](https://www.openstreetmap.org/way/1018545358), [1018601097](https://www.openstreetmap.org/way/1018601097), [1018660524](https://www.openstreetmap.org/way/1018660524), [1018660525](https://www.openstreetmap.org/way/1018660525), [1032351270](https://www.openstreetmap.org/way/1032351270), [1052911603](https://www.openstreetmap.org/way/1052911603)
- … y 7 más

Tras el ajuste no queda ningún carril más angosto que un auto.

## Semáforos

|  | valor |
|---|---:|
| Nodos semáforo en OSM: `highway=traffic_signals` | 297 |
| Nodos semáforo en OSM: solo `crossing=traffic_signals` (peatonal) | 452 |
| Controladores en la red | 147 |
| … ubicados a partir de OSM | 147 |
| … adivinados por `tls.guess` (sin señal OSM a ≤ 35 m) | 0 |
| Cruces controlados (tras `tls.join`) | 180 |
| Señales OSM que no quedaron en ningún semáforo | 82 |
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
| [348413119](https://www.openstreetmap.org/node/348413119) | vehicular | Calle 87 (residential) | en el extremo de una vía (borde de la red o calle ciega) |
| [538256579](https://www.openstreetmap.org/node/538256579) | vehicular | Carrera 52D (tertiary) | en el extremo de una vía (borde de la red o calle ciega) |
| [11988049451](https://www.openstreetmap.org/node/11988049451) | peatonal | Avenida 80 (primary) | paso peatonal a mitad de cuadra |
| [4382694465](https://www.openstreetmap.org/node/4382694465) | peatonal | Avenida Carrera 42 (trunk) | paso peatonal a mitad de cuadra |
| [4382694466](https://www.openstreetmap.org/node/4382694466) | peatonal | Avenida Carrera 42 (trunk) | paso peatonal a mitad de cuadra |
| [11933215254](https://www.openstreetmap.org/node/11933215254) | peatonal | Avenida Carrera 42 (trunk) | paso peatonal a mitad de cuadra |
| [11933215255](https://www.openstreetmap.org/node/11933215255) | peatonal | Avenida Carrera 42 (trunk) | paso peatonal a mitad de cuadra |
| [567932575](https://www.openstreetmap.org/node/567932575) | peatonal | Avenida Las Vegas (primary) | paso peatonal a mitad de cuadra |
| [10537074688](https://www.openstreetmap.org/node/10537074688) | peatonal | Avenida Las Vegas (primary) | paso peatonal a mitad de cuadra |
| [10537074689](https://www.openstreetmap.org/node/10537074689) | peatonal | Avenida Las Vegas (primary) | paso peatonal a mitad de cuadra |
| [11986825860](https://www.openstreetmap.org/node/11986825860) | peatonal | Avenida Las Vegas (primary) | paso peatonal a mitad de cuadra |
| [11987895116](https://www.openstreetmap.org/node/11987895116) | peatonal | Avenida Las Vegas (primary) | paso peatonal a mitad de cuadra |
| [5476158295](https://www.openstreetmap.org/node/5476158295) | peatonal | Avenida Las Vegas (primary) | paso peatonal a mitad de cuadra |
| [11986681102](https://www.openstreetmap.org/node/11986681102) | peatonal | Avenida Las Vegas (primary) | paso peatonal a mitad de cuadra |
| [11986681103](https://www.openstreetmap.org/node/11986681103) | peatonal | Avenida Las Vegas (primary) | paso peatonal a mitad de cuadra |
| [10699863700](https://www.openstreetmap.org/node/10699863700) | peatonal | Calle 25 Sur (secondary) | paso peatonal a mitad de cuadra |
| [10699863702](https://www.openstreetmap.org/node/10699863702) | peatonal | Calle 25 Sur (secondary) | paso peatonal a mitad de cuadra |
| [11986825817](https://www.openstreetmap.org/node/11986825817) | peatonal | Calle 26 Sur (residential) | paso peatonal a mitad de cuadra |
| [10313189132](https://www.openstreetmap.org/node/10313189132) | peatonal | Calle 32 Sur (residential) | paso peatonal a mitad de cuadra |
| [10699845192](https://www.openstreetmap.org/node/10699845192) | peatonal | Calle 37 Sur (secondary) | paso peatonal a mitad de cuadra |
| [10724514140](https://www.openstreetmap.org/node/10724514140) | peatonal | Calle 38 Sur (secondary) | paso peatonal a mitad de cuadra |
| [10724514143](https://www.openstreetmap.org/node/10724514143) | peatonal | Calle 38 Sur (secondary) | paso peatonal a mitad de cuadra |
| [7204279970](https://www.openstreetmap.org/node/7204279970) | peatonal | Calle 52 Sur (residential) | paso peatonal a mitad de cuadra |
| [11986681088](https://www.openstreetmap.org/node/11986681088) | peatonal | Calle 68 Sur (tertiary) | paso peatonal a mitad de cuadra |
| [10557729213](https://www.openstreetmap.org/node/10557729213) | peatonal | Calle 76 (tertiary) | paso peatonal a mitad de cuadra |
| [10557707897](https://www.openstreetmap.org/node/10557707897) | peatonal | Calle 80 (residential) | paso peatonal a mitad de cuadra |
| [5927555379](https://www.openstreetmap.org/node/5927555379) | peatonal | Carrera 43A (primary) | paso peatonal a mitad de cuadra |
| [9395455241](https://www.openstreetmap.org/node/9395455241) | peatonal | Carrera 43A (primary) | paso peatonal a mitad de cuadra |
| [10312139802](https://www.openstreetmap.org/node/10312139802) | peatonal | Carrera 43A (primary) | paso peatonal a mitad de cuadra |
| [10312139803](https://www.openstreetmap.org/node/10312139803) | peatonal | Carrera 43A (primary) | paso peatonal a mitad de cuadra |
| [11935708025](https://www.openstreetmap.org/node/11935708025) | peatonal | Carrera 43A (secondary) | paso peatonal a mitad de cuadra |
| [10557707907](https://www.openstreetmap.org/node/10557707907) | peatonal | Carrera 52D (primary) | paso peatonal a mitad de cuadra |
| [10699845190](https://www.openstreetmap.org/node/10699845190) | peatonal | Diagonal 31 (secondary) | paso peatonal a mitad de cuadra |
| [12164646632](https://www.openstreetmap.org/node/12164646632) | vehicular | (sin nombre) (tertiary) | semáforo vehicular a mitad de vía |
| [344804238](https://www.openstreetmap.org/node/344804238) | vehicular | Avenida 80 (primary) | semáforo vehicular a mitad de vía |
| [538255105](https://www.openstreetmap.org/node/538255105) | vehicular | Avenida Carrera 42 (trunk) | semáforo vehicular a mitad de vía |
| [3424987432](https://www.openstreetmap.org/node/3424987432) | vehicular | Avenida Carrera 42 (trunk) | semáforo vehicular a mitad de vía |
| [3270883958](https://www.openstreetmap.org/node/3270883958) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [9411152884](https://www.openstreetmap.org/node/9411152884) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [9411152885](https://www.openstreetmap.org/node/9411152885) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [10331108517](https://www.openstreetmap.org/node/10331108517) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [10331108518](https://www.openstreetmap.org/node/10331108518) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [4065415184](https://www.openstreetmap.org/node/4065415184) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [5476158279](https://www.openstreetmap.org/node/5476158279) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [536505936](https://www.openstreetmap.org/node/536505936) | vehicular | Calle 36 (secondary) | semáforo vehicular a mitad de vía |
| [537623040](https://www.openstreetmap.org/node/537623040) | vehicular | Calle 36 (secondary) | semáforo vehicular a mitad de vía |
| [3980411913](https://www.openstreetmap.org/node/3980411913) | vehicular | Calle 36 (secondary) | semáforo vehicular a mitad de vía |
| [3980412269](https://www.openstreetmap.org/node/3980412269) | vehicular | Calle 36 (secondary) | semáforo vehicular a mitad de vía |
| [5497617231](https://www.openstreetmap.org/node/5497617231) | vehicular | Calle 36 (secondary) | semáforo vehicular a mitad de vía |
| [5497617237](https://www.openstreetmap.org/node/5497617237) | vehicular | Calle 36 (secondary) | semáforo vehicular a mitad de vía |
| [1839422348](https://www.openstreetmap.org/node/1839422348) | vehicular | Calle 36D (secondary) | semáforo vehicular a mitad de vía |
| [1863090139](https://www.openstreetmap.org/node/1863090139) | vehicular | Calle 36D (secondary) | semáforo vehicular a mitad de vía |
| [9372774845](https://www.openstreetmap.org/node/9372774845) | vehicular | Calle 36D (secondary) | semáforo vehicular a mitad de vía |
| [9395129450](https://www.openstreetmap.org/node/9395129450) | vehicular | Calle 36D (secondary) | semáforo vehicular a mitad de vía |
| [9395129451](https://www.openstreetmap.org/node/9395129451) | vehicular | Calle 36D (secondary) | semáforo vehicular a mitad de vía |
| [9395129452](https://www.openstreetmap.org/node/9395129452) | vehicular | Calle 36D (secondary) | semáforo vehicular a mitad de vía |
| [9395509539](https://www.openstreetmap.org/node/9395509539) | vehicular | Calle 37B (secondary) | semáforo vehicular a mitad de vía |
| [9395509540](https://www.openstreetmap.org/node/9395509540) | vehicular | Calle 37B (secondary) | semáforo vehicular a mitad de vía |
| [330635001](https://www.openstreetmap.org/node/330635001) | vehicular | Calle 38 Sur (secondary) | semáforo vehicular a mitad de vía |
| [1193707831](https://www.openstreetmap.org/node/1193707831) | vehicular | Carrera 43A (primary) | semáforo vehicular a mitad de vía |
| [3501089903](https://www.openstreetmap.org/node/3501089903) | vehicular | Carrera 43A (primary) | semáforo vehicular a mitad de vía |
| [10313189070](https://www.openstreetmap.org/node/10313189070) | vehicular | Carrera 43A (primary) | semáforo vehicular a mitad de vía |
| [10313189071](https://www.openstreetmap.org/node/10313189071) | vehicular | Carrera 43A (primary) | semáforo vehicular a mitad de vía |
| [11943800084](https://www.openstreetmap.org/node/11943800084) | vehicular | Carrera 43A (secondary) | semáforo vehicular a mitad de vía |
| [13070224788](https://www.openstreetmap.org/node/13070224788) | vehicular | Carrera 43A (secondary) | semáforo vehicular a mitad de vía |
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

OSM trae **184 relaciones de restricción de giro** para 3141 intersecciones con al menos dos entradas y dos salidas (5.9 por cada 100). Cualquier giro prohibido que no esté mapeado queda permitido en la simulación.

| tipo | relaciones |
|---|---:|
| no_left_turn | 101 |
| no_right_turn | 49 |
| only_straight_on | 18 |
| no_u_turn | 7 |
| only_left_turn | 7 |
| no_straight_on | 1 |
| only_right_turn | 1 |

netconvert ignoró 12 por referir vías que no están en la descarga o que no son para autos.

Flechas de giro por carril (`turn:lanes`) en OSM, por tipo de vía:

| tipo | vías con turn:lanes | vías del tipo |
|---|---:|---:|
| residential | 25 | 3798 |
| service | 0 | 2976 |
| tertiary | 29 | 472 |
| unclassified | 0 | 418 |
| secondary | 27 | 364 |
| primary | 27 | 270 |
| primary_link | 4 | 68 |
| trunk_link | 0 | 64 |
| trunk | 1 | 53 |
| secondary_link | 0 | 41 |
| tertiary_link | 0 | 31 |

## Componentes desconectados

Calculado sobre la red **antes de podar**, con las conexiones que puede usar
un auto.

|  | valor |
|---|---:|
| Componentes débilmente conexos | 6 |
| Aristas en el mayor (débil) | 11450 (99.1 %) |
| Componentes fuertemente conexos | 142 |
| Aristas en el mayor (fuerte) | 11311 (97.9 %) |
| Componentes fuertes de más de 1 arista, aparte del mayor | 6 |
| Aristas conservadas | 11450 |
| Aristas podadas: islas (otro componente débil) | 100 |
| Aristas podadas: trampas dentro del componente principal | 0 |

Una arista se conserva si un vehículo puede recorrerla de principio a fin: porque
llega al componente fuerte principal, porque se llega a ella desde él, o porque
está entre una entrada y una salida de la red (vías de paso por el borde).
Se poda lo demás: islas sin conexión vial con el resto y trampas (tramos de
sentido único a los que no se puede llegar o que no llevan a ninguna parte).
Casi siempre son errores de sentido o de conexión en OSM.

Islas: 100 aristas, 16.13 km, en estas vías OSM. Revisar en netedit o corregir en OSM (una isla suele ser una conexión que falta en el mapa, o una vía de un tipo que no se descarga, como `track`):

- [172999668](https://www.openstreetmap.org/way/172999668), [172999670](https://www.openstreetmap.org/way/172999670), [222665941](https://www.openstreetmap.org/way/222665941), [222665944](https://www.openstreetmap.org/way/222665944), [330732838](https://www.openstreetmap.org/way/330732838), [330734265](https://www.openstreetmap.org/way/330734265), [548427461](https://www.openstreetmap.org/way/548427461), [548427462](https://www.openstreetmap.org/way/548427462), [548427463](https://www.openstreetmap.org/way/548427463), [548787965](https://www.openstreetmap.org/way/548787965), [548787966](https://www.openstreetmap.org/way/548787966), [551360222](https://www.openstreetmap.org/way/551360222), [551360230](https://www.openstreetmap.org/way/551360230), [847241456](https://www.openstreetmap.org/way/847241456), [847241457](https://www.openstreetmap.org/way/847241457), [915035460](https://www.openstreetmap.org/way/915035460), [915035461](https://www.openstreetmap.org/way/915035461), [915035462](https://www.openstreetmap.org/way/915035462), [915037939](https://www.openstreetmap.org/way/915037939), [915037940](https://www.openstreetmap.org/way/915037940), [928124863](https://www.openstreetmap.org/way/928124863), [928124865](https://www.openstreetmap.org/way/928124865), [928124866](https://www.openstreetmap.org/way/928124866), [928794621](https://www.openstreetmap.org/way/928794621), [928794622](https://www.openstreetmap.org/way/928794622), [1020815166](https://www.openstreetmap.org/way/1020815166), [1078371698](https://www.openstreetmap.org/way/1078371698), [1078371699](https://www.openstreetmap.org/way/1078371699), [1078371700](https://www.openstreetmap.org/way/1078371700), [1078371701](https://www.openstreetmap.org/way/1078371701), [1078371702](https://www.openstreetmap.org/way/1078371702), [1078378834](https://www.openstreetmap.org/way/1078378834), [1170553638](https://www.openstreetmap.org/way/1170553638), [1175506600](https://www.openstreetmap.org/way/1175506600), [1211282013](https://www.openstreetmap.org/way/1211282013), [1457950324](https://www.openstreetmap.org/way/1457950324), [1551198023](https://www.openstreetmap.org/way/1551198023)

## Aristas de entrada y salida (`is_fringe`)

|  | entradas | salidas |
|---|---:|---:|
| Total | 1237 | 1241 |
| … en vías arteriales (troncal a terciaria) | 28 | 26 |
| … en vías locales | 1209 | 1215 |

`is_fringe` marca toda arista cuyo nodo extremo no tiene otra continuación.
Eso incluye los cruces reales del límite municipal, pero también las calles
ciegas internas. Las entradas en vías arteriales son casi todas conexiones con
los municipios vecinos; las locales son mayoritariamente calles sin salida.
La demanda sintética de `python main.py prueba-tecnica` se reparte
uniformemente entre todas, así que la mayoría de esos viajes entran y salen
por calles ciegas: otra razón por la que esa demanda no representa nada.

## Advertencias de netconvert

Salida completa en `envigado_itagui_sabaneta_netconvert.log`.

| mensaje | veces |
|---|---:|
| Not joining junctions % (%). | 236 |
| Speed of % connection '%' reduced by % due to turning radius of % (length=%, angle=%). | 129 |
| Reducing junction cluster % (%). | 54 |
| Found sharp turn with radius % at the % of edge '%'. | 35 |
| Intersecting left turns at junction '%' from lane '%' and lane '%' (increase junction radius to avoid this). | 35 |
| Value of key % is not numeric (%) in edge %. | 19 |
| Ambiguity in turnarounds computation at junction '%'. | 17 |
| Cannot apply turn sign information for edge '%' because there are % signed directions but only % targets | 11 |
| Replacing loaded roundabout '%' with '%'. | 11 |
| Ignoring turn sign information for % lanes on edge % with % driving lanes | 8 |
| Discarding unknown compound '%' in type '%' (first occurrence for edge '%'). | 8 |
| Found angle of % degrees at edge '%', segment %. | 8 |
| Removed a road without junctions: %. | 7 |
| Discarding unknown compound % in type % (first occurrence for edge %). | 5 |
| No way found for reference % in relation % | 5 |

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
