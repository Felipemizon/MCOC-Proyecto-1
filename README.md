# MCOC-Proyecto-1
## Introducción
Los disipadores sísmicos son elementos que se utilizan en obras civiles como edificios, los cuales permiten una mejor respuesta de cara a sismo debido a que estos absorben gran cantidad de energía liberada sobre el edificio, aumentando los periodos de la estructura y por ende, minimizando las deformaciones por el movimiento telúrico.
##**Objetivos**
El objetivo de este proyecto es diseñar un sistema de disipación de energía para un edificio, utilizando una modelación simplificada de este. Se debe determinar la cantidad y distribución de cada tipo de sisipador a utilizar. El objetivo del sistema es minimizar el drift de entrepiso máximo en el edificio, con la idea de minimizar el daño que este experimenta durante un sismo severo.
##**Procedimiento**
Para su resolución es necesario generar matrices de masa (M), amortiguamiento (C) y rigidez (K) para el sistema, además del vector de cargas f(t) y efecto de amortiguadores friccionales dada una distribución de capacidades fija. Con esto se logra generar ecuaciones diferenciales que pueden ser resueltas por el método RK45 y el método de euler, utilizando una base de datos de registros sísmicos previamente analizados.
Con respecto a los disipadores, hay disponibles de 150KN, 250KN, 500KN y 800KN de capacidad. Se debe considerar que la suma total instalada no puede exceder los 5.000KN.
