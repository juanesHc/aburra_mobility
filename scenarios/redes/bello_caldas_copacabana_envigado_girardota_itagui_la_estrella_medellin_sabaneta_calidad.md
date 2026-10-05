# Calidad de la red vial — Bello + Caldas + Copacabana + Envigado + Girardota + Itagüí + La Estrella + Medellín + Sabaneta

Generado automáticamente por `python main.py construir-red`. No editar a mano:
se sobrescribe en cada corrida.

- Fuente: OpenStreetMap.
  - Bello: relación 1307262 (DIVIPOLA 05088), `bello_city.osm.xml`, datos al 2026-10-04T03:29:59Z.
  - Caldas: relación 1307283 (DIVIPOLA 05129), `caldas_city.osm.xml`, datos al 2026-10-03T16:17:36Z.
  - Copacabana: relación 1307276 (DIVIPOLA 05212), `copacabana_city.osm.xml`, datos al 2026-10-04T21:03:55Z.
  - Envigado: relación 1307277 (DIVIPOLA 05266), `envigado_city.osm.xml`, datos al 2026-09-24T16:07:09Z.
  - Girardota: relación 1307263 (DIVIPOLA 05308), `girardota_city.osm.xml`, datos al 2026-10-05T00:21:21Z.
  - Itagüí: relación 1343279 (DIVIPOLA 05360), `itagui_city.osm.xml`, datos al 2026-10-02T17:47:21Z.
  - La Estrella: relación 1307284 (DIVIPOLA 05380), `la_estrella_city.osm.xml`, datos al 2026-10-03T15:40:01Z.
  - Medellín: relación 1343264 (DIVIPOLA 05001), `medellin_city.osm.xml`, datos al 2026-10-04T02:46:04Z.
  - Sabaneta: relación 1307270 (DIVIPOLA 05631), `sabaneta_city.osm.xml`, datos al 2026-09-24T02:33:48Z.
- Red: `bello_caldas_copacabana_envigado_girardota_itagui_la_estrella_medellin_sabaneta.net.xml` (podada) y `bello_caldas_copacabana_envigado_girardota_itagui_la_estrella_medellin_sabaneta_sin_podar.net.xml` (antes de podar).
- Tolerancia de unión de intersecciones: 15 m. `tls.guess`: desactivado.

## Resumen

|  | valor |
|---|---:|
| Nodos (intersecciones y extremos) | 31046 |
| Aristas (un sentido cada una) | 70610 |
| Longitud total por sentido | 7669.3 km |
| Carril-km | 8736.0 |
| Semáforos (controladores) | 761 |
| Advertencias al cargar en sumo | 0 |

Los kilómetros se cuentan por sentido: una vía de doble sentido aporta dos veces
su longitud. Es la medida que importa para capacidad.

## Fronteras entre municipios

La red une 9 municipios convertidos juntos. Las vías que cruzan
el límite vienen en más de una descarga (213 vías OSM compartidas)
y netconvert las toma una sola vez. El núcleo es el componente fuertemente
conexo principal: desde cualquier punto del núcleo se llega a cualquier otro.
Si la frontera no conectara, uno de los municipios tendría casi nada en él.

|  | aristas | km | km en el núcleo | % en el núcleo |
|---|---:|---:|---:|---:|
| Bello | 7090 | 817.2 | 814.0 | 99.6 % |
| Caldas | 1867 | 385.5 | 381.1 | 98.9 % |
| Copacabana | 2506 | 497.8 | 460.2 | 92.4 % |
| Envigado | 5500 | 714.1 | 713.4 | 99.9 % |
| Girardota | 2034 | 570.2 | 567.9 | 99.6 % |
| Itagüí | 4188 | 290.3 | 290.2 | 100.0 % |
| La Estrella | 1710 | 224.1 | 223.8 | 99.9 % |
| Medellín | 43538 | 3788.2 | 3782.5 | 99.8 % |
| Sabaneta | 1548 | 156.4 | 156.3 | 99.9 % |
| Vías de frontera (en más de una descarga) | 629 | 225.5 | 220.8 | 97.9 % |

Los límites con municipios que no están en la red siguen cortados: sus vías
aparecen como entradas y salidas (ver la sección de bordes).

## Vías por tipo y carriles

| tipo | aristas | km | carriles/sentido (media) | carriles por defecto | velocidad por defecto |
|---|---:|---:|---:|---:|---:|
| residential | 49843 | 4035.2 | 1.05 | 36299 (77.8 % de km) | 46636 (93.7 % de km) |
| unclassified | 5219 | 1856.7 | 1.02 | 4962 (97.6 % de km) | 5119 (98.1 % de km) |
| tertiary | 8136 | 850.9 | 1.33 | 1277 (41.5 % de km) | 6121 (79.3 % de km) |
| secondary | 4032 | 443.7 | 1.71 | 317 (27.8 % de km) | 2651 (62.1 % de km) |
| trunk | 770 | 221.3 | 2.52 | 0 (0.0 % de km) | 275 (39.0 % de km) |
| primary | 1480 | 210.7 | 2.45 | 3 (0.2 % de km) | 587 (23.8 % de km) |
| trunk_link | 349 | 21.8 | 1.38 | 28 (3.5 % de km) | 278 (78.1 % de km) |
| primary_link | 396 | 15.4 | 1.55 | 12 (0.9 % de km) | 370 (91.1 % de km) |
| secondary_link | 246 | 7.8 | 1.33 | 21 (4.0 % de km) | 222 (91.1 % de km) |
| living_street | 42 | 3.3 | 1.00 | 42 (100.0 % de km) | 42 (100.0 % de km) |
| tertiary_link | 97 | 2.5 | 1.15 | 16 (32.2 % de km) | 92 (90.8 % de km) |

**42977 de 70610 aristas (70.9 % de los km) no tienen `lanes` en OSM** y netconvert les puso el valor del typemap (1 carril por sentido en secundaria, terciaria y locales; 2 en primaria y troncal). En la red arterial (troncal a terciaria) la cifra es 1674 de 15506 aristas (27.0 % de los km).

| carriles por sentido | km | % de la red |
|---|---:|---:|
| 1 | 6804.8 | 88.7 % |
| 2 | 684.6 | 8.9 % |
| 3 o más | 179.9 | 2.3 % |

Relevancia para la moto: con `lateral-resolution` 0,8 m el modelo sublane deja
que la moto se filtre entre filas en vías de dos o más carriles por sentido. En
vías de un carril solo puede adelantar dentro del mismo carril si el ancho lo
permite; OSM casi nunca trae `width`, así que los anchos de carril quedan en el valor por defecto (distribución: 3.2 m: 80918, 2.5 m: 970, 3.0 m: 158, 2.0 m: 73).
Ningún parámetro del vType `moto` se tocó.

**Calles de carril compartido: 802 aristas, 77.03 km.** Vienen de vías con `lanes=1` y doble sentido en OSM, sin `width`. netconvert las partía en dos carriles de 0.5 m, más angostos que un auto (1.8 m); se ensancharon a 2.5 m por sentido (ver supuesto `carril_compartido`). Si alguna calle resulta ser de un solo sentido o más ancha, corregirla en OSM es mejor que ajustarla aquí:

