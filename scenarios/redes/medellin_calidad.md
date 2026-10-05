# Calidad de la red vial — Medellín

Generado automáticamente por `python main.py construir-red`. No editar a mano:
se sobrescribe en cada corrida.

- Fuente: OpenStreetMap.
  - Medellín: relación 1343264 (DIVIPOLA 05001), `medellin_city.osm.xml`, datos al 2026-10-04T02:46:04Z.
- Red: `medellin.net.xml` (podada) y `medellin_sin_podar.net.xml` (antes de podar).
- Tolerancia de unión de intersecciones: 15 m. `tls.guess`: desactivado.

## Resumen

|  | valor |
|---|---:|
| Nodos (intersecciones y extremos) | 18649 |
| Aristas (un sentido cada una) | 43802 |
| Longitud total por sentido | 3876.7 km |
| Carril-km | 4556.2 |
| Semáforos (controladores) | 544 |
| Advertencias al cargar en sumo | 0 |

Los kilómetros se cuentan por sentido: una vía de doble sentido aporta dos veces
su longitud. Es la medida que importa para capacidad.

## Vías por tipo y carriles

| tipo | aristas | km | carriles/sentido (media) | carriles por defecto | velocidad por defecto |
|---|---:|---:|---:|---:|---:|
| residential | 31090 | 2243.2 | 1.04 | 21625 (72.4 % de km) | 29094 (93.2 % de km) |
| tertiary | 6153 | 574.3 | 1.34 | 955 (36.0 % de km) | 4678 (77.3 % de km) |
| unclassified | 1778 | 519.8 | 1.02 | 1656 (96.8 % de km) | 1710 (97.1 % de km) |
| secondary | 2612 | 274.0 | 1.81 | 143 (24.0 % de km) | 1645 (67.4 % de km) |
| primary | 1018 | 136.6 | 2.53 | 0 (0.0 % de km) | 465 (28.4 % de km) |
| trunk | 324 | 92.7 | 2.64 | 0 (0.0 % de km) | 93 (33.6 % de km) |
| primary_link | 334 | 13.5 | 1.57 | 9 (0.7 % de km) | 314 (91.9 % de km) |
| trunk_link | 188 | 11.9 | 1.43 | 18 (4.8 % de km) | 153 (76.1 % de km) |
| secondary_link | 204 | 6.8 | 1.36 | 15 (2.8 % de km) | 182 (90.4 % de km) |
| living_street | 30 | 2.4 | 1.00 | 30 (100.0 % de km) | 30 (100.0 % de km) |
| tertiary_link | 71 | 1.6 | 1.18 | 11 (38.3 % de km) | 69 (96.4 % de km) |

**24462 de 43802 aristas (62.0 % de los km) no tienen `lanes` en OSM** y netconvert les puso el valor del typemap (1 carril por sentido en secundaria, terciaria y locales; 2 en primaria y troncal). En la red arterial (troncal a terciaria) la cifra es 1151 de 10904 aristas (24.7 % de los km).

| carriles por sentido | km | % de la red |
|---|---:|---:|
| 1 | 3336.0 | 86.1 % |
| 2 | 421.9 | 10.9 % |
| 3 o más | 118.8 | 3.1 % |

Relevancia para la moto: con `lateral-resolution` 0,8 m el modelo sublane deja
que la moto se filtre entre filas en vías de dos o más carriles por sentido. En
vías de un carril solo puede adelantar dentro del mismo carril si el ancho lo
permite; OSM casi nunca trae `width`, así que los anchos de carril quedan en el valor por defecto (distribución: 3.2 m: 50922, 2.5 m: 532, 3.0 m: 44, 3.5 m: 32).
Ningún parámetro del vType `moto` se tocó.

**Calles de carril compartido: 432 aristas, 37.16 km.** Vienen de vías con `lanes=1` y doble sentido en OSM, sin `width`. netconvert las partía en dos carriles de 1.0 m, más angostos que un auto (1.8 m); se ensancharon a 2.5 m por sentido (ver supuesto `carril_compartido`). Si alguna calle resulta ser de un solo sentido o más ancha, corregirla en OSM es mejor que ajustarla aquí:

