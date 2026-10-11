# Demanda estimada (modelo gravitacional + Furness)

Generado por `python main.py demanda`. No editar a mano.

> Matriz ESTIMADA, no observada (beta = 0.1 por minuto, sin calibrar). Ver la seccion de supuestos.

Red: `barbosa_bello_caldas_copacabana_envigado_girardota_itagui_la_estrella_medellin_sabaneta.net.xml`

## Zonas

| zona | km de calles | viajes que salen (informe) | llegan (informe) | vehiculos privados/dia que salen | min dentro de la zona |
|---|---|---|---|---|---|
| Bello | 816 | 660,461 | 670,717 | 174,847 | 9.7 |
| La Candelaria | 151 | 560,721 | 578,475 | 148,442 | 2.1 |
| Itagüí | 285 | 481,845 | 485,419 | 127,561 | 3.1 |
| El Poblado | 253 | 446,255 | 444,067 | 118,139 | 2.9 |
| Envigado | 700 | 396,896 | 399,271 | 105,072 | 14.1 |
| Robledo | 184 | 331,970 | 330,584 | 87,884 | 2.5 |
| Belén | 241 | 330,428 | 328,045 | 87,476 | 1.9 |
| Laureles-Estadio | 170 | 296,592 | 298,227 | 78,518 | 1.8 |
| Buenos Aires | 137 | 260,201 | 235,550 | 68,884 | 2.6 |
| Manrique | 140 | 243,372 | 243,652 | 64,429 | 1.5 |
| San Javier | 162 | 237,089 | 234,376 | 62,766 | 1.9 |
| Aranjuez | 131 | 234,077 | 234,036 | 61,968 | 1.3 |
| Castilla | 133 | 208,450 | 208,720 | 55,184 | 2.0 |
| Doce de Octubre | 146 | 202,835 | 198,840 | 53,698 | 1.1 |
| Popular | 90 | 196,083 | 183,715 | 51,910 | 1.4 |
| La América | 126 | 178,470 | 176,290 | 47,247 | 1.4 |
| Sabaneta | 152 | 175,120 | 177,894 | 46,360 | 3.0 |
| Villa Hermosa | 133 | 148,514 | 139,718 | 39,317 | 1.7 |
| Guayabal | 146 | 144,787 | 143,038 | 38,330 | 1.9 |
| Caldas | 349 | 120,822 | 118,937 | 31,986 | 11.0 |
| Santa Cruz | 72 | 110,973 | 92,605 | 29,378 | 1.3 |
| La Estrella | 222 | 101,509 | 98,601 | 26,873 | 4.7 |
| Copacabana | 437 | 83,904 | 84,578 | 22,212 | 10.7 |
| Barbosa | 761 | 80,201 | 80,594 | 21,232 | 14.9 |
| Girardota | 510 | 72,599 | 69,918 | 19,220 | 8.2 |
| San Cristóbal | 361 | 57,351 | 56,937 | 15,183 | 6.2 |
| San Antonio de Prado | 271 | 51,128 | 51,141 | 13,535 | 7.0 |
| Santa Elena | 390 | 13,559 | 14,748 | 3,590 | 19.0 |
| Altavista | 135 | 12,697 | 12,577 | 3,361 | 8.2 |
| San Sebastián de Palmitas | 125 | 1,495 | 1,158 | 396 | 10.9 |

## Matriz

- Vehiculos privados por dia: 1,705,001 (auto y moto).
- Furness convergio en 10 iteraciones.
- Viajes dentro de la misma zona: 10.6%.

| origen | destino | vehiculos/dia | minutos a flujo libre |
|---|---|---|---|
| Bello | Bello | 34,479 | 9.7 |
| Itagüí | Itagüí | 21,266 | 3.1 |
| La Candelaria | La Candelaria | 18,432 | 2.1 |
| Envigado | Envigado | 14,293 | 14.1 |
| El Poblado | El Poblado | 13,625 | 2.9 |
| Bello | La Candelaria | 13,425 | 11.7 |
| La Candelaria | Bello | 13,352 | 12.7 |
| Itagüí | Envigado | 13,218 | 12.8 |
| Envigado | Itagüí | 13,142 | 10.1 |
| El Poblado | Envigado | 11,814 | 11.3 |

