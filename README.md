# constructor-virtual-circuitos-skill

Skill de Claude para trabajar con el **Constructor Virtual y Simulador de Circuitos Digitales 0.9.7** (PUCP, 2011, www.tourdigital.net): explica el programa y genera circuitos `.txt` (`Version 0.9.7`) con protoboard, chips TTL 74xx, interruptores, pulsadores, LEDs, siete segmentos, temporizador y fuente DC.

El conocimiento sale de analizar el ejecutable (sin ejecutarlo) y de probar los archivos generados en el programa real.

## Contenido

- `SKILL.md`: la skill (modelo de simulación, catálogo de chips, geometría, formato de archivo, generador, receta del contador).
- `tools/ckv_gen.py`: generador y verificador en Python 3 (extraído de la sección 7 del skill).
- `examples/contador_pulsador.txt`: contador 000 a 999 con pulsador como reloj.
- `examples/contador_timer.txt`: el mismo contador con el temporizador (10 Hz).

## Instalación

Copia `SKILL.md` en una carpeta `constructor-virtual-circuitos/` dentro del directorio de skills de Claude (o súbela desde la configuración de skills de Claude).

## Uso de los ejemplos

1. En el programa: Circuitos > Recuperar y elige el `.txt`.
2. Enciende la fuente DC con un clic en su interruptor (el archivo no guarda ese estado).
3. Con pulsador, pulsa el primer pulsador; con temporizador cuenta solo.

## Qué está verificado

Probado en el programa real: fuente, protoboard (rieles y columnas), siete segmentos, 74LS90, 74LS47, pulsadores, temporizador y el contador 000-999 completo.

Sin verificar: PLA con contenido y el comportamiento de chips distintos de 7490 y 7447.
