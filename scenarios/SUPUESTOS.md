# Supuestos y limitaciones del pipeline

Generado automaticamente por `python main.py preparar-insumos`.
No editar a mano: se sobrescribe en cada corrida.

## Lo que si sale del informe

- Perfil horario de inicio de viaje por grupo modal (dato directo).
- Cuotas modales para definir vType (dato directo, con la salvedad de abajo).
- Volumen total de control: 6,490,296 viajes/dia habil.
- Viajes privados motorizados: 1,705,001.
- Marginales de origen y de destino por macrozona (67 zonas).

## Lo que NO sale del informe y bloquea la simulacion

1. **Matriz OD.** Solo hay marginales independientes: 134 numeros para una
   matriz de 67x67 = 4.489 celdas. La conjunta no es recuperable desde las
   marginales. `od2trips` no se puede alimentar. Este es el bloqueante #1.
2. **Distancia por viaje.** Solo hay duracion en rangos, confundida con el
   modo. Sin distancia no hay funcion de impedancia ni estimacion de
   kilometraje diario (y por tanto no hay SOC).
3. **Zonificacion fina.** 67 macrozonas para 4,06 M de habitantes es escala
   macro. Microsimular con TAZ de ese tamano fabrica cuellos de botella
   inexistentes.
4. **Cadenas de viaje.** 47,16 % de los viajes son 'regreso al hogar', pero
   un agregado no permite enlazar viajes con personas.
5. **Aforos de validacion.** Ninguno. Sin conteos la simulacion no es
   calibrable ni defendible.

Los cinco se resuelven con una sola cosa: el microdato de la EOD 2025.

Los supuestos de la red vial van en `redes/<municipio>_calidad.md`.

## Supuestos tomados

### 1. `taxonomia_modal`

El informe da dos reparticiones modales incompatibles: 'Modo Principal' (8 categorias) implica 26.27 % de viajes en modo privado motorizado, mientras la hoja horaria (4 grupos) implica 28.96 %. La diferencia de 2.69 pp queda sin explicar porque la categoria 'Otros' (6.33 %) no esta desagregada. Se adopta 'Modo Principal' para las cuotas de vType y la hoja horaria para el perfil temporal. Resolver esto requiere el microdato.

### 2. `perfil_privado_compartido`

La hoja horaria agrega automovil y motocicleta en un solo grupo 'privado'. Al no existir curvas separadas, ambos vType heredan el mismo perfil de salida. Es un supuesto fuerte: los patrones de salida de auto y moto difieren, y esto sesga cualquier estimacion de composicion vehicular por hora. Corregible solo con el microdato.

### 3. `hora_inicio_no_es_hora_de_carga`

El perfil horario describe la hora de INICIO DEL VIAJE, no la hora de conexion a un cargador. No debe usarse directamente como perfil de carga electrica. Para eso hace falta modelar el fin del ultimo viaje del dia por vehiculo, lo que exige cadenas de viaje encadenadas por persona.

### 4. `moto_sin_calibrar`

La motocicleta es el 59,94 % del parque y el 14,57 % de los viajes. Los parametros laterales del vType 'moto' son valores de arranque, no calibrados. Sin calibrar el modelo sublane contra aforos locales, la simulacion sobreestimara la congestion de forma severa.

### 5. `bev_plantilla`

El vType 'auto_bev' usa parametros de plantilla del modelo battery de SUMO. El informe solo dice que 5,04 % del parque opera con 'tecnologias limpias', sin aclarar si eso incluye GNV e hibridos o solo electricos puros. Esa definicion hay que confirmarla con AMVA antes de usar el dato.