- [29874143](https://www.openstreetmap.org/way/29874143), [29875909](https://www.openstreetmap.org/way/29875909), [29880205](https://www.openstreetmap.org/way/29880205), [29881321](https://www.openstreetmap.org/way/29881321), [29881358](https://www.openstreetmap.org/way/29881358), [29881491](https://www.openstreetmap.org/way/29881491), [29978696](https://www.openstreetmap.org/way/29978696), [29978699](https://www.openstreetmap.org/way/29978699), [29998292](https://www.openstreetmap.org/way/29998292), [29999158](https://www.openstreetmap.org/way/29999158), [29999203](https://www.openstreetmap.org/way/29999203), [30002041](https://www.openstreetmap.org/way/30002041), [32526187](https://www.openstreetmap.org/way/32526187), [34580571](https://www.openstreetmap.org/way/34580571), [43117446](https://www.openstreetmap.org/way/43117446), [43517790](https://www.openstreetmap.org/way/43517790), [43518907](https://www.openstreetmap.org/way/43518907), [43519694](https://www.openstreetmap.org/way/43519694), [43519978](https://www.openstreetmap.org/way/43519978), [43520895](https://www.openstreetmap.org/way/43520895), [43570056](https://www.openstreetmap.org/way/43570056), [43570073](https://www.openstreetmap.org/way/43570073), [43616464](https://www.openstreetmap.org/way/43616464), [43686541](https://www.openstreetmap.org/way/43686541), [43947090](https://www.openstreetmap.org/way/43947090), [43947186](https://www.openstreetmap.org/way/43947186), [44935079](https://www.openstreetmap.org/way/44935079), [45416263](https://www.openstreetmap.org/way/45416263), [46303035](https://www.openstreetmap.org/way/46303035), [64886263](https://www.openstreetmap.org/way/64886263), [64948415](https://www.openstreetmap.org/way/64948415), [89062155](https://www.openstreetmap.org/way/89062155), [89062156](https://www.openstreetmap.org/way/89062156), [99760016](https://www.openstreetmap.org/way/99760016), [99871423](https://www.openstreetmap.org/way/99871423), [113978945](https://www.openstreetmap.org/way/113978945), [119183691](https://www.openstreetmap.org/way/119183691), [122290197](https://www.openstreetmap.org/way/122290197), [123755856](https://www.openstreetmap.org/way/123755856), [124008305](https://www.openstreetmap.org/way/124008305)
- … y 249 más

Tras el ajuste no queda ningún carril más angosto que un auto.

## Semáforos

|  | valor |
|---|---:|
| Nodos semáforo en OSM: `highway=traffic_signals` | 1550 |
| Nodos semáforo en OSM: solo `crossing=traffic_signals` (peatonal) | 2539 |
| Controladores en la red | 761 |
| … ubicados a partir de OSM | 761 |
| … adivinados por `tls.guess` (sin señal OSM a ≤ 35 m) | 0 |
| Cruces controlados (tras `tls.join`) | 936 |
| Señales OSM que no quedaron en ningún semáforo | 376 |
| Controladores con plan real | **0** |

Ciclos generados: mín 90 s, mediana 90 s, máx 273 s. **Todos los planes semafóricos son inventados** por netconvert (tiempos fijos genéricos). Los planes reales de Medellín los tiene el SIMM y no son públicos en formato utilizable. Esto afecta directamente la capacidad de cada intersección semaforizada.

**Señales de OSM descartadas.** `tls.discard-simple` quita los semáforos que no
están en un cruce. Conservarlos no mejora la red: recibirían un plan inventado
(82 s verde, 3 s amarillo, 5 s rojo) y alteran la agrupación de cruces vecinos;
en Sabaneta eso produjo entre 12 y 17 teleports por corrida. Su efecto real
(pasos peatonales con fase propia, control de accesos) queda sin modelar.

| señal OSM | tipo | vía | causa probable |
|---|---:|---:|---:|
| [10061788845](https://www.openstreetmap.org/node/10061788845) | vehicular | Calle 63 (tertiary) | en el cruce con una vía de servicio, que no entra a la red |
| [3661813254](https://www.openstreetmap.org/node/3661813254) | vehicular | Calle 66F (secondary) | en el cruce con una vía de servicio, que no entra a la red |
| [1664735594](https://www.openstreetmap.org/node/1664735594) | vehicular | Calle 67 (tertiary) | en el cruce con una vía de servicio, que no entra a la red |
| [3661813246](https://www.openstreetmap.org/node/3661813246) | vehicular | Calle 67 (secondary) | en el cruce con una vía de servicio, que no entra a la red |
| [3661813247](https://www.openstreetmap.org/node/3661813247) | vehicular | Calle 67 (secondary) | en el cruce con una vía de servicio, que no entra a la red |
| [3661813268](https://www.openstreetmap.org/node/3661813268) | vehicular | Calle 69 (tertiary) | en el cruce con una vía de servicio, que no entra a la red |
| [1664762039](https://www.openstreetmap.org/node/1664762039) | vehicular | Calle 71 (tertiary) | en el cruce con una vía de servicio, que no entra a la red |
| [560719971](https://www.openstreetmap.org/node/560719971) | vehicular | Calle 78 (residential) | en el cruce con una vía de servicio, que no entra a la red |
| [560719536](https://www.openstreetmap.org/node/560719536) | vehicular | Calle 80 (residential) | en el cruce con una vía de servicio, que no entra a la red |
| [3661813305](https://www.openstreetmap.org/node/3661813305) | vehicular | Calle 84 (residential) | en el cruce con una vía de servicio, que no entra a la red |
| [2548417179](https://www.openstreetmap.org/node/2548417179) | vehicular | Calle 86 (residential) | en el cruce con una vía de servicio, que no entra a la red |
| [2548417181](https://www.openstreetmap.org/node/2548417181) | vehicular | Calle 86 (residential) | en el cruce con una vía de servicio, que no entra a la red |
| [3661813322](https://www.openstreetmap.org/node/3661813322) | vehicular | Calle 88 (residential) | en el cruce con una vía de servicio, que no entra a la red |
| [3661813252](https://www.openstreetmap.org/node/3661813252) | vehicular | Carrera 45 (secondary) | en el cruce con una vía de servicio, que no entra a la red |
| [5558092753](https://www.openstreetmap.org/node/5558092753) | vehicular | Carrera 52 (secondary) | en el cruce con una vía de servicio, que no entra a la red |
| [3637211708](https://www.openstreetmap.org/node/3637211708) | peatonal | (sin nombre) (secondary_link) | paso peatonal a mitad de cuadra |
| [4384580978](https://www.openstreetmap.org/node/4384580978) | peatonal | (sin nombre) (secondary_link) | paso peatonal a mitad de cuadra |
| [5247737818](https://www.openstreetmap.org/node/5247737818) | peatonal | (sin nombre) (secondary_link) | paso peatonal a mitad de cuadra |
| [8665414950](https://www.openstreetmap.org/node/8665414950) | peatonal | (sin nombre) (primary_link) | paso peatonal a mitad de cuadra |
| [13527612726](https://www.openstreetmap.org/node/13527612726) | peatonal | (sin nombre) (primary_link) | paso peatonal a mitad de cuadra |
| [13527665121](https://www.openstreetmap.org/node/13527665121) | peatonal | (sin nombre) (primary_link) | paso peatonal a mitad de cuadra |
| [3713684708](https://www.openstreetmap.org/node/3713684708) | peatonal | Avenida 33 (primary) | paso peatonal a mitad de cuadra |
| [4386154924](https://www.openstreetmap.org/node/4386154924) | peatonal | Avenida 33 (primary) | paso peatonal a mitad de cuadra |
| [4386154925](https://www.openstreetmap.org/node/4386154925) | peatonal | Avenida 33 (primary) | paso peatonal a mitad de cuadra |
| [10292129509](https://www.openstreetmap.org/node/10292129509) | peatonal | Avenida 80 (primary) | paso peatonal a mitad de cuadra |
| [10292129510](https://www.openstreetmap.org/node/10292129510) | peatonal | Avenida 80 (primary) | paso peatonal a mitad de cuadra |
| [338510059](https://www.openstreetmap.org/node/338510059) | peatonal | Avenida Bolivariana (secondary) | paso peatonal a mitad de cuadra |
| [9915898324](https://www.openstreetmap.org/node/9915898324) | peatonal | Avenida Bolivariana (secondary) | paso peatonal a mitad de cuadra |
| [9915898325](https://www.openstreetmap.org/node/9915898325) | peatonal | Avenida Bolivariana (secondary) | paso peatonal a mitad de cuadra |
| [4382694465](https://www.openstreetmap.org/node/4382694465) | peatonal | Avenida Carrera 42 (trunk) | paso peatonal a mitad de cuadra |
| [4382694466](https://www.openstreetmap.org/node/4382694466) | peatonal | Avenida Carrera 42 (trunk) | paso peatonal a mitad de cuadra |
| [8660931018](https://www.openstreetmap.org/node/8660931018) | peatonal | Avenida Carrera 46 (primary) | paso peatonal a mitad de cuadra |
| [8660931019](https://www.openstreetmap.org/node/8660931019) | peatonal | Avenida Carrera 46 (primary) | paso peatonal a mitad de cuadra |
| [339057390](https://www.openstreetmap.org/node/339057390) | peatonal | Avenida Carrera 57 (primary) | paso peatonal a mitad de cuadra |
| [567932575](https://www.openstreetmap.org/node/567932575) | peatonal | Avenida Las Vegas (primary) | paso peatonal a mitad de cuadra |
| [11986825860](https://www.openstreetmap.org/node/11986825860) | peatonal | Avenida Las Vegas (primary) | paso peatonal a mitad de cuadra |
| [5476158295](https://www.openstreetmap.org/node/5476158295) | peatonal | Avenida Las Vegas (primary) | paso peatonal a mitad de cuadra |
| [11986681102](https://www.openstreetmap.org/node/11986681102) | peatonal | Avenida Las Vegas (primary) | paso peatonal a mitad de cuadra |
| [11986681103](https://www.openstreetmap.org/node/11986681103) | peatonal | Avenida Las Vegas (primary) | paso peatonal a mitad de cuadra |
| [5506995808](https://www.openstreetmap.org/node/5506995808) | peatonal | Avenida San Juan (secondary) | paso peatonal a mitad de cuadra |
| [7235805069](https://www.openstreetmap.org/node/7235805069) | peatonal | Avenida San Juan (secondary) | paso peatonal a mitad de cuadra |
| [8644394470](https://www.openstreetmap.org/node/8644394470) | peatonal | Avenida San Juan (secondary) | paso peatonal a mitad de cuadra |
| [3547429896](https://www.openstreetmap.org/node/3547429896) | peatonal | Calle 10 (unclassified) | paso peatonal a mitad de cuadra |
| [4944568292](https://www.openstreetmap.org/node/4944568292) | peatonal | Calle 10 (secondary) | paso peatonal a mitad de cuadra |
| [4944568293](https://www.openstreetmap.org/node/4944568293) | peatonal | Calle 10 (secondary) | paso peatonal a mitad de cuadra |
| [10699863700](https://www.openstreetmap.org/node/10699863700) | peatonal | Calle 25 Sur (secondary) | paso peatonal a mitad de cuadra |
| [10699863702](https://www.openstreetmap.org/node/10699863702) | peatonal | Calle 25 Sur (secondary) | paso peatonal a mitad de cuadra |
| [11986825817](https://www.openstreetmap.org/node/11986825817) | peatonal | Calle 26 Sur (residential) | paso peatonal a mitad de cuadra |
| [2671871268](https://www.openstreetmap.org/node/2671871268) | peatonal | Calle 30 (tertiary) | paso peatonal a mitad de cuadra |
| [10313189132](https://www.openstreetmap.org/node/10313189132) | peatonal | Calle 32 Sur (residential) | paso peatonal a mitad de cuadra |
| [10699845192](https://www.openstreetmap.org/node/10699845192) | peatonal | Calle 37 Sur (secondary) | paso peatonal a mitad de cuadra |
| [10724514140](https://www.openstreetmap.org/node/10724514140) | peatonal | Calle 38 Sur (secondary) | paso peatonal a mitad de cuadra |
| [10724514143](https://www.openstreetmap.org/node/10724514143) | peatonal | Calle 38 Sur (secondary) | paso peatonal a mitad de cuadra |
| [9159833180](https://www.openstreetmap.org/node/9159833180) | peatonal | Calle 42C (residential) | paso peatonal a mitad de cuadra |
| [11143846301](https://www.openstreetmap.org/node/11143846301) | peatonal | Calle 47F (tertiary) | paso peatonal a mitad de cuadra |
| [11143853705](https://www.openstreetmap.org/node/11143853705) | peatonal | Calle 47F (residential) | paso peatonal a mitad de cuadra |
| [4351304170](https://www.openstreetmap.org/node/4351304170) | peatonal | Calle 48 (residential) | paso peatonal a mitad de cuadra |
| [7282708263](https://www.openstreetmap.org/node/7282708263) | peatonal | Calle 48 (residential) | paso peatonal a mitad de cuadra |
| [8644401667](https://www.openstreetmap.org/node/8644401667) | peatonal | Calle 48 (residential) | paso peatonal a mitad de cuadra |
| [10735826602](https://www.openstreetmap.org/node/10735826602) | peatonal | Calle 49 (secondary) | paso peatonal a mitad de cuadra |
| [10735878405](https://www.openstreetmap.org/node/10735878405) | peatonal | Calle 49 (secondary) | paso peatonal a mitad de cuadra |
| [8656021496](https://www.openstreetmap.org/node/8656021496) | peatonal | Calle 50 (secondary) | paso peatonal a mitad de cuadra |
| [8656021497](https://www.openstreetmap.org/node/8656021497) | peatonal | Calle 50 (secondary) | paso peatonal a mitad de cuadra |
| [10311382905](https://www.openstreetmap.org/node/10311382905) | peatonal | Calle 50 (secondary) | paso peatonal a mitad de cuadra |
| [10311382908](https://www.openstreetmap.org/node/10311382908) | peatonal | Calle 50 (secondary) | paso peatonal a mitad de cuadra |
| [7204279970](https://www.openstreetmap.org/node/7204279970) | peatonal | Calle 52 Sur (residential) | paso peatonal a mitad de cuadra |
| [8665635457](https://www.openstreetmap.org/node/8665635457) | peatonal | Calle 56 (secondary) | paso peatonal a mitad de cuadra |
| [13534276977](https://www.openstreetmap.org/node/13534276977) | peatonal | Calle 56 (residential) | paso peatonal a mitad de cuadra |
| [5496791122](https://www.openstreetmap.org/node/5496791122) | peatonal | Calle 58 (tertiary) | paso peatonal a mitad de cuadra |
| [10737258848](https://www.openstreetmap.org/node/10737258848) | peatonal | Calle 65 (secondary) | paso peatonal a mitad de cuadra |
| [3661813258](https://www.openstreetmap.org/node/3661813258) | peatonal | Calle 66F (secondary) | paso peatonal a mitad de cuadra |
| [8666664966](https://www.openstreetmap.org/node/8666664966) | peatonal | Calle 67 (secondary) | paso peatonal a mitad de cuadra |
| [8666664975](https://www.openstreetmap.org/node/8666664975) | peatonal | Calle 67 (secondary) | paso peatonal a mitad de cuadra |
| [13585719786](https://www.openstreetmap.org/node/13585719786) | peatonal | Calle 67 (secondary) | paso peatonal a mitad de cuadra |
| [13585719787](https://www.openstreetmap.org/node/13585719787) | peatonal | Calle 67 (secondary) | paso peatonal a mitad de cuadra |
| [13585719788](https://www.openstreetmap.org/node/13585719788) | peatonal | Calle 67 (secondary) | paso peatonal a mitad de cuadra |
| [13585719789](https://www.openstreetmap.org/node/13585719789) | peatonal | Calle 67 (secondary) | paso peatonal a mitad de cuadra |
| [11986681088](https://www.openstreetmap.org/node/11986681088) | peatonal | Calle 68 Sur (tertiary) | paso peatonal a mitad de cuadra |
| [8666732087](https://www.openstreetmap.org/node/8666732087) | peatonal | Calle 69 (tertiary) | paso peatonal a mitad de cuadra |
| [8666732088](https://www.openstreetmap.org/node/8666732088) | peatonal | Calle 69 (tertiary) | paso peatonal a mitad de cuadra |
| [10557729213](https://www.openstreetmap.org/node/10557729213) | peatonal | Calle 76 (tertiary) | paso peatonal a mitad de cuadra |
| [8666745841](https://www.openstreetmap.org/node/8666745841) | peatonal | Calle 78 (residential) | paso peatonal a mitad de cuadra |
| [8666745848](https://www.openstreetmap.org/node/8666745848) | peatonal | Calle 78 (residential) | paso peatonal a mitad de cuadra |
| [10557707897](https://www.openstreetmap.org/node/10557707897) | peatonal | Calle 80 (residential) | paso peatonal a mitad de cuadra |
| [8668750343](https://www.openstreetmap.org/node/8668750343) | peatonal | Calle 80 (residential) | paso peatonal a mitad de cuadra |
| [8668750344](https://www.openstreetmap.org/node/8668750344) | peatonal | Calle 80 (residential) | paso peatonal a mitad de cuadra |
| [8668750333](https://www.openstreetmap.org/node/8668750333) | peatonal | Calle 84 (residential) | paso peatonal a mitad de cuadra |
| [8668750336](https://www.openstreetmap.org/node/8668750336) | peatonal | Calle 84 (residential) | paso peatonal a mitad de cuadra |
| [8668750364](https://www.openstreetmap.org/node/8668750364) | peatonal | Calle 86 (residential) | paso peatonal a mitad de cuadra |
| [8668750365](https://www.openstreetmap.org/node/8668750365) | peatonal | Calle 86 (residential) | paso peatonal a mitad de cuadra |
| [8668750379](https://www.openstreetmap.org/node/8668750379) | peatonal | Calle 88 (residential) | paso peatonal a mitad de cuadra |
| [8668750382](https://www.openstreetmap.org/node/8668750382) | peatonal | Calle 88 (residential) | paso peatonal a mitad de cuadra |
| [8668754883](https://www.openstreetmap.org/node/8668754883) | peatonal | Calle 93 (residential) | paso peatonal a mitad de cuadra |
| [13122957748](https://www.openstreetmap.org/node/13122957748) | peatonal | Carrera 100 (residential) | paso peatonal a mitad de cuadra |
| [8656021431](https://www.openstreetmap.org/node/8656021431) | peatonal | Carrera 31 (residential) | paso peatonal a mitad de cuadra |
| [8656021433](https://www.openstreetmap.org/node/8656021433) | peatonal | Carrera 31 (residential) | paso peatonal a mitad de cuadra |
| [8656024131](https://www.openstreetmap.org/node/8656024131) | peatonal | Carrera 31 (residential) | paso peatonal a mitad de cuadra |
| [8647959799](https://www.openstreetmap.org/node/8647959799) | peatonal | Carrera 32 (residential) | paso peatonal a mitad de cuadra |
| [8647959800](https://www.openstreetmap.org/node/8647959800) | peatonal | Carrera 32 (residential) | paso peatonal a mitad de cuadra |
| [8647924397](https://www.openstreetmap.org/node/8647924397) | peatonal | Carrera 39 (secondary) | paso peatonal a mitad de cuadra |
| [8647924399](https://www.openstreetmap.org/node/8647924399) | peatonal | Carrera 39 (secondary) | paso peatonal a mitad de cuadra |
| [8647924351](https://www.openstreetmap.org/node/8647924351) | peatonal | Carrera 40 (tertiary) | paso peatonal a mitad de cuadra |
| [8647924400](https://www.openstreetmap.org/node/8647924400) | peatonal | Carrera 40 (tertiary) | paso peatonal a mitad de cuadra |
| [4351304133](https://www.openstreetmap.org/node/4351304133) | peatonal | Carrera 43 (secondary) | paso peatonal a mitad de cuadra |
| [8644401741](https://www.openstreetmap.org/node/8644401741) | peatonal | Carrera 43 (secondary) | paso peatonal a mitad de cuadra |
| [8644401748](https://www.openstreetmap.org/node/8644401748) | peatonal | Carrera 43 (secondary) | paso peatonal a mitad de cuadra |
| [5927555379](https://www.openstreetmap.org/node/5927555379) | peatonal | Carrera 43A (primary) | paso peatonal a mitad de cuadra |
| [9395455241](https://www.openstreetmap.org/node/9395455241) | peatonal | Carrera 43A (primary) | paso peatonal a mitad de cuadra |
| [10312139802](https://www.openstreetmap.org/node/10312139802) | peatonal | Carrera 43A (primary) | paso peatonal a mitad de cuadra |
| [10312139803](https://www.openstreetmap.org/node/10312139803) | peatonal | Carrera 43A (primary) | paso peatonal a mitad de cuadra |
| [11935708025](https://www.openstreetmap.org/node/11935708025) | peatonal | Carrera 43A (secondary) | paso peatonal a mitad de cuadra |
| [5549142897](https://www.openstreetmap.org/node/5549142897) | peatonal | Carrera 44 (tertiary) | paso peatonal a mitad de cuadra |
| [8644401718](https://www.openstreetmap.org/node/8644401718) | peatonal | Carrera 45 (tertiary) | paso peatonal a mitad de cuadra |
| [8644401740](https://www.openstreetmap.org/node/8644401740) | peatonal | Carrera 45 (tertiary) | paso peatonal a mitad de cuadra |
| [11151956271](https://www.openstreetmap.org/node/11151956271) | peatonal | Carrera 45 (tertiary) | paso peatonal a mitad de cuadra |
| [11151956273](https://www.openstreetmap.org/node/11151956273) | peatonal | Carrera 45 (tertiary) | paso peatonal a mitad de cuadra |
| [4351304289](https://www.openstreetmap.org/node/4351304289) | peatonal | Carrera 46 (primary) | paso peatonal a mitad de cuadra |
| [4351304292](https://www.openstreetmap.org/node/4351304292) | peatonal | Carrera 46 (primary) | paso peatonal a mitad de cuadra |
| [8668754885](https://www.openstreetmap.org/node/8668754885) | peatonal | Carrera 49A (residential) | paso peatonal a mitad de cuadra |
| [11988049397](https://www.openstreetmap.org/node/11988049397) | peatonal | Carrera 50FF (residential) | paso peatonal a mitad de cuadra |
| [13623965632](https://www.openstreetmap.org/node/13623965632) | peatonal | Carrera 51 (tertiary) | paso peatonal a mitad de cuadra |
| [13623965633](https://www.openstreetmap.org/node/13623965633) | peatonal | Carrera 51 (tertiary) | paso peatonal a mitad de cuadra |
| [13623965671](https://www.openstreetmap.org/node/13623965671) | peatonal | Carrera 51 (secondary) | paso peatonal a mitad de cuadra |
| [13623965676](https://www.openstreetmap.org/node/13623965676) | peatonal | Carrera 51 (secondary) | paso peatonal a mitad de cuadra |
| [3781303990](https://www.openstreetmap.org/node/3781303990) | peatonal | Carrera 52 (primary) | paso peatonal a mitad de cuadra |
| [5475641779](https://www.openstreetmap.org/node/5475641779) | peatonal | Carrera 52 (tertiary) | paso peatonal a mitad de cuadra |
| [5475641780](https://www.openstreetmap.org/node/5475641780) | peatonal | Carrera 52 (primary) | paso peatonal a mitad de cuadra |
| [5475641781](https://www.openstreetmap.org/node/5475641781) | peatonal | Carrera 52 (primary) | paso peatonal a mitad de cuadra |
| [5475641782](https://www.openstreetmap.org/node/5475641782) | peatonal | Carrera 52 (tertiary) | paso peatonal a mitad de cuadra |
| [5475641793](https://www.openstreetmap.org/node/5475641793) | peatonal | Carrera 52 (tertiary) | paso peatonal a mitad de cuadra |
| [5475641794](https://www.openstreetmap.org/node/5475641794) | peatonal | Carrera 52 (primary) | paso peatonal a mitad de cuadra |
| [5475641795](https://www.openstreetmap.org/node/5475641795) | peatonal | Carrera 52 (primary) | paso peatonal a mitad de cuadra |
| [5475641796](https://www.openstreetmap.org/node/5475641796) | peatonal | Carrera 52 (tertiary) | paso peatonal a mitad de cuadra |
| [5495155197](https://www.openstreetmap.org/node/5495155197) | peatonal | Carrera 52 (primary) | paso peatonal a mitad de cuadra |
| [10557707907](https://www.openstreetmap.org/node/10557707907) | peatonal | Carrera 52D (primary) | paso peatonal a mitad de cuadra |
| [8576987772](https://www.openstreetmap.org/node/8576987772) | peatonal | Carrera 55 (tertiary) | paso peatonal a mitad de cuadra |
| [13563351451](https://www.openstreetmap.org/node/13563351451) | peatonal | Carrera 55 (secondary) | paso peatonal a mitad de cuadra |
| [13534276935](https://www.openstreetmap.org/node/13534276935) | peatonal | Carrera 56 (tertiary) | paso peatonal a mitad de cuadra |
| [13585772922](https://www.openstreetmap.org/node/13585772922) | peatonal | Carrera 56 (residential) | paso peatonal a mitad de cuadra |
| [13536913095](https://www.openstreetmap.org/node/13536913095) | peatonal | Carrera 57 (tertiary) | paso peatonal a mitad de cuadra |
| [10691239513](https://www.openstreetmap.org/node/10691239513) | peatonal | Carrera 59 (secondary) | paso peatonal a mitad de cuadra |
| [8576987806](https://www.openstreetmap.org/node/8576987806) | peatonal | Carrera 62 (tertiary) | paso peatonal a mitad de cuadra |
| [8751449570](https://www.openstreetmap.org/node/8751449570) | peatonal | Carrera 64C (tertiary) | paso peatonal a mitad de cuadra |
| [429901289](https://www.openstreetmap.org/node/429901289) | peatonal | Carrera 65 (secondary) | paso peatonal a mitad de cuadra |
| [430508388](https://www.openstreetmap.org/node/430508388) | peatonal | Carrera 65 (secondary) | paso peatonal a mitad de cuadra |
| [806754869](https://www.openstreetmap.org/node/806754869) | peatonal | Carrera 65 (secondary) | paso peatonal a mitad de cuadra |
| [3312970236](https://www.openstreetmap.org/node/3312970236) | peatonal | Carrera 65 (secondary) | paso peatonal a mitad de cuadra |
| [5549356969](https://www.openstreetmap.org/node/5549356969) | peatonal | Carrera 65 (secondary) | paso peatonal a mitad de cuadra |
| [6603442655](https://www.openstreetmap.org/node/6603442655) | peatonal | Carrera 65 (secondary) | paso peatonal a mitad de cuadra |
| [10726831805](https://www.openstreetmap.org/node/10726831805) | peatonal | Carrera 65 (tertiary) | paso peatonal a mitad de cuadra |
| [10726831806](https://www.openstreetmap.org/node/10726831806) | peatonal | Carrera 65 (tertiary) | paso peatonal a mitad de cuadra |
| [11137391311](https://www.openstreetmap.org/node/11137391311) | peatonal | Carrera 65 (secondary) | paso peatonal a mitad de cuadra |
| [13485110059](https://www.openstreetmap.org/node/13485110059) | peatonal | Carrera 65 (secondary) | paso peatonal a mitad de cuadra |
| [9915898326](https://www.openstreetmap.org/node/9915898326) | peatonal | Carrera 66B (residential) | paso peatonal a mitad de cuadra |
| [5529647682](https://www.openstreetmap.org/node/5529647682) | peatonal | Carrera 69A (residential) | paso peatonal a mitad de cuadra |
| [13944123770](https://www.openstreetmap.org/node/13944123770) | peatonal | Carrera 69B (tertiary) | paso peatonal a mitad de cuadra |
| [9846653117](https://www.openstreetmap.org/node/9846653117) | peatonal | Carrera 78 (tertiary) | paso peatonal a mitad de cuadra |
| [11143846295](https://www.openstreetmap.org/node/11143846295) | peatonal | Carrera 87 (tertiary) | paso peatonal a mitad de cuadra |
| [10699845190](https://www.openstreetmap.org/node/10699845190) | peatonal | Diagonal 31 (secondary) | paso peatonal a mitad de cuadra |
| [12164646632](https://www.openstreetmap.org/node/12164646632) | vehicular | (sin nombre) (tertiary) | semáforo vehicular a mitad de vía |
| [348408723](https://www.openstreetmap.org/node/348408723) | vehicular | (sin nombre) (primary_link) | semáforo vehicular a mitad de vía |
| [366633944](https://www.openstreetmap.org/node/366633944) | vehicular | (sin nombre) (primary_link) | semáforo vehicular a mitad de vía |
| [4061457532](https://www.openstreetmap.org/node/4061457532) | vehicular | (sin nombre) (primary_link) | semáforo vehicular a mitad de vía |
| [5495155157](https://www.openstreetmap.org/node/5495155157) | vehicular | (sin nombre) (primary_link) | semáforo vehicular a mitad de vía |
| [5553024665](https://www.openstreetmap.org/node/5553024665) | vehicular | (sin nombre) (primary_link) | semáforo vehicular a mitad de vía |
| [5553024669](https://www.openstreetmap.org/node/5553024669) | vehicular | (sin nombre) (secondary_link) | semáforo vehicular a mitad de vía |
| [8243620020](https://www.openstreetmap.org/node/8243620020) | vehicular | (sin nombre) (trunk_link) | semáforo vehicular a mitad de vía |
| [8243620022](https://www.openstreetmap.org/node/8243620022) | vehicular | (sin nombre) (trunk_link) | semáforo vehicular a mitad de vía |
| [8669024863](https://www.openstreetmap.org/node/8669024863) | vehicular | (sin nombre) (primary_link) | semáforo vehicular a mitad de vía |
| [10557799391](https://www.openstreetmap.org/node/10557799391) | vehicular | (sin nombre) (primary_link) | semáforo vehicular a mitad de vía |
| [13644498933](https://www.openstreetmap.org/node/13644498933) | vehicular | (sin nombre) (trunk_link) | semáforo vehicular a mitad de vía |
| [5758402008](https://www.openstreetmap.org/node/5758402008) | vehicular | Autopista Norte (primary) | semáforo vehicular a mitad de vía |
| [5758402009](https://www.openstreetmap.org/node/5758402009) | vehicular | Autopista Norte (primary) | semáforo vehicular a mitad de vía |
| [4061457528](https://www.openstreetmap.org/node/4061457528) | vehicular | Avenida 33 (primary) | semáforo vehicular a mitad de vía |
| [4061457531](https://www.openstreetmap.org/node/4061457531) | vehicular | Avenida 33 (primary) | semáforo vehicular a mitad de vía |
| [4061457534](https://www.openstreetmap.org/node/4061457534) | vehicular | Avenida 33 (primary) | semáforo vehicular a mitad de vía |
| [4061457537](https://www.openstreetmap.org/node/4061457537) | vehicular | Avenida 33 (primary) | semáforo vehicular a mitad de vía |
| [8751625090](https://www.openstreetmap.org/node/8751625090) | vehicular | Avenida 33 (primary) | semáforo vehicular a mitad de vía |
| [8751625091](https://www.openstreetmap.org/node/8751625091) | vehicular | Avenida 33 (primary) | semáforo vehicular a mitad de vía |
| [344805835](https://www.openstreetmap.org/node/344805835) | vehicular | Avenida 80 (primary) | semáforo vehicular a mitad de vía |
| [344805986](https://www.openstreetmap.org/node/344805986) | vehicular | Avenida 80 (primary) | semáforo vehicular a mitad de vía |
| [344806216](https://www.openstreetmap.org/node/344806216) | vehicular | Avenida 80 (primary) | semáforo vehicular a mitad de vía |
| [344807941](https://www.openstreetmap.org/node/344807941) | vehicular | Avenida 80 (primary) | semáforo vehicular a mitad de vía |
| [548590105](https://www.openstreetmap.org/node/548590105) | vehicular | Avenida 80 (primary) | semáforo vehicular a mitad de vía |
| [3687875533](https://www.openstreetmap.org/node/3687875533) | vehicular | Avenida 80 (primary) | semáforo vehicular a mitad de vía |
| [3706967528](https://www.openstreetmap.org/node/3706967528) | vehicular | Avenida 80 (primary) | semáforo vehicular a mitad de vía |
| [3729592833](https://www.openstreetmap.org/node/3729592833) | vehicular | Avenida 80 (primary) | semáforo vehicular a mitad de vía |
| [5541034013](https://www.openstreetmap.org/node/5541034013) | vehicular | Avenida 80 (primary) | semáforo vehicular a mitad de vía |
| [5541034014](https://www.openstreetmap.org/node/5541034014) | vehicular | Avenida 80 (primary) | semáforo vehicular a mitad de vía |
| [9407866951](https://www.openstreetmap.org/node/9407866951) | vehicular | Avenida 80 (primary) | semáforo vehicular a mitad de vía |
| [10291849905](https://www.openstreetmap.org/node/10291849905) | vehicular | Avenida 80 (primary) | semáforo vehicular a mitad de vía |
| [4075244933](https://www.openstreetmap.org/node/4075244933) | vehicular | Avenida Bolivariana (secondary) | semáforo vehicular a mitad de vía |
| [4075244939](https://www.openstreetmap.org/node/4075244939) | vehicular | Avenida Bolivariana (secondary) | semáforo vehicular a mitad de vía |
| [4075244956](https://www.openstreetmap.org/node/4075244956) | vehicular | Avenida Bolivariana (secondary) | semáforo vehicular a mitad de vía |
| [4075244957](https://www.openstreetmap.org/node/4075244957) | vehicular | Avenida Bolivariana (secondary) | semáforo vehicular a mitad de vía |
| [13145941239](https://www.openstreetmap.org/node/13145941239) | vehicular | Avenida Calle 37 (primary) | semáforo vehicular a mitad de vía |
| [5506997225](https://www.openstreetmap.org/node/5506997225) | vehicular | Avenida Carrera 55 (primary) | semáforo vehicular a mitad de vía |
| [343276886](https://www.openstreetmap.org/node/343276886) | vehicular | Avenida Industriales (primary) | semáforo vehicular a mitad de vía |
| [5529378869](https://www.openstreetmap.org/node/5529378869) | vehicular | Avenida Industriales (primary) | semáforo vehicular a mitad de vía |
| [5529378870](https://www.openstreetmap.org/node/5529378870) | vehicular | Avenida Industriales (primary) | semáforo vehicular a mitad de vía |
| [5529378882](https://www.openstreetmap.org/node/5529378882) | vehicular | Avenida Industriales (primary) | semáforo vehicular a mitad de vía |
| [5529378883](https://www.openstreetmap.org/node/5529378883) | vehicular | Avenida Industriales (primary) | semáforo vehicular a mitad de vía |
| [8669024862](https://www.openstreetmap.org/node/8669024862) | vehicular | Avenida Industriales (primary) | semáforo vehicular a mitad de vía |
| [9411152884](https://www.openstreetmap.org/node/9411152884) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [9411152885](https://www.openstreetmap.org/node/9411152885) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [10331108517](https://www.openstreetmap.org/node/10331108517) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [10331108518](https://www.openstreetmap.org/node/10331108518) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [339269241](https://www.openstreetmap.org/node/339269241) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [5408098633](https://www.openstreetmap.org/node/5408098633) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [5530930969](https://www.openstreetmap.org/node/5530930969) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [5530930970](https://www.openstreetmap.org/node/5530930970) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [5530930974](https://www.openstreetmap.org/node/5530930974) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [6983560951](https://www.openstreetmap.org/node/6983560951) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [4065415184](https://www.openstreetmap.org/node/4065415184) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [5476158279](https://www.openstreetmap.org/node/5476158279) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [339057036](https://www.openstreetmap.org/node/339057036) | vehicular | Avenida San Juan (secondary) | semáforo vehicular a mitad de vía |
| [3302672451](https://www.openstreetmap.org/node/3302672451) | vehicular | Avenida San Juan (secondary) | semáforo vehicular a mitad de vía |
| [5506997256](https://www.openstreetmap.org/node/5506997256) | vehicular | Avenida San Juan (secondary) | semáforo vehicular a mitad de vía |
| [8665404310](https://www.openstreetmap.org/node/8665404310) | vehicular | Avenida San Juan (secondary) | semáforo vehicular a mitad de vía |
| [10554749102](https://www.openstreetmap.org/node/10554749102) | vehicular | Avenida San Juan (secondary) | semáforo vehicular a mitad de vía |
| [329581215](https://www.openstreetmap.org/node/329581215) | vehicular | Calle 1 Sur (tertiary) | semáforo vehicular a mitad de vía |
| [5483179201](https://www.openstreetmap.org/node/5483179201) | vehicular | Calle 1 Sur (tertiary) | semáforo vehicular a mitad de vía |
| [5483179212](https://www.openstreetmap.org/node/5483179212) | vehicular | Calle 1 Sur (tertiary) | semáforo vehicular a mitad de vía |
| [5483179213](https://www.openstreetmap.org/node/5483179213) | vehicular | Calle 1 Sur (tertiary) | semáforo vehicular a mitad de vía |
| [3693492445](https://www.openstreetmap.org/node/3693492445) | vehicular | Calle 29 (secondary) | semáforo vehicular a mitad de vía |
| [3693492446](https://www.openstreetmap.org/node/3693492446) | vehicular | Calle 29 (secondary) | semáforo vehicular a mitad de vía |
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
| [8243620021](https://www.openstreetmap.org/node/8243620021) | vehicular | Calle 4 Sur (residential) | semáforo vehicular a mitad de vía |
| [5548848797](https://www.openstreetmap.org/node/5548848797) | vehicular | Calle 44 (secondary) | semáforo vehicular a mitad de vía |
| [315063962](https://www.openstreetmap.org/node/315063962) | vehicular | Calle 49 (secondary) | semáforo vehicular a mitad de vía |
| [10740094222](https://www.openstreetmap.org/node/10740094222) | vehicular | Calle 49 (secondary) | semáforo vehicular a mitad de vía |
| [309857489](https://www.openstreetmap.org/node/309857489) | vehicular | Calle 50 (secondary) | semáforo vehicular a mitad de vía |
| [9854564225](https://www.openstreetmap.org/node/9854564225) | vehicular | Calle 50 (secondary) | semáforo vehicular a mitad de vía |
| [9854564226](https://www.openstreetmap.org/node/9854564226) | vehicular | Calle 50 (secondary) | semáforo vehicular a mitad de vía |
| [358027263](https://www.openstreetmap.org/node/358027263) | vehicular | Calle 53 (tertiary) | semáforo vehicular a mitad de vía |
| [3265941179](https://www.openstreetmap.org/node/3265941179) | vehicular | Calle 62D (secondary) | semáforo vehicular a mitad de vía |
| [3265941477](https://www.openstreetmap.org/node/3265941477) | vehicular | Calle 65 (secondary) | semáforo vehicular a mitad de vía |
| [5351252063](https://www.openstreetmap.org/node/5351252063) | vehicular | Calle 65 (secondary) | semáforo vehicular a mitad de vía |
| [11139315724](https://www.openstreetmap.org/node/11139315724) | vehicular | Calle 65 (secondary) | semáforo vehicular a mitad de vía |
| [401420245](https://www.openstreetmap.org/node/401420245) | vehicular | Calle 7 Sur (secondary) | semáforo vehicular a mitad de vía |
| [3602300445](https://www.openstreetmap.org/node/3602300445) | vehicular | Calle 7 Sur (secondary) | semáforo vehicular a mitad de vía |
| [429901857](https://www.openstreetmap.org/node/429901857) | vehicular | Calle 71 (secondary) | semáforo vehicular a mitad de vía |
| [4386260132](https://www.openstreetmap.org/node/4386260132) | vehicular | Calle 71 (secondary) | semáforo vehicular a mitad de vía |
| [4100631378](https://www.openstreetmap.org/node/4100631378) | vehicular | Carrera 16A (tertiary) | semáforo vehicular a mitad de vía |
| [4100631384](https://www.openstreetmap.org/node/4100631384) | vehicular | Carrera 16A (tertiary) | semáforo vehicular a mitad de vía |
| [13674463953](https://www.openstreetmap.org/node/13674463953) | vehicular | Carrera 16A (tertiary) | semáforo vehicular a mitad de vía |
| [608732779](https://www.openstreetmap.org/node/608732779) | vehicular | Carrera 31 (residential) | semáforo vehicular a mitad de vía |
| [5756412244](https://www.openstreetmap.org/node/5756412244) | vehicular | Carrera 31 (residential) | semáforo vehicular a mitad de vía |
| [4100631296](https://www.openstreetmap.org/node/4100631296) | vehicular | Carrera 32 (residential) | semáforo vehicular a mitad de vía |
| [5756412245](https://www.openstreetmap.org/node/5756412245) | vehicular | Carrera 32 (residential) | semáforo vehicular a mitad de vía |
| [4100629977](https://www.openstreetmap.org/node/4100629977) | vehicular | Carrera 40 (tertiary) | semáforo vehicular a mitad de vía |
| [4100629981](https://www.openstreetmap.org/node/4100629981) | vehicular | Carrera 40 (tertiary) | semáforo vehicular a mitad de vía |
| [330615052](https://www.openstreetmap.org/node/330615052) | vehicular | Carrera 43 (secondary) | semáforo vehicular a mitad de vía |
| [9854564255](https://www.openstreetmap.org/node/9854564255) | vehicular | Carrera 43 (secondary) | semáforo vehicular a mitad de vía |
| [1193707831](https://www.openstreetmap.org/node/1193707831) | vehicular | Carrera 43A (primary) | semáforo vehicular a mitad de vía |
| [3501089903](https://www.openstreetmap.org/node/3501089903) | vehicular | Carrera 43A (primary) | semáforo vehicular a mitad de vía |
| [10313189070](https://www.openstreetmap.org/node/10313189070) | vehicular | Carrera 43A (primary) | semáforo vehicular a mitad de vía |
| [10313189071](https://www.openstreetmap.org/node/10313189071) | vehicular | Carrera 43A (primary) | semáforo vehicular a mitad de vía |
| [394216483](https://www.openstreetmap.org/node/394216483) | vehicular | Carrera 43A (primary) | semáforo vehicular a mitad de vía |
| [1077838526](https://www.openstreetmap.org/node/1077838526) | vehicular | Carrera 43A (primary) | semáforo vehicular a mitad de vía |
| [1469634095](https://www.openstreetmap.org/node/1469634095) | vehicular | Carrera 43A (primary) | semáforo vehicular a mitad de vía |
| [5494665023](https://www.openstreetmap.org/node/5494665023) | vehicular | Carrera 43A (primary) | semáforo vehicular a mitad de vía |
| [5531200244](https://www.openstreetmap.org/node/5531200244) | vehicular | Carrera 43A (primary) | semáforo vehicular a mitad de vía |
| [5531200245](https://www.openstreetmap.org/node/5531200245) | vehicular | Carrera 43A (primary) | semáforo vehicular a mitad de vía |
| [5531200249](https://www.openstreetmap.org/node/5531200249) | vehicular | Carrera 43A (primary) | semáforo vehicular a mitad de vía |
| [5531200250](https://www.openstreetmap.org/node/5531200250) | vehicular | Carrera 43A (primary) | semáforo vehicular a mitad de vía |
| [9397843134](https://www.openstreetmap.org/node/9397843134) | vehicular | Carrera 43A (primary) | semáforo vehicular a mitad de vía |
| [9397843135](https://www.openstreetmap.org/node/9397843135) | vehicular | Carrera 43A (primary) | semáforo vehicular a mitad de vía |
| [11943800084](https://www.openstreetmap.org/node/11943800084) | vehicular | Carrera 43A (secondary) | semáforo vehicular a mitad de vía |
| [13070224788](https://www.openstreetmap.org/node/13070224788) | vehicular | Carrera 43A (secondary) | semáforo vehicular a mitad de vía |
| [7029925200](https://www.openstreetmap.org/node/7029925200) | vehicular | Carrera 43B (secondary) | semáforo vehicular a mitad de vía |
| [7029925201](https://www.openstreetmap.org/node/7029925201) | vehicular | Carrera 43B (secondary) | semáforo vehicular a mitad de vía |
| [9943516217](https://www.openstreetmap.org/node/9943516217) | vehicular | Carrera 43C (secondary) | semáforo vehicular a mitad de vía |
| [9943516218](https://www.openstreetmap.org/node/9943516218) | vehicular | Carrera 43C (secondary) | semáforo vehicular a mitad de vía |
| [4100629952](https://www.openstreetmap.org/node/4100629952) | vehicular | Carrera 45 (tertiary) | semáforo vehicular a mitad de vía |
| [4100629954](https://www.openstreetmap.org/node/4100629954) | vehicular | Carrera 45 (tertiary) | semáforo vehicular a mitad de vía |
| [5497069516](https://www.openstreetmap.org/node/5497069516) | vehicular | Carrera 45 (tertiary) | semáforo vehicular a mitad de vía |
| [9758160433](https://www.openstreetmap.org/node/9758160433) | vehicular | Carrera 48 (residential) | semáforo vehicular a mitad de vía |
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
| [351851828](https://www.openstreetmap.org/node/351851828) | vehicular | Carrera 52 (primary) | semáforo vehicular a mitad de vía |
| [5492433397](https://www.openstreetmap.org/node/5492433397) | vehicular | Carrera 52 (tertiary) | semáforo vehicular a mitad de vía |
| [5495155159](https://www.openstreetmap.org/node/5495155159) | vehicular | Carrera 52 (primary) | semáforo vehicular a mitad de vía |
| [5495155160](https://www.openstreetmap.org/node/5495155160) | vehicular | Carrera 52 (primary) | semáforo vehicular a mitad de vía |
| [5495155196](https://www.openstreetmap.org/node/5495155196) | vehicular | Carrera 52 (tertiary) | semáforo vehicular a mitad de vía |
| [8669309475](https://www.openstreetmap.org/node/8669309475) | vehicular | Carrera 52 (tertiary) | semáforo vehicular a mitad de vía |
| [9410534819](https://www.openstreetmap.org/node/9410534819) | vehicular | Carrera 52 (primary) | semáforo vehicular a mitad de vía |
| [9410534820](https://www.openstreetmap.org/node/9410534820) | vehicular | Carrera 52 (primary) | semáforo vehicular a mitad de vía |
| [9413884630](https://www.openstreetmap.org/node/9413884630) | vehicular | Carrera 52 (tertiary) | semáforo vehicular a mitad de vía |
| [9413884631](https://www.openstreetmap.org/node/9413884631) | vehicular | Carrera 52 (primary) | semáforo vehicular a mitad de vía |
| [9401025944](https://www.openstreetmap.org/node/9401025944) | vehicular | Carrera 52D (primary) | semáforo vehicular a mitad de vía |
| [3514626604](https://www.openstreetmap.org/node/3514626604) | vehicular | Carrera 55 (tertiary) | semáforo vehicular a mitad de vía |
| [5553024683](https://www.openstreetmap.org/node/5553024683) | vehicular | Carrera 55 (secondary) | semáforo vehicular a mitad de vía |
| [5553024686](https://www.openstreetmap.org/node/5553024686) | vehicular | Carrera 55 (secondary) | semáforo vehicular a mitad de vía |
| [12164646633](https://www.openstreetmap.org/node/12164646633) | vehicular | Carrera 55A (tertiary) | semáforo vehicular a mitad de vía |
| [543399079](https://www.openstreetmap.org/node/543399079) | vehicular | Carrera 65 (secondary) | semáforo vehicular a mitad de vía |
| [4947179617](https://www.openstreetmap.org/node/4947179617) | vehicular | Carrera 65 (secondary) | semáforo vehicular a mitad de vía |
| [5867899858](https://www.openstreetmap.org/node/5867899858) | vehicular | Carrera 65 (secondary) | semáforo vehicular a mitad de vía |
| [5867899859](https://www.openstreetmap.org/node/5867899859) | vehicular | Carrera 65 (secondary) | semáforo vehicular a mitad de vía |
| [5871232934](https://www.openstreetmap.org/node/5871232934) | vehicular | Carrera 65 (secondary) | semáforo vehicular a mitad de vía |
| [5871232935](https://www.openstreetmap.org/node/5871232935) | vehicular | Carrera 65 (secondary) | semáforo vehicular a mitad de vía |
| [4075244929](https://www.openstreetmap.org/node/4075244929) | vehicular | Carrera 66B (residential) | semáforo vehicular a mitad de vía |
| [4075244955](https://www.openstreetmap.org/node/4075244955) | vehicular | Carrera 66B (residential) | semáforo vehicular a mitad de vía |
| [6498481781](https://www.openstreetmap.org/node/6498481781) | vehicular | Carrera 69B (tertiary) | semáforo vehicular a mitad de vía |
| [5529647664](https://www.openstreetmap.org/node/5529647664) | vehicular | Carrera 70 (tertiary) | semáforo vehicular a mitad de vía |
| [8243620024](https://www.openstreetmap.org/node/8243620024) | vehicular | Carrera 70 (secondary) | semáforo vehicular a mitad de vía |
| [8997278453](https://www.openstreetmap.org/node/8997278453) | vehicular | Carrera 70 (secondary) | semáforo vehicular a mitad de vía |
| [8997278466](https://www.openstreetmap.org/node/8997278466) | vehicular | Carrera 70 (secondary) | semáforo vehicular a mitad de vía |
| [10750992777](https://www.openstreetmap.org/node/10750992777) | vehicular | Carrera 70 (secondary) | semáforo vehicular a mitad de vía |
| [5557407909](https://www.openstreetmap.org/node/5557407909) | vehicular | Carrera 72A (secondary) | semáforo vehicular a mitad de vía |
| [5557407910](https://www.openstreetmap.org/node/5557407910) | vehicular | Carrera 72A (secondary) | semáforo vehicular a mitad de vía |
| [3914296184](https://www.openstreetmap.org/node/3914296184) | vehicular | Carrera 89 (tertiary) | semáforo vehicular a mitad de vía |
| [4444033450](https://www.openstreetmap.org/node/4444033450) | vehicular | Carrera 90 (residential) | semáforo vehicular a mitad de vía |
| [7243113069](https://www.openstreetmap.org/node/7243113069) | vehicular | Transversal 51A (secondary) | semáforo vehicular a mitad de vía |
| [7209289846](https://www.openstreetmap.org/node/7209289846) | vehicular | Transversal 73 (secondary) | semáforo vehicular a mitad de vía |
| [7237645734](https://www.openstreetmap.org/node/7237645734) | vehicular | Transversal 73 (secondary) | semáforo vehicular a mitad de vía |
| [416757217](https://www.openstreetmap.org/node/416757217) | vehicular | Transversal Superior (secondary) | semáforo vehicular a mitad de vía |
| [9408056530](https://www.openstreetmap.org/node/9408056530) | vehicular | Transversal Superior (secondary) | semáforo vehicular a mitad de vía |
| [3617311445](https://www.openstreetmap.org/node/3617311445) | vehicular | (sin nombre) (primary) | sobre el anillo de una glorieta |
| [8566349426](https://www.openstreetmap.org/node/8566349426) | vehicular | (sin nombre) (primary) | sobre el anillo de una glorieta |
| [8566349459](https://www.openstreetmap.org/node/8566349459) | vehicular | (sin nombre) (primary) | sobre el anillo de una glorieta |
| [8566349466](https://www.openstreetmap.org/node/8566349466) | vehicular | (sin nombre) (primary) | sobre el anillo de una glorieta |
| [4917215691](https://www.openstreetmap.org/node/4917215691) | vehicular | (sin nombre) (service) | sobre una vía de servicio, que no entra a la red |
| [4917215695](https://www.openstreetmap.org/node/4917215695) | vehicular | (sin nombre) (service) | sobre una vía de servicio, que no entra a la red |
| [5069582525](https://www.openstreetmap.org/node/5069582525) | vehicular | (sin nombre) (service) | sobre una vía de servicio, que no entra a la red |
| [9416236191](https://www.openstreetmap.org/node/9416236191) | vehicular | (sin nombre) (service) | sobre una vía de servicio, que no entra a la red |
| [9416236196](https://www.openstreetmap.org/node/9416236196) | vehicular | (sin nombre) (service) | sobre una vía de servicio, que no entra a la red |
| [10311534639](https://www.openstreetmap.org/node/10311534639) | peatonal | (sin nombre) (service) | sobre una vía de servicio, que no entra a la red |
| [13948390354](https://www.openstreetmap.org/node/13948390354) | peatonal | (sin nombre) (service) | sobre una vía de servicio, que no entra a la red |
| [1339916397](https://www.openstreetmap.org/node/1339916397) | peatonal | Calle 50 (service) | sobre una vía de servicio, que no entra a la red |
| [1339916402](https://www.openstreetmap.org/node/1339916402) | vehicular | Carrera 49 (service) | sobre una vía de servicio, que no entra a la red |
| [5512719631](https://www.openstreetmap.org/node/5512719631) | vehicular | Carrera 49 (service) | sobre una vía de servicio, que no entra a la red |
| [3667792259](https://www.openstreetmap.org/node/3667792259) | peatonal | Metroplús (service) | sobre una vía de servicio, que no entra a la red |
| [3667792260](https://www.openstreetmap.org/node/3667792260) | peatonal | Metroplús (service) | sobre una vía de servicio, que no entra a la red |
| [8660930976](https://www.openstreetmap.org/node/8660930976) | peatonal | Metroplús (service) | sobre una vía de servicio, que no entra a la red |
| [8660930977](https://www.openstreetmap.org/node/8660930977) | peatonal | Metroplús (service) | sobre una vía de servicio, que no entra a la red |
| [8660931020](https://www.openstreetmap.org/node/8660931020) | peatonal | Metroplús (service) | sobre una vía de servicio, que no entra a la red |
| [8660931021](https://www.openstreetmap.org/node/8660931021) | peatonal | Metroplús (service) | sobre una vía de servicio, que no entra a la red |
| [8668750373](https://www.openstreetmap.org/node/8668750373) | peatonal | Metroplús (service) | sobre una vía de servicio, que no entra a la red |
| [8668750374](https://www.openstreetmap.org/node/8668750374) | peatonal | Metroplús (service) | sobre una vía de servicio, que no entra a la red |
| [11114374105](https://www.openstreetmap.org/node/11114374105) | peatonal | Metroplús (service) | sobre una vía de servicio, que no entra a la red |
| [11114374125](https://www.openstreetmap.org/node/11114374125) | peatonal | Metroplús (service) | sobre una vía de servicio, que no entra a la red |
| [11139939530](https://www.openstreetmap.org/node/11139939530) | peatonal | Metroplús (service) | sobre una vía de servicio, que no entra a la red |
| [11139939531](https://www.openstreetmap.org/node/11139939531) | peatonal | Metroplús (service) | sobre una vía de servicio, que no entra a la red |
| [11139946871](https://www.openstreetmap.org/node/11139946871) | peatonal | Metroplús (service) | sobre una vía de servicio, que no entra a la red |
| [11139946874](https://www.openstreetmap.org/node/11139946874) | peatonal | Metroplús (service) | sobre una vía de servicio, que no entra a la red |
| [11139946878](https://www.openstreetmap.org/node/11139946878) | peatonal | Metroplús (service) | sobre una vía de servicio, que no entra a la red |
| [11139946887](https://www.openstreetmap.org/node/11139946887) | peatonal | Metroplús (service) | sobre una vía de servicio, que no entra a la red |
| [11139946890](https://www.openstreetmap.org/node/11139946890) | peatonal | Metroplús (service) | sobre una vía de servicio, que no entra a la red |
| [11139946899](https://www.openstreetmap.org/node/11139946899) | peatonal | Metroplús (service) | sobre una vía de servicio, que no entra a la red |
| [11139946902](https://www.openstreetmap.org/node/11139946902) | peatonal | Metroplús (service) | sobre una vía de servicio, que no entra a la red |

**Glorietas con semáforos en el anillo: (sin nombre).** En la red funcionan como glorietas con prelación para quien va dentro, y en la realidad están semaforizadas. El plan semafórico de una glorieta no se puede adivinar: hay que construirlo a mano en netedit con los tiempos reales.

## Restricciones de giro y carriles de giro

OSM trae **994 relaciones de restricción de giro** para 19962 intersecciones con al menos dos entradas y dos salidas (5.0 por cada 100). Cualquier giro prohibido que no esté mapeado queda permitido en la simulación.

| tipo | relaciones |
|---|---:|
| no_left_turn | 538 |
| ? | 164 |
| no_right_turn | 160 |
| no_u_turn | 60 |
| only_straight_on | 47 |
| only_right_turn | 10 |
| only_left_turn | 9 |
| no_straight_on | 4 |
| only_u_turn | 2 |

netconvert ignoró 24 por referir vías que no están en la descarga o que no son para autos.

Flechas de giro por carril (`turn:lanes`) en OSM, por tipo de vía:

| tipo | vías con turn:lanes | vías del tipo |
|---|---:|---:|
| residential | 412 | 18527 |
| service | 5 | 14530 |
| tertiary | 622 | 3955 |
| secondary | 311 | 2332 |
| unclassified | 3 | 2174 |
| primary | 164 | 1212 |
| trunk | 38 | 608 |
| primary_link | 16 | 400 |
| trunk_link | 6 | 344 |
| secondary_link | 12 | 295 |
| tertiary_link | 13 | 136 |
| platform | 0 | 28 |
| living_street | 0 | 19 |

## Componentes desconectados

Calculado sobre la red **antes de podar**, con las conexiones que puede usar
un auto.

|  | valor |
|---|---:|
| Componentes débilmente conexos | 18 |
| Aristas en el mayor (débil) | 70610 (99.7 %) |
| Componentes fuertemente conexos | 181 |
| Aristas en el mayor (fuerte) | 70336 (99.4 %) |
| Componentes fuertes de más de 1 arista, aparte del mayor | 23 |
| Aristas conservadas | 70610 |
| Aristas podadas: islas (otro componente débil) | 182 |
| Aristas podadas: trampas dentro del componente principal | 0 |

Una arista se conserva si un vehículo puede recorrerla de principio a fin: porque
llega al componente fuerte principal, porque se llega a ella desde él, o porque
está entre una entrada y una salida de la red (vías de paso por el borde).
Se poda lo demás: islas sin conexión vial con el resto y trampas (tramos de
sentido único a los que no se puede llegar o que no llevan a ninguna parte).
Casi siempre son errores de sentido o de conexión en OSM.

Islas: 182 aristas, 46.01 km, en estas vías OSM. Revisar en netedit o corregir en OSM (una isla suele ser una conexión que falta en el mapa, o una vía de un tipo que no se descarga, como `track`):

- [62228930](https://www.openstreetmap.org/way/62228930), [172999668](https://www.openstreetmap.org/way/172999668), [172999670](https://www.openstreetmap.org/way/172999670), [176994955](https://www.openstreetmap.org/way/176994955), [185660054](https://www.openstreetmap.org/way/185660054), [185660625](https://www.openstreetmap.org/way/185660625), [222665941](https://www.openstreetmap.org/way/222665941), [222665944](https://www.openstreetmap.org/way/222665944), [253852289](https://www.openstreetmap.org/way/253852289), [253874849](https://www.openstreetmap.org/way/253874849), [440529002](https://www.openstreetmap.org/way/440529002), [440529006](https://www.openstreetmap.org/way/440529006), [440529009](https://www.openstreetmap.org/way/440529009), [485603895](https://www.openstreetmap.org/way/485603895), [485603896](https://www.openstreetmap.org/way/485603896), [485603897](https://www.openstreetmap.org/way/485603897), [485606800](https://www.openstreetmap.org/way/485606800), [485606801](https://www.openstreetmap.org/way/485606801), [485606802](https://www.openstreetmap.org/way/485606802), [548427461](https://www.openstreetmap.org/way/548427461), [548427462](https://www.openstreetmap.org/way/548427462), [548427463](https://www.openstreetmap.org/way/548427463), [548787965](https://www.openstreetmap.org/way/548787965), [548787966](https://www.openstreetmap.org/way/548787966), [549843249](https://www.openstreetmap.org/way/549843249), [549843250](https://www.openstreetmap.org/way/549843250), [551360222](https://www.openstreetmap.org/way/551360222), [551360230](https://www.openstreetmap.org/way/551360230), [552231576](https://www.openstreetmap.org/way/552231576), [552231577](https://www.openstreetmap.org/way/552231577), [552231578](https://www.openstreetmap.org/way/552231578), [560763516](https://www.openstreetmap.org/way/560763516), [571721526](https://www.openstreetmap.org/way/571721526), [571721527](https://www.openstreetmap.org/way/571721527), [571721530](https://www.openstreetmap.org/way/571721530), [626743027](https://www.openstreetmap.org/way/626743027), [914667947](https://www.openstreetmap.org/way/914667947), [914667948](https://www.openstreetmap.org/way/914667948), [914699849](https://www.openstreetmap.org/way/914699849), [914699850](https://www.openstreetmap.org/way/914699850), [1017763600](https://www.openstreetmap.org/way/1017763600), [1017816788](https://www.openstreetmap.org/way/1017816788), [1017816789](https://www.openstreetmap.org/way/1017816789), [1018913291](https://www.openstreetmap.org/way/1018913291), [1018913292](https://www.openstreetmap.org/way/1018913292), [1020815166](https://www.openstreetmap.org/way/1020815166), [1067543750](https://www.openstreetmap.org/way/1067543750), [1077898733](https://www.openstreetmap.org/way/1077898733), [1077904239](https://www.openstreetmap.org/way/1077904239), [1078371698](https://www.openstreetmap.org/way/1078371698), [1078371699](https://www.openstreetmap.org/way/1078371699), [1078371700](https://www.openstreetmap.org/way/1078371700), [1078371701](https://www.openstreetmap.org/way/1078371701), [1078371702](https://www.openstreetmap.org/way/1078371702), [1078378834](https://www.openstreetmap.org/way/1078378834), [1175506600](https://www.openstreetmap.org/way/1175506600), [1389963057](https://www.openstreetmap.org/way/1389963057), [1389963059](https://www.openstreetmap.org/way/1389963059), [1410572892](https://www.openstreetmap.org/way/1410572892), [1459094972](https://www.openstreetmap.org/way/1459094972)
- … y 8 más

## Aristas de entrada y salida (`is_fringe`)

|  | entradas | salidas |
|---|---:|---:|
| Total | 6494 | 6475 |
| … en vías arteriales (troncal a terciaria) | 86 | 74 |
| … en vías locales | 6408 | 6401 |

`is_fringe` marca toda arista cuyo nodo extremo no tiene otra continuación.
Eso incluye los cruces reales del límite municipal, pero también las calles
ciegas internas. Las entradas en vías arteriales son casi todas conexiones con
los municipios vecinos; las locales son mayoritariamente calles sin salida.
La demanda sintética de `python main.py prueba-tecnica` se reparte
uniformemente entre todas, así que la mayoría de esos viajes entran y salen
por calles ciegas: otra razón por la que esa demanda no representa nada.

## Advertencias de netconvert

Salida completa en `bello_caldas_copacabana_envigado_girardota_itagui_la_estrella_medellin_sabaneta_netconvert.log`.

| mensaje | veces |
|---|---:|
| Not joining junctions % (%). | 1173 |
| Speed of % connection '%' reduced by % due to turning radius of % (length=%, angle=%). | 1042 |
| Found sharp turn with radius % at the % of edge '%'. | 560 |
| Reducing junction cluster % (%). | 496 |
| Intersecting left turns at junction '%' from lane '%' and lane '%' (increase junction radius to avoid this). | 347 |
| Found angle of % degrees at edge '%', segment %. | 179 |
| Cannot apply turn sign information for edge '%' because there are % signed directions but only % targets | 176 |
| Ignoring restriction relation '%' with unknown type. | 159 |
| Removed a road without junctions: %. | 137 |
| Ambiguity in turnarounds computation at junction '%'. | 115 |
| Ignoring turn sign information for % lanes on edge % with % driving lanes | 66 |
| No way found for reference '%' in relation '%' | 61 |
| Could not find corresponding edge or compatible lane for free-floating pt stop '%' (%). Thus, it will be removed! | 59 |
| Replacing loaded roundabout '%' with '%'. | 50 |
| Cannot apply turn sign information for edge '%' because there are % signed connections with directions '%' but target edge '%' has only % suitable lanes | 41 |

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