## Sensibilidad a beta

El factor implicito es cuanto habria que multiplicar el tiempo medio a flujo libre para llegar a los 39.03 min del informe. Un factor entre 2 y 3 corresponde a una velocidad puerta a puerta de un tercio a la mitad de la de flujo libre. Beta mas alto concentra los viajes cerca de su origen.

| beta (1/min) | minutos a flujo libre | factor implicito | viajes internos | iteraciones |
|---|---|---|---|---|
| 0.00 | 12.3 | 3.18 | 5.3% | 1 |
| 0.05 | 11.4 | 3.42 | 7.5% | 4 |
| 0.10 (usado) | 10.3 | 3.79 | 10.6% | 10 |
| 0.15 | 9.3 | 4.20 | 14.1% | 21 |
| 0.20 | 8.5 | 4.59 | 17.8% | 38 |
| 0.30 | 7.4 | 5.31 | 25.0% | 84 |

## Esta corrida

- Ventana: 5:00 a 10:00. Escala: 2%. Semilla: 1.
- Vehiculos sorteados: 12,897 (esperados 12,932).
- Otra semilla da otro sorteo con el mismo patron promedio; la misma semilla repite la corrida.

## Supuestos

### 1. `matriz_estimada`

La matriz no es observada. El informe da cuantos viajes salen y llegan a cada macrozona, no quien va a donde; el reparto entre pares sale de un modelo gravitacional doblemente restringido balanceado con Furness. Sirve para que la demanda tenga estructura espacial razonable, no para afirmar flujos entre zonas.

### 2. `zonificacion_provisional`

Se usan 30 zonas: las 16 comunas y 5 corregimientos de Medellin, que estan en OSM, y un bloque por cada uno de los otros nueve municipios, porque OSM no tiene las comunas de Bello e Itagui, las zonas de Envigado ni el limite urbano-rural. Las 46 macrozonas de esos municipios se suman en su bloque. Con los poligonos oficiales de AMVA se puede volver a las 67.

### 3. `sin_especificar`

Los viajes de la macrozona 'Sin especificar' se reparten en proporcion a las demas zonas.

### 4. `beta_sin_calibrar`

beta = 0.1 por minuto no esta calibrado. El unico tiempo del informe para el transporte privado (39.03 min) es puerta a puerta y con congestion; los tiempos del modelo son de flujo libre sobre la red. Compararlos exige suponer un factor entre ambos, y beta depende de ese factor (ver la tabla de sensibilidad). El histograma de duraciones del informe incluye los viajes a pie y no sirve para el privado.

### 5. `tiempos_flujo_libre`

El tiempo entre zonas es el del camino mas rapido entre sus aristas representativas, a la velocidad maxima de cada calle. Dentro de una zona es el promedio desde su arista representativa hacia sus calles, ponderado por largo.

### 6. `patron_igual_todo_el_dia`

El informe da los totales por zona del dia, no por hora. Todas las horas usan la misma matriz escalada por el perfil horario del privado: no se distingue la ida de la manana de la vuelta de la tarde.

### 7. `reparto_modal_uniforme`

Las marginales son de todos los modos. Se supone que auto y moto (su cuota en 'Modo Principal') pesan lo mismo en todas las zonas, lo que subestima el privado en zonas como El Poblado y lo sobreestima en otras.

### 8. `un_vehiculo_por_viaje`

Cada viaje privado es un vehiculo: el informe no trae ocupacion vehicular.

### 9. `calles_de_origen`

Los viajes empiezan y terminan en calles del nucleo conectado, con probabilidad proporcional a su largo. Se excluyen autopistas, troncales y tramos de menos de 10 m. No hay datos de donde viven o trabajan las personas dentro de cada zona.

### 10. `escala_sin_capacidad`

Se simula el 2% de los vehiculos sin reducir la capacidad de las vias, asi que la congestion queda subestimada. Sirve para probar la cadena y ver el patron espacial, no para medir congestion.