- [32526187](https://www.openstreetmap.org/way/32526187), [34580571](https://www.openstreetmap.org/way/34580571), [43517790](https://www.openstreetmap.org/way/43517790), [43518907](https://www.openstreetmap.org/way/43518907), [43519694](https://www.openstreetmap.org/way/43519694), [43519978](https://www.openstreetmap.org/way/43519978), [43520895](https://www.openstreetmap.org/way/43520895), [43570056](https://www.openstreetmap.org/way/43570056), [43570073](https://www.openstreetmap.org/way/43570073), [43616464](https://www.openstreetmap.org/way/43616464), [43686541](https://www.openstreetmap.org/way/43686541), [43947090](https://www.openstreetmap.org/way/43947090), [43947186](https://www.openstreetmap.org/way/43947186), [44935079](https://www.openstreetmap.org/way/44935079), [45416263](https://www.openstreetmap.org/way/45416263), [46303035](https://www.openstreetmap.org/way/46303035), [64886263](https://www.openstreetmap.org/way/64886263), [64948415](https://www.openstreetmap.org/way/64948415), [99760016](https://www.openstreetmap.org/way/99760016), [99871423](https://www.openstreetmap.org/way/99871423), [113978945](https://www.openstreetmap.org/way/113978945), [122290197](https://www.openstreetmap.org/way/122290197), [123755856](https://www.openstreetmap.org/way/123755856), [124008305](https://www.openstreetmap.org/way/124008305), [129779007](https://www.openstreetmap.org/way/129779007), [131889773](https://www.openstreetmap.org/way/131889773), [152237903](https://www.openstreetmap.org/way/152237903), [173108829](https://www.openstreetmap.org/way/173108829), [173109221](https://www.openstreetmap.org/way/173109221), [173151555](https://www.openstreetmap.org/way/173151555), [211937414](https://www.openstreetmap.org/way/211937414), [211946760](https://www.openstreetmap.org/way/211946760), [229240805](https://www.openstreetmap.org/way/229240805), [230675926](https://www.openstreetmap.org/way/230675926), [264764942](https://www.openstreetmap.org/way/264764942), [265627137](https://www.openstreetmap.org/way/265627137), [265627139](https://www.openstreetmap.org/way/265627139), [265627156](https://www.openstreetmap.org/way/265627156), [265630519](https://www.openstreetmap.org/way/265630519), [265630521](https://www.openstreetmap.org/way/265630521)
- … y 112 más

Tras el ajuste no queda ningún carril más angosto que un auto.

## Semáforos

|  | valor |
|---|---:|
| Nodos semáforo en OSM: `highway=traffic_signals` | 1153 |
| Nodos semáforo en OSM: solo `crossing=traffic_signals` (peatonal) | 1911 |
| Controladores en la red | 544 |
| … ubicados a partir de OSM | 543 |
| … adivinados por `tls.guess` (sin señal OSM a ≤ 35 m) | 1 |
| Cruces controlados (tras `tls.join`) | 681 |
| Señales OSM que no quedaron en ningún semáforo | 316 |
| Controladores con plan real | **0** |

Ciclos generados: mín 90 s, mediana 90 s, máx 273 s. **Todos los planes semafóricos son inventados** por netconvert (tiempos fijos genéricos). Los planes reales de Medellín los tiene el SIMM y no son públicos en formato utilizable. Esto afecta directamente la capacidad de cada intersección semaforizada.

**Señales de OSM descartadas.** `tls.discard-simple` quita los semáforos que no
están en un cruce. Conservarlos no mejora la red: recibirían un plan inventado
(82 s verde, 3 s amarillo, 5 s rojo) y alteran la agrupación de cruces vecinos;
en Sabaneta eso produjo entre 12 y 17 teleports por corrida. Su efecto real
(pasos peatonales con fase propia, control de accesos) queda sin modelar.

| señal OSM | tipo | vía | causa probable |
|---|---:|---:|---:|
| [1834684816](https://www.openstreetmap.org/node/1834684816) | vehicular | (sin nombre) (residential) | en el extremo de una vía (borde de la red o calle ciega) |
| [11988049441](https://www.openstreetmap.org/node/11988049441) | vehicular | Avenida 80 (primary) | en el extremo de una vía (borde de la red o calle ciega) |
| [567932575](https://www.openstreetmap.org/node/567932575) | peatonal | Avenida Las Vegas (primary) | en el extremo de una vía (borde de la red o calle ciega) |
| [348413118](https://www.openstreetmap.org/node/348413118) | vehicular | Carrera 52 (primary) | en el extremo de una vía (borde de la red o calle ciega) |
| [2431017474](https://www.openstreetmap.org/node/2431017474) | vehicular | Carrera 52D (primary) | en el extremo de una vía (borde de la red o calle ciega) |
| [1664735594](https://www.openstreetmap.org/node/1664735594) | vehicular | (sin nombre) (service) | en un cruce (revisar) |
| [10061788845](https://www.openstreetmap.org/node/10061788845) | vehicular | (sin nombre) (service) | en un cruce (revisar) |
| [3661813254](https://www.openstreetmap.org/node/3661813254) | vehicular | Calle 66F (secondary) | en un cruce (revisar) |
| [3661813246](https://www.openstreetmap.org/node/3661813246) | vehicular | Calle 67 (secondary) | en un cruce (revisar) |
| [3661813247](https://www.openstreetmap.org/node/3661813247) | vehicular | Calle 67 (secondary) | en un cruce (revisar) |
| [3661813268](https://www.openstreetmap.org/node/3661813268) | vehicular | Calle 69 (tertiary) | en un cruce (revisar) |
| [5558092753](https://www.openstreetmap.org/node/5558092753) | vehicular | Carrera 52 (secondary) | en un cruce (revisar) |
| [560719536](https://www.openstreetmap.org/node/560719536) | vehicular | Metroplús (service) | en un cruce (revisar) |
| [560719971](https://www.openstreetmap.org/node/560719971) | vehicular | Metroplús (service) | en un cruce (revisar) |
| [1664762039](https://www.openstreetmap.org/node/1664762039) | vehicular | Metroplús (service) | en un cruce (revisar) |
| [2548417179](https://www.openstreetmap.org/node/2548417179) | vehicular | Metroplús (service) | en un cruce (revisar) |
| [2548417181](https://www.openstreetmap.org/node/2548417181) | vehicular | Metroplús (service) | en un cruce (revisar) |
| [3661813252](https://www.openstreetmap.org/node/3661813252) | vehicular | Metroplús (service) | en un cruce (revisar) |
| [3661813305](https://www.openstreetmap.org/node/3661813305) | vehicular | Metroplús (service) | en un cruce (revisar) |
| [3661813322](https://www.openstreetmap.org/node/3661813322) | vehicular | Metroplús (service) | en un cruce (revisar) |
| [3637211708](https://www.openstreetmap.org/node/3637211708) | peatonal | (sin nombre) (secondary_link) | paso peatonal a mitad de cuadra |
| [4384580978](https://www.openstreetmap.org/node/4384580978) | peatonal | (sin nombre) (secondary_link) | paso peatonal a mitad de cuadra |
| [5247737818](https://www.openstreetmap.org/node/5247737818) | peatonal | (sin nombre) (secondary_link) | paso peatonal a mitad de cuadra |
| [8665414950](https://www.openstreetmap.org/node/8665414950) | peatonal | (sin nombre) (primary_link) | paso peatonal a mitad de cuadra |
| [10311534639](https://www.openstreetmap.org/node/10311534639) | peatonal | (sin nombre) (service) | paso peatonal a mitad de cuadra |
| [10557707901](https://www.openstreetmap.org/node/10557707901) | peatonal | (sin nombre) (residential) | paso peatonal a mitad de cuadra |
| [13527612726](https://www.openstreetmap.org/node/13527612726) | peatonal | (sin nombre) (primary_link) | paso peatonal a mitad de cuadra |
| [13527665121](https://www.openstreetmap.org/node/13527665121) | peatonal | (sin nombre) (primary_link) | paso peatonal a mitad de cuadra |
| [13948390354](https://www.openstreetmap.org/node/13948390354) | peatonal | (sin nombre) (service) | paso peatonal a mitad de cuadra |
| [3713684708](https://www.openstreetmap.org/node/3713684708) | peatonal | Avenida 33 (primary) | paso peatonal a mitad de cuadra |
| [4386154924](https://www.openstreetmap.org/node/4386154924) | peatonal | Avenida 33 (primary) | paso peatonal a mitad de cuadra |
| [4386154925](https://www.openstreetmap.org/node/4386154925) | peatonal | Avenida 33 (primary) | paso peatonal a mitad de cuadra |
| [10292129509](https://www.openstreetmap.org/node/10292129509) | peatonal | Avenida 80 (primary) | paso peatonal a mitad de cuadra |
| [10292129510](https://www.openstreetmap.org/node/10292129510) | peatonal | Avenida 80 (primary) | paso peatonal a mitad de cuadra |
| [338510059](https://www.openstreetmap.org/node/338510059) | peatonal | Avenida Bolivariana (secondary) | paso peatonal a mitad de cuadra |
| [9915898324](https://www.openstreetmap.org/node/9915898324) | peatonal | Avenida Bolivariana (secondary) | paso peatonal a mitad de cuadra |
| [9915898325](https://www.openstreetmap.org/node/9915898325) | peatonal | Avenida Bolivariana (secondary) | paso peatonal a mitad de cuadra |
| [8660931018](https://www.openstreetmap.org/node/8660931018) | peatonal | Avenida Carrera 46 (primary) | paso peatonal a mitad de cuadra |
| [8660931019](https://www.openstreetmap.org/node/8660931019) | peatonal | Avenida Carrera 46 (primary) | paso peatonal a mitad de cuadra |
| [339057390](https://www.openstreetmap.org/node/339057390) | peatonal | Avenida Carrera 57 (primary) | paso peatonal a mitad de cuadra |
| [11986825860](https://www.openstreetmap.org/node/11986825860) | peatonal | Avenida Las Vegas (primary) | paso peatonal a mitad de cuadra |
| [5506995808](https://www.openstreetmap.org/node/5506995808) | peatonal | Avenida San Juan (secondary) | paso peatonal a mitad de cuadra |
| [7235805069](https://www.openstreetmap.org/node/7235805069) | peatonal | Avenida San Juan (secondary) | paso peatonal a mitad de cuadra |
| [8644394470](https://www.openstreetmap.org/node/8644394470) | peatonal | Avenida San Juan (secondary) | paso peatonal a mitad de cuadra |
| [3547429896](https://www.openstreetmap.org/node/3547429896) | peatonal | Calle 10 (unclassified) | paso peatonal a mitad de cuadra |
| [4944568292](https://www.openstreetmap.org/node/4944568292) | peatonal | Calle 10 (secondary) | paso peatonal a mitad de cuadra |
| [4944568293](https://www.openstreetmap.org/node/4944568293) | peatonal | Calle 10 (secondary) | paso peatonal a mitad de cuadra |
| [1194445344](https://www.openstreetmap.org/node/1194445344) | peatonal | Calle 21 Sur (residential) | paso peatonal a mitad de cuadra |
| [2671871268](https://www.openstreetmap.org/node/2671871268) | peatonal | Calle 30 (tertiary) | paso peatonal a mitad de cuadra |
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
| [8666732087](https://www.openstreetmap.org/node/8666732087) | peatonal | Calle 69 (tertiary) | paso peatonal a mitad de cuadra |
| [8666732088](https://www.openstreetmap.org/node/8666732088) | peatonal | Calle 69 (tertiary) | paso peatonal a mitad de cuadra |
| [8666745841](https://www.openstreetmap.org/node/8666745841) | peatonal | Calle 78 (residential) | paso peatonal a mitad de cuadra |
| [8666745848](https://www.openstreetmap.org/node/8666745848) | peatonal | Calle 78 (residential) | paso peatonal a mitad de cuadra |
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
| [10313188996](https://www.openstreetmap.org/node/10313188996) | peatonal | Carrera 43A (primary) | paso peatonal a mitad de cuadra |
| [10313188997](https://www.openstreetmap.org/node/10313188997) | peatonal | Carrera 43A (primary) | paso peatonal a mitad de cuadra |
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
| [5512849444](https://www.openstreetmap.org/node/5512849444) | peatonal | Carrera 52D (primary) | paso peatonal a mitad de cuadra |
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
| [3667792259](https://www.openstreetmap.org/node/3667792259) | peatonal | Metroplús (service) | paso peatonal a mitad de cuadra |
| [3667792260](https://www.openstreetmap.org/node/3667792260) | peatonal | Metroplús (service) | paso peatonal a mitad de cuadra |
| [8660930976](https://www.openstreetmap.org/node/8660930976) | peatonal | Metroplús (service) | paso peatonal a mitad de cuadra |
| [8660930977](https://www.openstreetmap.org/node/8660930977) | peatonal | Metroplús (service) | paso peatonal a mitad de cuadra |
| [8660931020](https://www.openstreetmap.org/node/8660931020) | peatonal | Metroplús (service) | paso peatonal a mitad de cuadra |
| [8660931021](https://www.openstreetmap.org/node/8660931021) | peatonal | Metroplús (service) | paso peatonal a mitad de cuadra |
| [8668750373](https://www.openstreetmap.org/node/8668750373) | peatonal | Metroplús (service) | paso peatonal a mitad de cuadra |
| [8668750374](https://www.openstreetmap.org/node/8668750374) | peatonal | Metroplús (service) | paso peatonal a mitad de cuadra |
| [11114374105](https://www.openstreetmap.org/node/11114374105) | peatonal | Metroplús (service) | paso peatonal a mitad de cuadra |
| [11114374125](https://www.openstreetmap.org/node/11114374125) | peatonal | Metroplús (service) | paso peatonal a mitad de cuadra |
| [11139939530](https://www.openstreetmap.org/node/11139939530) | peatonal | Metroplús (service) | paso peatonal a mitad de cuadra |
| [11139939531](https://www.openstreetmap.org/node/11139939531) | peatonal | Metroplús (service) | paso peatonal a mitad de cuadra |
| [11139946871](https://www.openstreetmap.org/node/11139946871) | peatonal | Metroplús (service) | paso peatonal a mitad de cuadra |
| [11139946874](https://www.openstreetmap.org/node/11139946874) | peatonal | Metroplús (service) | paso peatonal a mitad de cuadra |
| [11139946878](https://www.openstreetmap.org/node/11139946878) | peatonal | Metroplús (service) | paso peatonal a mitad de cuadra |
| [11139946887](https://www.openstreetmap.org/node/11139946887) | peatonal | Metroplús (service) | paso peatonal a mitad de cuadra |
| [11139946890](https://www.openstreetmap.org/node/11139946890) | peatonal | Metroplús (service) | paso peatonal a mitad de cuadra |
| [11139946899](https://www.openstreetmap.org/node/11139946899) | peatonal | Metroplús (service) | paso peatonal a mitad de cuadra |
| [11139946902](https://www.openstreetmap.org/node/11139946902) | peatonal | Metroplús (service) | paso peatonal a mitad de cuadra |
| [348408723](https://www.openstreetmap.org/node/348408723) | vehicular | (sin nombre) (primary_link) | semáforo vehicular a mitad de vía |
| [366633944](https://www.openstreetmap.org/node/366633944) | vehicular | (sin nombre) (primary_link) | semáforo vehicular a mitad de vía |
| [4061457532](https://www.openstreetmap.org/node/4061457532) | vehicular | (sin nombre) (primary_link) | semáforo vehicular a mitad de vía |
| [4917215691](https://www.openstreetmap.org/node/4917215691) | vehicular | (sin nombre) (service) | semáforo vehicular a mitad de vía |
| [4917215695](https://www.openstreetmap.org/node/4917215695) | vehicular | (sin nombre) (service) | semáforo vehicular a mitad de vía |
| [5069582525](https://www.openstreetmap.org/node/5069582525) | vehicular | (sin nombre) (service) | semáforo vehicular a mitad de vía |
| [5495155157](https://www.openstreetmap.org/node/5495155157) | vehicular | (sin nombre) (primary_link) | semáforo vehicular a mitad de vía |
| [5553024665](https://www.openstreetmap.org/node/5553024665) | vehicular | (sin nombre) (primary_link) | semáforo vehicular a mitad de vía |
| [5553024669](https://www.openstreetmap.org/node/5553024669) | vehicular | (sin nombre) (secondary_link) | semáforo vehicular a mitad de vía |
| [8243620020](https://www.openstreetmap.org/node/8243620020) | vehicular | (sin nombre) (trunk_link) | semáforo vehicular a mitad de vía |
| [8243620022](https://www.openstreetmap.org/node/8243620022) | vehicular | (sin nombre) (trunk_link) | semáforo vehicular a mitad de vía |
| [8669024863](https://www.openstreetmap.org/node/8669024863) | vehicular | (sin nombre) (primary_link) | semáforo vehicular a mitad de vía |
| [9416236191](https://www.openstreetmap.org/node/9416236191) | vehicular | (sin nombre) (service) | semáforo vehicular a mitad de vía |
| [9416236196](https://www.openstreetmap.org/node/9416236196) | vehicular | (sin nombre) (service) | semáforo vehicular a mitad de vía |
| [10557799391](https://www.openstreetmap.org/node/10557799391) | vehicular | (sin nombre) (primary_link) | semáforo vehicular a mitad de vía |
| [13644498933](https://www.openstreetmap.org/node/13644498933) | vehicular | (sin nombre) (trunk_link) | semáforo vehicular a mitad de vía |
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
| [339269241](https://www.openstreetmap.org/node/339269241) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [5408098633](https://www.openstreetmap.org/node/5408098633) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [5530930969](https://www.openstreetmap.org/node/5530930969) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [5530930970](https://www.openstreetmap.org/node/5530930970) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [5530930974](https://www.openstreetmap.org/node/5530930974) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
| [6983560951](https://www.openstreetmap.org/node/6983560951) | vehicular | Avenida Las Vegas (primary) | semáforo vehicular a mitad de vía |
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
| [13674485197](https://www.openstreetmap.org/node/13674485197) | vehicular | Carrera 43A (primary) | semáforo vehicular a mitad de vía |
| [7029925200](https://www.openstreetmap.org/node/7029925200) | vehicular | Carrera 43B (secondary) | semáforo vehicular a mitad de vía |
| [7029925201](https://www.openstreetmap.org/node/7029925201) | vehicular | Carrera 43B (secondary) | semáforo vehicular a mitad de vía |
| [9943516217](https://www.openstreetmap.org/node/9943516217) | vehicular | Carrera 43C (secondary) | semáforo vehicular a mitad de vía |
| [9943516218](https://www.openstreetmap.org/node/9943516218) | vehicular | Carrera 43C (secondary) | semáforo vehicular a mitad de vía |
| [4100629952](https://www.openstreetmap.org/node/4100629952) | vehicular | Carrera 45 (tertiary) | semáforo vehicular a mitad de vía |
| [4100629954](https://www.openstreetmap.org/node/4100629954) | vehicular | Carrera 45 (tertiary) | semáforo vehicular a mitad de vía |
| [5497069516](https://www.openstreetmap.org/node/5497069516) | vehicular | Carrera 45 (tertiary) | semáforo vehicular a mitad de vía |
| [9758160433](https://www.openstreetmap.org/node/9758160433) | vehicular | Carrera 48 (residential) | semáforo vehicular a mitad de vía |
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
| [833662051](https://www.openstreetmap.org/node/833662051) | vehicular | Carrera 52D (primary) | semáforo vehicular a mitad de vía |
| [3514626604](https://www.openstreetmap.org/node/3514626604) | vehicular | Carrera 55 (tertiary) | semáforo vehicular a mitad de vía |
| [5553024683](https://www.openstreetmap.org/node/5553024683) | vehicular | Carrera 55 (secondary) | semáforo vehicular a mitad de vía |
| [5553024686](https://www.openstreetmap.org/node/5553024686) | vehicular | Carrera 55 (secondary) | semáforo vehicular a mitad de vía |
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
| [8566349459](https://www.openstreetmap.org/node/8566349459) | vehicular | (sin nombre) (primary) | sobre el anillo de una glorieta |
| [8566349466](https://www.openstreetmap.org/node/8566349466) | vehicular | (sin nombre) (primary) | sobre el anillo de una glorieta |
| [3617311445](https://www.openstreetmap.org/node/3617311445) | vehicular | Metroplús (service) | sobre el anillo de una glorieta |
| [8566349426](https://www.openstreetmap.org/node/8566349426) | vehicular | Metroplús (service) | sobre el anillo de una glorieta |

**Glorietas con semáforos en el anillo: (sin nombre), Metroplús.** En la red funcionan como glorietas con prelación para quien va dentro, y en la realidad están semaforizadas. El plan semafórico de una glorieta no se puede adivinar: hay que construirlo a mano en netedit con los tiempos reales.

## Restricciones de giro y carriles de giro

OSM trae **750 relaciones de restricción de giro** para 12429 intersecciones con al menos dos entradas y dos salidas (6.0 por cada 100). Cualquier giro prohibido que no esté mapeado queda permitido en la simulación.

| tipo | relaciones |
|---|---:|
| no_left_turn | 399 |
| ? | 164 |
| no_right_turn | 102 |
| no_u_turn | 48 |
| only_straight_on | 24 |
| only_right_turn | 7 |
| only_left_turn | 2 |
| no_straight_on | 2 |
| only_u_turn | 2 |

netconvert ignoró 24 por referir vías que no están en la descarga o que no son para autos.

Flechas de giro por carril (`turn:lanes`) en OSM, por tipo de vía:

| tipo | vías con turn:lanes | vías del tipo |
|---|---:|---:|
| residential | 382 | 10988 |
| service | 5 | 8261 |
| tertiary | 580 | 3080 |
| secondary | 275 | 1649 |
| primary | 136 | 915 |
| unclassified | 2 | 818 |
| trunk | 34 | 343 |
| primary_link | 12 | 322 |
| secondary_link | 12 | 241 |
| trunk_link | 6 | 201 |
| tertiary_link | 13 | 99 |
| platform | 0 | 28 |
| living_street | 0 | 16 |

## Componentes desconectados

Calculado sobre la red **antes de podar**, con las conexiones que puede usar
un auto.

|  | valor |
|---|---:|
| Componentes débilmente conexos | 13 |
| Aristas en el mayor (débil) | 43802 (99.8 %) |
| Componentes fuertemente conexos | 203 |
| Aristas en el mayor (fuerte) | 43569 (99.2 %) |
| Componentes fuertes de más de 1 arista, aparte del mayor | 17 |
| Aristas conservadas | 43802 |
| Aristas podadas: islas (otro componente débil) | 106 |
| Aristas podadas: trampas dentro del componente principal | 0 |

Una arista se conserva si un vehículo puede recorrerla de principio a fin: porque
llega al componente fuerte principal, porque se llega a ella desde él, o porque
está entre una entrada y una salida de la red (vías de paso por el borde).
Se poda lo demás: islas sin conexión vial con el resto y trampas (tramos de
sentido único a los que no se puede llegar o que no llevan a ninguna parte).
Casi siempre son errores de sentido o de conexión en OSM.

Islas: 106 aristas, 27.34 km, en estas vías OSM. Revisar en netedit o corregir en OSM (una isla suele ser una conexión que falta en el mapa, o una vía de un tipo que no se descarga, como `track`):

- [61395788](https://www.openstreetmap.org/way/61395788), [176994955](https://www.openstreetmap.org/way/176994955), [185660054](https://www.openstreetmap.org/way/185660054), [185660625](https://www.openstreetmap.org/way/185660625), [199485428](https://www.openstreetmap.org/way/199485428), [201197726](https://www.openstreetmap.org/way/201197726), [204198041](https://www.openstreetmap.org/way/204198041), [206545277](https://www.openstreetmap.org/way/206545277), [206545278](https://www.openstreetmap.org/way/206545278), [258924388](https://www.openstreetmap.org/way/258924388), [258924391](https://www.openstreetmap.org/way/258924391), [552231576](https://www.openstreetmap.org/way/552231576), [552231577](https://www.openstreetmap.org/way/552231577), [552231578](https://www.openstreetmap.org/way/552231578), [558314961](https://www.openstreetmap.org/way/558314961), [560763516](https://www.openstreetmap.org/way/560763516), [571721526](https://www.openstreetmap.org/way/571721526), [571721527](https://www.openstreetmap.org/way/571721527), [571721530](https://www.openstreetmap.org/way/571721530), [1017048101](https://www.openstreetmap.org/way/1017048101), [1017099721](https://www.openstreetmap.org/way/1017099721), [1017816788](https://www.openstreetmap.org/way/1017816788), [1017816789](https://www.openstreetmap.org/way/1017816789), [1018913291](https://www.openstreetmap.org/way/1018913291), [1018913292](https://www.openstreetmap.org/way/1018913292), [1067839251](https://www.openstreetmap.org/way/1067839251), [1067843799](https://www.openstreetmap.org/way/1067843799), [1067843801](https://www.openstreetmap.org/way/1067843801), [1067885876](https://www.openstreetmap.org/way/1067885876), [1067885877](https://www.openstreetmap.org/way/1067885877), [1102446436](https://www.openstreetmap.org/way/1102446436), [1102487353](https://www.openstreetmap.org/way/1102487353), [1389963057](https://www.openstreetmap.org/way/1389963057), [1389963059](https://www.openstreetmap.org/way/1389963059), [1409952502](https://www.openstreetmap.org/way/1409952502), [1410572892](https://www.openstreetmap.org/way/1410572892), [1416607078](https://www.openstreetmap.org/way/1416607078), [1459094972](https://www.openstreetmap.org/way/1459094972), [1459094973](https://www.openstreetmap.org/way/1459094973), [1459094974](https://www.openstreetmap.org/way/1459094974), [1498237793](https://www.openstreetmap.org/way/1498237793), [1511075222](https://www.openstreetmap.org/way/1511075222), [1527929762](https://www.openstreetmap.org/way/1527929762), [1528613449](https://www.openstreetmap.org/way/1528613449), [1528613450](https://www.openstreetmap.org/way/1528613450), [1537276215](https://www.openstreetmap.org/way/1537276215), [1537276216](https://www.openstreetmap.org/way/1537276216), [1549141120](https://www.openstreetmap.org/way/1549141120), [1549141121](https://www.openstreetmap.org/way/1549141121), [1549143660](https://www.openstreetmap.org/way/1549143660)

## Aristas de entrada y salida (`is_fringe`)

|  | entradas | salidas |
|---|---:|---:|
| Total | 3420 | 3399 |
| … en vías arteriales (troncal a terciaria) | 88 | 77 |
| … en vías locales | 3332 | 3322 |

`is_fringe` marca toda arista cuyo nodo extremo no tiene otra continuación.
Eso incluye los cruces reales del límite municipal, pero también las calles
ciegas internas. Las entradas en vías arteriales son casi todas conexiones con
los municipios vecinos; las locales son mayoritariamente calles sin salida.
La demanda sintética de `python main.py prueba-tecnica` se reparte
uniformemente entre todas, así que la mayoría de esos viajes entran y salen
por calles ciegas: otra razón por la que esa demanda no representa nada.

## Advertencias de netconvert

Salida completa en `medellin_netconvert.log`.

| mensaje | veces |
|---|---:|
| Not joining junctions % (%). | 731 |
| Speed of % connection '%' reduced by % due to turning radius of % (length=%, angle=%). | 698 |
| Found sharp turn with radius % at the % of edge '%'. | 387 |
| Reducing junction cluster % (%). | 354 |
| Intersecting left turns at junction '%' from lane '%' and lane '%' (increase junction radius to avoid this). | 245 |
| Ignoring restriction relation '%' with unknown type. | 159 |
| Cannot apply turn sign information for edge '%' because there are % signed directions but only % targets | 158 |
| Removed a road without junctions: %. | 113 |
| Found angle of % degrees at edge '%', segment %. | 110 |
| Ambiguity in turnarounds computation at junction '%'. | 66 |
| Ignoring turn sign information for % lanes on edge % with % driving lanes | 57 |
| No way found for reference '%' in relation '%' | 53 |
| Could not find corresponding edge or compatible lane for free-floating pt stop '%' (%). Thus, it will be removed! | 43 |
| Cannot apply turn sign information for edge '%' because there are % signed directions and % targets (after target pruning) | 39 |
| Cannot apply turn sign information for edge '%' because there are % signed connections with directions '%' but target edge '%' has only % suitable lanes | 35 |

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
