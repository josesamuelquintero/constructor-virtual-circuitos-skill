---
name: "constructor-virtual-circuitos"
description: "Explica y genera circuitos .txt (Version 0.9.7) del Constructor Virtual y Simulador de Circuitos Digitales: protoboard, chips TTL 74xx, interruptores, LEDs, siete segmentos y fuente DC."
---

# Constructor Virtual y Simulador de Circuitos Digitales 0.9.7

Usar este skill cuando el usuario mencione `ConstructorVirtualDeCircuitos.exe`, el "Constructor Virtual sobre Protoboards", circuitos guardados como `.txt` con cabecera `Version 0.9.7`, o pida diseñar, explicar, revisar o generar un circuito digital TTL para ese programa.

## 1. Qué es y de dónde sale este conocimiento

- Programa Win32 (GUI) de mayo de 2011, C++ compilado con MinGW. Autor indicado en el Acerca de: Arturo Javier Miguel de Priego Paz Soldán (PUCP), www.tourdigital.net. Tamaño 2 541 180 bytes, SHA-256 `ea56cc14e73f51bf69576ff721f5295c5b8f156e2ace77fc97e98e1a27ef2d2c`.
- Simula una mesa de trabajo (2000x1500 px) con protoboards, tableros de entrada/salida, una fuente DC y chips TTL de la serie 74xx. Se trabaja con el ratón: se colocan tableros, se insertan chips en la protoboard y se tienden cables entre agujeros.
- El conocimiento viene de **análisis estático del ejecutable** (símbolos C++, strings, desensamblado, recursos) más **pruebas reales del usuario** con archivos generados por este skill.
- **Verificado con archivos reales guardados por el programa**: formato completo, protoboard (R1, R2, R3, R4), interruptores, pulsadores, LEDs, fuente DC.
- **Verificado ejecutando en el programa real** (el usuario abrió los archivos generados): fuente DC encendida, rieles y columnas de ambas tiras (R1 y R2), tablero de siete segmentos (terminal VCC y segmentos a..g), chips 74LS90 y 74LS47 insertados con la geometría de la sección 5, **temporizador** (geometría de sus salidas, `timer_visible=1`, cuenta sola) y un **contador 000–999 con tres 74LS90 + tres 74LS47**, tanto con pulsador como con temporizador, que cuenta correctamente.
- **Sin verificar**: PLA con contenido, fidelidad de cada chip distinto de 7490/7447.
- Lección: un fallo "todo apagado" casi siempre fue geometría de pines mal asignada, no el programa. Probar en etapas (display solo, un chip, circuito completo).

## 2. Interfaz y flujo de uso

- Menú **Circuitos**: Nuevo, Recuperar..., Almacenar, Almacenar en..., Salir. Filtro `*.txt`. Solo abre la versión 0.9.7 (si no, "El programa solo abre archivos de la versión 0.9.7").
- Menú **Tableros**: Protoboard (breadboard), Interruptores, Pulsadores, Leds, Leds de siete segmentos, Temporizador. Menú **Circuitos TTL**: catálogo de chips por familia. Menú **Tutoriales**: PLA de 4x8x4.
- La fuente DC tiene un interruptor de encendido. **La simulación solo corre con la fuente encendida, y el archivo NO guarda ese estado: al abrir un circuito la fuente está apagada y hay que encenderla con un clic en su interruptor** (el LED rojo de la fuente se ilumina). Hay que apagarla antes de crear, recuperar o salir. Para eliminar un tablero primero hay que retirar cables y componentes.
- Un circuito nuevo trae fuente DC y temporizador (este oculto). Un tablero PLA oculto de tamaño 0 (`8 0 0 0 0 0 <id>`) aparece en algunos archivos guardados; no es necesario para circuitos sin PLA.
- Un chip recién creado aparece suelto en (20,50) y se arrastra hasta la protoboard.

## 3. Modelo de simulación

- Cada pin de chip tiene un tipo: `E` entrada, `S` salida, `V` Vcc, `G` tierra, `N` sin conexión. Los estados de un puerto son `'0'`, `'1'` o `'Z'` (alta impedancia). Una entrada en `'Z'` se lee como 1.
- Fuente DC encendida: 4 agujeros superiores = `1` (+5 V, tipo V) y 4 inferiores = `0` (tierra, tipo G). Apagada: `Z`.
- **Alimentación = tipo del nodo, no solo el valor**: el programa propaga por los cables el *tipo* V/G desde la fuente. Un chip solo calcula si el nodo de cada pin V es de tipo V (con valor 1) y el de cada pin G es de tipo G; si no, **todas sus salidas pasan a 0**. Por eso Vcc/GND de cada chip deben llegar por cable desde la fuente (directo o vía rieles/columnas).
- **Tableros activos necesitan alimentación por cable**: interruptores, pulsadores y temporizador exigen un agujero Vcc a `1` y uno GND a `0`. El tablero de LEDs exige el agujero GND a `0`; el LED i se enciende si su puerto vale `1`.
- Cuatro chips (7483A, 74164, 74166, 74191) no declaran pines V/G (tipados como `E`), así que funcionan sin alimentación.
- **Un solo cable por agujero**: cada puerto guarda un único puntero de conexión, así que un segundo cable en el mismo agujero desconecta o pisa al primero (comprobado: dos cables en la salida 0 del temporizador dejaron sin reloj al contador). Usar un agujero distinto para cada cable: en una columna de protoboard hay 5 agujeros, de los que uno (R1 fila 4 / R2 fila 0) lo ocupa el pin del chip; en el temporizador, interruptores y pulsadores cada unidad tiene 3 agujeros (r=0..2, mismo nodo).
- Se itera la función de los chips hasta que nadie cambie (tope 1000 iteraciones); si hay realimentación sin solución sale un aviso.
- **7447** (comportamiento del código): LT (pin 3) en 0 → todas las salidas a 0 (prueba de lámparas); BCD 0 con RBI (pin 5) en 0 → todo apagado (salidas 1); si no, salidas activas en 0 según el dígito. BI/RBO (pin 4) no se lee: se puede dejar sin conectar. Con LT y RBI a +5 V muestra todos los dígitos, incluido el cero inicial.
- **Siete segmentos**: el segmento i se enciende solo si la terminal VCC del tablero es tipo V con valor 1 **y** el puerto i vale `0` (ánodo común, activo en bajo; encaja con las salidas del 7447/74247 sin inversores).
- **Temporizador** ✓: avanza cada 47 ms; solo avanza si el tablero está marcado como visible (línea `timer_visible` = 1). Sus 4 salidas c=0..3 están rotuladas **10 Hz, 5 Hz, 2 Hz, 1 Hz**. A 10 Hz un contador 000–999 tarda unos 100 s en completar la cuenta.
- Se asume comportamiento de hoja de datos 74LS para cada chip; solo 7490 y 7447 se vieron funcionar.

## 4. Catálogo de chips

Código de componente en el archivo = **7000 + sufijo** (74LS00 → 7000, 74LS11 → 7011, 74LS138 → 7138, 74LS669 → 7669). Columnas: chip, código, pines, bits de estado interno, tipos de pin 1..N en orden.

```
7400|7000|14|0|EESEESGSEESEEV
7402|7002|14|0|SEESEEGEESEESV
7404|7004|14|0|ESESESGSESESEV
7408|7008|14|0|EESEESGSEESEEV
7410|7010|14|0|EEEEESGSEEESEV
7411|7011|14|0|EEEEESGSEEESEV
7420|7020|14|0|EENEESGSEENEEV
7421|7021|14|0|EENEESGSEENEEV
7427|7027|14|0|EEEEESGSEEESEV
7430|7030|14|0|EEEEEEGSNNEENV
7432|7032|14|0|EESEESGSEESEEV
7442|7042|16|0|SSSSSSSGSSSEEEEV
7447|7047|16|0|EEESEEEGSSSSSSSV
7451|7051|14|0|EEEEESGSEEEEEV
7454|7054|14|0|EEEEESGNEEEEEV
7455|7055|14|0|EEEENNGSNEEEEV
7473|7073|14|0|EEEVEEESSEGSSE
7474|7074|14|2|EEEESSGSSEEEEV
7475|7075|16|0|SEEEVEESSSSGESSS
7476A|7076|16|2|EEEEVEEEESSEGSSE
7477|7077|14|0|EEEVEENSSNGESS
7483A|7083|16|0|ESEEESEESEEEESSE
7485|7085|16|0|EEEESSSGEEEEEEEV
7486|7086|14|0|EESEESGSEESEEV
7490|7090|14|2|EEENVEESSGSSNE
7492|7092|14|2|ENNNVEESSGSSNE
7493|7093|14|2|EEENVNNSSGSSNE
7495|7095|14|1|EEEEEEGEESSSSV
74107|7107|14|2|ESSESSGEEEEEEV
74109|7109|16|2|EEEEESSGSSEEEEEV
74112|7112|16|2|EEEESSSGSEEEEEEV
74113|7113|14|2|EEEESSGSSEEEEV
74114|7114|14|1|EEEESSGSSEEEEV
74133|7133|16|0|EEEEEEEGSEEEEEEV
74137|7137|16|3|EEEEEESGSSSSSSSV
74138|7138|16|0|EEEEEESGSSSSSSSV
74139|7139|16|0|EEESSSSGSSSSEEEV
74147|7147|16|0|EEEEESSGSEEEESNV
74148|7148|16|0|EEEEESSGSEEEESSV
74151|7151|16|0|EEEESSEGEEEEEEEV
74153|7153|16|0|EEEEEESGSEEEEEEV
74155|7155|16|0|EEESSSSGSSSSEEEV
74157|7157|16|0|EEESEESGSEESEEEV
74158|7158|16|0|EEESEESGSEESEEEV
74160|7160|16|1|EEEEEEEGEESSSSSV
74161|7161|16|1|EEEEEEEGEESSSSSV
74162|7162|16|1|EEEEEEEGEESSSSSV
74163|7163|16|1|EEEEEEEGEESSSSSV
74164|7164|14|1|EESSSSEEESSSSE
74165|7165|16|9|EEEEEESGSEEEEEEV
74166|7166|16|9|EEEEEEEEEEEESEEE
74168|7168|16|1|EEEEEEEGEESSSSSV
74169|7169|16|1|EEEEEEEGEESSSSSV
74170|7170|16|16|EEEEESSGSSEEEEEV
74174|7174|16|1|ESEESESGESESEESV
74175|7175|16|1|ESSEESSGESSEESSV
74181|7181|24|0|EEEEEEEESSSGSSSSSEEEEEEV
74190|7190|16|1|ESSEESSGEEESSEEV
74191|7191|16|1|ESSEESSEEEESSEEE
74192|7192|16|2|ESSEESSGEEESSEEV
74193|7193|16|2|ESSEESSGEEESSEEV
74194|7194|16|1|EEEEEEEGEEESSSSV
74195|7195|16|1|EEEEEEEGEESSSSSV
74196|7196|14|2|ESEESEGESEESEV
74197|7197|14|2|ESEESEGESEESEV
74247|7247|16|0|EEEEEEEGSSSSSSSV
74256|7256|16|0|EEESSSSGSSSSEEEV
74259|7259|16|0|EEESSSSGSSSSEEEV
74260|7260|14|0|EEEESSGEEEEEEV
74273|7273|20|1|ESEESSEESGESEESSEESV
74279|7279|16|0|EEESEESGSEEESEEV
74280|7280|14|0|EENESSGEEEEEEV
74283|7283|16|0|SEESEEEGSSEESEEV
74290|7290|14|2|ENESSNGSSEEEEV
74293|7293|14|2|NNNSSNGSSEEEEV
74298|7298|16|1|EEEEEEEGEEESSSSV
74352|7352|16|0|EEEEEESGSEEEEEEV
74375|7375|16|0|ESSESSEGESSESSEV
74377|7377|20|1|ESEESSEESGESEESSEESV
74378|7378|16|1|ESEESESGESESEESV
74379|7379|16|1|ESSEESSGESSEESSV
74386|7386|14|0|EESSEEGEESSEEV
74390|7390|16|4|EESESSSGSSSESEEV
74393|7393|14|2|EESSSSGSSSSEEV
74398|7398|20|1|ESSEEEESSGESSEEEESSV
74399|7399|16|1|ESEEEESGESEEEESV
74490|7490|16|2|EESESSSGSSSESEEV
74669|7669|16|1|EEEEEEEGEESSSSSV
```

La numeración de pines sigue el DIP estándar. Para el comportamiento lógico de cada pin consultar la hoja de datos del 74LS correspondiente; los tipos E/S de arriba son lo que el programa realmente usa.

Pines útiles (hoja de datos, coinciden con el catálogo):
- **74LS90 (7090)**: 1 CKB, 2 R0(1), 3 R0(2), 5 Vcc, 6 R9(1), 7 R9(2), 8 QC, 9 QB, 10 GND, 11 QD, 12 QA, 14 CKA. Cuenta en el flanco de bajada. Década BCD: QA → CKB, reloj a CKA, R0 y R9 a GND.
- **74LS47 (7047)**: 1 B, 2 C, 3 LT, 4 BI/RBO, 5 RBI, 6 D, 7 A, 8 GND, 9 e, 10 d, 11 c, 12 b, 13 a, 14 g, 15 f, 16 Vcc.

## 5. Geometría (px, relativa a la esquina (Ex, Ey) del tablero)

Un agujero acepta cualquier punto dentro de ±4 px de su centro. Los extremos de cable y la posición de chips se resuelven **por coordenadas**, no por índices. ✓ = confirmado con archivo real o en ejecución.

- **Protoboard** ✓ (877x276, tipo 0, 132 nodos). Paso 13 px.
  - R1 tira superior ✓: columnas a=0..63, filas b=0..4, centro `(Ex+27+13a, Ey+66+13b)`. La fila 4 es la pegada al canal central. Nodo = columna a.
  - R2 tira inferior ✓: centro `(Ex+27+13a, Ey+157+13b)`, fila 0 pegada al canal. Nodo = 64+a.
  - R3 riel superior ✓: a=0..59, b=0..1, centro `(Ex+53+13a, Ey+14+13b)`. Cada fila es un solo nodo (128+b).
  - R4 riel inferior ✓: centro `(Ex+53+13a, Ey+248+13b)`. Nodo 130+b.
- **Chip DIP de n pines** ✓ (ejecutado): **el chip se coloca por el agujero R1 fila 4 columna a, que corresponde al pin n** (esquina superior izquierda). Pines **n/2+1..n van en la tira superior R1** (pin n en la columna a, pin p en la columna `a+(n-p)`, fila 4) y pines **1..n/2 van en la tira inferior R2** (pin p en la columna `a+p-1`, fila 0; el pin 1 queda justo debajo del pin n). Ejemplo 14 pines con a=0: pin 14 R1 col 0, pin 8 R1 col 6, pin 1 R2 col 0, pin 7 R2 col 6. Requiere a + n/2 ≤ 64. Ancho de imagen 91, 104, 117, 130 o 156 px (n = 14, 16, 18, 20, 24) por 41 de alto. Dejar al menos una columna libre entre chips contiguos.
- **Interruptores y Pulsadores** ✓ (206x81, tipos 1 y 2): 8 unidades c=0..7, 3 agujeros por unidad (r=0..2, mismo nodo, es la salida): `(Ex+56+19c, Ey+11+13r)`. Vcc en `(Ex+15, Ey+11)`, GND en `(Ex+15, Ey+69)`. En ejecución, el pulsador 0 funciona como reloj para un 74LS90.
- **Fuente DC** ✓ (77x128, tipo 4): x = Ex+61. Superiores +5 V: `(Ex+61, Ey+14+13r)`, r=0..3. Inferiores GND: `(Ex+61, Ey+74+13r)`, r=0..3. Los 4 de cada grupo son un mismo nodo.
- **LEDs** ✓ (203x58, tipo 3): LED c=0..7 en `(Ex+46+20c, Ey+44)`. GND en `(Ex+11, Ey+37)`.
- **Siete segmentos** ✓ (449x130, tipo 6, 33 nodos, **4 displays x 8 puertos**): puerto `c = 8*d + s` en `(Ex+37+13c, Ey+123)`, con d = 0..3 (de izquierda a derecha) y s = 0..7 = a, b, c, d, e, f, g, punto. **La terminal VCC `(Ex+16, Ey+27)` va a +5 V** (fuente DC, tipo V; ánodo común). Cada segmento se enciende cuando su puerto vale 0. Ejemplo comprobado: centenas en display 0, decenas en 1, unidades en 2, cada 74LS47 con a..g a los puertos s=0..6.
- **Temporizador** ✓ (206x81, tipo 5): salida c=0..3 (10 Hz, 5 Hz, 2 Hz, 1 Hz) en `(Ex+59+38c, Ey+11+13r)`, r=0..2 (mismo nodo, usar un r distinto por cada cable). Vcc `(Ex+15, Ey+11)`, GND `(Ex+15, Ey+69)`.
- **No descifrado**: PLA con contenido (tipo 8).

## 6. Formato del archivo `.txt` (texto, espacios en blanco indiferentes al leer)

```
Version 0.9.7
<N tableros>
 <tipo> <Ex> <Ey> <ancho> <alto> <base_nodos> <id>      (N líneas)
 <temporizador_visible 0|1>
<N cables>
 <color> <grosor> x0 y0 x1 y1 x2 y2 x3 y3 x4 y4 x5 y5 0 <idA> 0 <idB>   (N líneas)
<N componentes>
 <codigo> <etiqueta 0|1> <pines> <ux> <uy> <dx> <dy> <cx> <cy> <id_protoboard>   (N líneas)
```

Ejemplo real (archivo con pulsadores y chips insertados, recortado):

```
Version 0.9.7
4
 4 10 175 77 128 0 1
 5 80 400 206 81 2 2
 0 110 110 877 276 8 3
 2 76 423 206 81 140 4
 0
14
 16711680 5 215 176 215 176 215 176 215 137 215 137 215 137 0 3 0 3
 ...
4
 7011 1 14 209 228 5 0 0 0 3
 7008 1 14 339 228 5 0 0 0 3
 7107 1 14 456 228 5 0 0 0 3
 7083 1 16 560 228 5 0 0 0 3
```

- **Tablero**: tipo 0 Protoboard, 1 Interruptores, 2 Pulsadores, 3 Leds, 4 Fuente DC, 5 Temporizador, 6 Siete segmentos, 8 PLA. **Las dos primeras líneas son siempre** `4 10 175 77 128 0 1` (fuente DC) y `5 80 400 206 81 2 2` (temporizador). Los tableros agregados siguen con id 3, 4, … `base_nodos` = suma acumulada de nodos de los tableros anteriores (132 protoboard, 10 interruptores, 10 pulsadores, 9 LEDs, 2 fuente, 6 temporizador, 33 siete segmentos, 0 PLA); el programa lo recalcula al leer. Posiciones usadas con éxito: protoboard (110,110), siete segmentos (1032,34), pulsadores (300,400), LEDs (101,27).
- **Temporizador visible**: línea con 0 o 1 justo después de los tableros. Con 1 el tablero aparece en (80,400) y el temporizador avanza; con 0 está oculto y no avanza.
- **Cable**: `color` es COLORREF decimal 0x00BBGGRR (rojo = 255, azul = 16711680, negro = 0; el programa usa azul por defecto), grosor 5. Seis puntos: p0 = extremo A, p5 = extremo B. Los cuatro intermedios son solo dibujo (cualquier ruta ortogonal vale). Los dos extremos deben caer en un agujero (si uno no cae en ninguno, el cable se dibuja pero no conecta, sin aviso). Los 4 números finales son `0 idA 0 idB`, con `idA`/`idB` los ids de los tableros donde terminan A y B.
- **Componente (chip)**: `ux,uy` esquina de la imagen, `dx,dy` = (5, 0), `cx,cy`: escribir 0. Chip suelto: `id_protoboard` = 0 y posición (20,50). **Chip insertado** ✓: `id_protoboard` = id de la protoboard, `ux = hx - 6`, `uy = hy`, con (hx, hy) el centro del agujero R1 fila 4 columna a (el del pin n).
- Al leer, el programa reconstruye las conexiones solo con las coordenadas de los extremos de cable y la posición de los chips. Una lista vacía se escribe como `0`.

## 7. Generador y verificador (Python 3)

```python
from dataclasses import dataclass, field
TIPOS = {0:("Protoboard",877,276,132),1:("Interruptores",206,81,10),2:("Pulsadores",206,81,10),
         3:("Leds",203,58,9),4:("FuenteDC",77,128,2),5:("Temporizador",206,81,6),6:("SieteSeg",449,130,33),8:("PLA",0,0,0)}
def hit(v,o,p,n):
    r=v-o
    if r<0 or r//p>=n or r%p>8: return None
    return r//p
def pb_hole(ex,ey,reg,a,b):
    return {1:(ex+27+13*a,ey+66+13*b),2:(ex+27+13*a,ey+157+13*b),3:(ex+53+13*a,ey+14+13*b),4:(ex+53+13*a,ey+248+13*b)}[reg]
def pb_port_at(ex,ey,x,y):
    for reg,ox,oy,na,nb in ((1,23,62,64,5),(2,23,153,64,5),(3,49,10,60,2),(4,49,244,60,2)):
        a=hit(x,ex+ox,13,na); b=hit(y,ey+oy,13,nb)
        if a is not None and b is not None: return {1:a,2:64+a,3:128+b,4:130+b}[reg]
sw_hole=lambda ex,ey,c,r:(ex+56+19*c,ey+11+13*r)
SW_VCC=lambda ex,ey:(ex+15,ey+11); SW_GND=lambda ex,ey:(ex+15,ey+69)
led_hole=lambda ex,ey,c:(ex+46+20*c,ey+44); LED_GND=lambda ex,ey:(ex+11,ey+37)
DC_VCC=lambda ex,ey,r:(ex+61,ey+14+13*r); DC_GND=lambda ex,ey,r:(ex+61,ey+74+13*r)
TM_HOLE=lambda ex,ey,c,r:(ex+59+38*c,ey+11+13*r)
SEG_VCC=lambda ex,ey:(ex+16,ey+27)
SEG_PORT=lambda ex,ey,disp,s:(ex+37+13*(8*disp+s),ey+123)   # s: 0..7 = a,b,c,d,e,f,g,punto

def pin_col(a,n,p):
    """Pin p (1..n) de un DIP de n pines con el chip colocado en la columna a -> (region, columna).
    region 2 = tira inferior (pines 1..n/2), region 1 = tira superior (pines n/2+1..n)."""
    return (2,a+p-1) if p<=n//2 else (1,a+(n-p))
def libre(pb,reg,col,k):
    """k-esimo agujero libre (0..3) de la columna: usar uno distinto por cada cable."""
    return pb_hole(pb["ex"],pb["ey"],reg,col,(3-k) if reg==1 else (1+k))

def port_at(t,x,y):
    tipo,ex,ey,tid=t["tipo"],t["ex"],t["ey"],t["id"]
    near=lambda p:abs(x-p[0])<=4 and abs(y-p[1])<=4
    if tipo==0:
        n=pb_port_at(ex,ey,x,y); return None if n is None else (tid,n)
    if tipo in (1,2,5):
        c=hit(x,ex+(52 if tipo!=5 else 55),19 if tipo!=5 else 38,8 if tipo!=5 else 4); r=hit(y,ey+7,13,3)
        if c is not None and r is not None: return (tid,c)
        if near(SW_VCC(ex,ey)): return (tid,"V")
        if near(SW_GND(ex,ey)): return (tid,"G")
    if tipo==3:
        c=hit(x,ex+42,20,8)
        if c is not None and hit(y,ey+40,13,1) is not None: return (tid,c)
        if near(LED_GND(ex,ey)): return (tid,"G")
    if tipo==4:
        for g,oy in (("V",10),("G",70)):
            if 0<=x-(ex+57)<=8 and 0<=y-(ey+oy)<=47 and (y-ey-oy)%13<=8: return (tid,g)
    if tipo==6:
        if near(SEG_VCC(ex,ey)): return (tid,"T")
        c=hit(x,ex+33,13,32)
        if c is not None and hit(y,ey+119,13,1) is not None: return (tid,c)

@dataclass
class Circuito:
    tableros:list=field(default_factory=list); timer_visible:int=0
    cables:list=field(default_factory=list); chips:list=field(default_factory=list)
    _id:int=1; _base:int=0
    def __post_init__(self):                       # dos tableros fijos de todo circuito nuevo
        self.dc=self.tablero(4,10,175); self.tm=self.tablero(5,80,400)
    def tablero(self,tipo,ex,ey):
        _,w,h,n=TIPOS[tipo]; t=dict(tipo=tipo,ex=ex,ey=ey,w=w,h=h,base=self._base,id=self._id)
        self._base+=n; self._id+=1; self.tableros.append(t); return t
    def _tab_en(self,p):
        return next((t for t in self.tableros if port_at(t,*p)),None)
    def cable(self,a,b,color=16711680,ancho=5):
        (ax,ay),(bx,by)=a,b; ta,tb=self._tab_en(a),self._tab_en(b)
        assert ta and tb, "extremo fuera de agujero: %s %s"%(a,b)
        self.cables.append(dict(color=color,ancho=ancho,pts=[ax,ay,ax,ay,bx,ay,bx,ay,bx,by,bx,by],ia=ta["id"],ib=tb["id"]))
    def chip(self,codigo,pines,pb=None,a=0):
        """pb=None: chip suelto en (20,50). Con pb y columna a: insertado; (hx,hy) = R1 fila 4 columna a (= pin n)."""
        if pb is None: ux,uy,pid=20,50,0
        else:
            hx,hy=pb_hole(pb["ex"],pb["ey"],1,a,4); ux,uy,pid=hx-6,hy,pb["id"]
        self.chips.append(dict(codigo=codigo,etiqueta=1,pines=pines,ux=ux,uy=uy,dx=5,dy=0,cx=0,cy=0,pb=pid))
    def texto(self):
        L=["Version 0.9.7",str(len(self.tableros))]
        L+=[" %d %d %d %d %d %d %d"%(t["tipo"],t["ex"],t["ey"],t["w"],t["h"],t["base"],t["id"]) for t in self.tableros]
        L+=[" %d"%self.timer_visible,str(len(self.cables))]
        L+=[" %d %d %s 0 %d 0 %d"%(c["color"],c["ancho"]," ".join(map(str,c["pts"])),c["ia"],c["ib"]) for c in self.cables]
        L.append(str(len(self.chips)))
        L+=[" %d %d %d %d %d %d %d %d %d %d"%(k["codigo"],k["etiqueta"],k["pines"],k["ux"],k["uy"],k["dx"],k["dy"],k["cx"],k["cy"],k["pb"]) for k in self.chips]
        return "\n".join(L)+"\n"

def netlist(txt):
    """Relee el texto como el programa; devuelve (chips, grupos_de_nodos_unidos_por_cables, problemas).
    Tambien avisa si dos cables comparten el mismo agujero (el programa solo admite uno)."""
    tok=txt.split(); assert tok[:2]==["Version","0.9.7"]; p=2; n=int(tok[p]); p+=1; tabs=[]
    for _ in range(n):
        tipo,ex,ey,w,h,base,tid=map(int,tok[p:p+7]); p+=7; tabs.append(dict(tipo=tipo,ex=ex,ey=ey,id=tid))
    p+=1; nc=int(tok[p]); p+=1; uf={}; prob=[]; usados={}
    def find(x):
        uf.setdefault(x,x)
        while uf[x]!=x: uf[x]=uf[uf[x]]; x=uf[x]
        return x
    def agujero(t,x,y):   # identificador exacto del agujero (no solo del nodo)
        return (t["id"],) + ((x-t["ex"])//13*0+0,) if False else (t["id"],x,y)
    for i in range(nc):
        v=list(map(int,tok[p:p+18])); p+=18; pts=v[2:14]; ends=[]
        for e in ((pts[0],pts[1]),(pts[10],pts[11])):
            h=next((q for t in tabs if (q:=port_at(t,*e))),None)
            if h is None: prob.append("cable %d: extremo %s fuera de todo agujero"%(i,e))
            else:
                t=next(t for t in tabs if port_at(t,*e)); k=(t["id"],)+tuple(e)
                if k in usados: prob.append("cable %d: agujero %s ya usado por el cable %d"%(i,e,usados[k]))
                usados[k]=i
            ends.append(h)
        if all(ends): uf[find(ends[0])]=find(ends[1])
    nk=int(tok[p]); p+=1; chips=[]
    for _ in range(nk):
        cod,et,pin,ux,uy,dx,dy,cx,cy,pid=map(int,tok[p:p+10]); p+=10
        if pid==0: chips.append((cod,"suelto",None,pin)); continue
        pb=next(t for t in tabs if t["id"]==pid and t["tipo"]==0)
        nodo=pb_port_at(pb["ex"],pb["ey"],ux+dx,uy+dy)
        if nodo is None or nodo>=64 or hit(uy+dy,pb["ey"]+62,13,5)!=4 or nodo+pin//2>64: prob.append("chip %d no insertable"%cod)
        else: chips.append((cod,pid,nodo,pin))
    g={}
    for k in list(uf): g.setdefault(find(k),[]).append(k)
    return chips,[sorted(map(str,x)) for x in g.values()],prob
```

Al comprobar un diseño, además de `netlist()`, conviene **simular el circuito en Python** con el mapa `pin_col` (nodo de pin p = columna `a+p-1` de R2 si p ≤ n/2, si no columna `a+(n-p)` de R1) para confirmar la lógica antes de entregar.

Ejemplo (NAND 74LS00 con dos interruptores y un LED; chip en la columna A=20):

```python
c=Circuito(); pb=c.tablero(0,300,60); sw=c.tablero(1,10,350); led=c.tablero(3,300,380)
A=20; c.chip(7000,14,pb,A); D=c.dc
H=lambda reg,a,b:pb_hole(pb["ex"],pb["ey"],reg,a,b)
c.cable(DC_VCC(D["ex"],D["ey"],0),SW_VCC(10,350)); c.cable(DC_GND(D["ex"],D["ey"],0),SW_GND(10,350))
c.cable(DC_GND(D["ex"],D["ey"],1),LED_GND(300,380))
c.cable(DC_VCC(D["ex"],D["ey"],1),H(3,0,0)); c.cable(DC_GND(D["ex"],D["ey"],2),H(3,0,1))   # rieles
c.cable(H(3,3,0),H(1,A,3))        # Vcc -> pin 14 (R1, columna A)
c.cable(H(3,9,1),H(2,A+6,1))      # GND -> pin 7 (R2, columna A+6)
c.cable(sw_hole(10,350,0,0),H(2,A,1)); c.cable(sw_hole(10,350,1,0),H(2,A+1,1))   # SW0->pin1, SW1->pin2 (R2)
c.cable(H(2,A+2,1),led_hole(300,380,0))                                          # pin3 -> LED0
open("nand.txt","w").write(c.texto()); print(netlist(c.texto()))
```

## 8. Receta probada: contador decimal de 3 dígitos (000–999)

Probado en el programa real, con pulsador y con temporizador como reloj (ambos cuentan bien). Tres bloques 74LS90 + 74LS47, chips en las columnas a = 0 (7090), 8 (7047), 18 (7090), 26 (7047), 36 (7090), 44 (7047); fuente DC; protoboard en (110,110); siete segmentos en (1032,34); pulsadores en (300,400).

- Alimentación: DC +5 → riel R3 fila 0; DC GND → riel R3 fila 1; un cable de riel por cada pin Vcc/GND/nivel fijo (un agujero de riel distinto por cable); DC +5 → terminal VCC del siete segmentos (`SEG_VCC`).
- Cada 74LS90: Vcc pin 5, GND pin 10, R0(1),R0(2),R9(1),R9(2) (pines 2,3,6,7) a GND; QA (12) → CKB (1).
- Cada 74LS47: Vcc 16, GND 8, LT (3) y RBI (5) a +5 V; BI/RBO (4) sin conectar; A,B,C,D ← QA(12), QB(9), QC(8), QD(11) del 90 de su dígito; salidas a(13) b(12) c(11) d(10) e(9) f(15) g(14) → `SEG_PORT(disp, 0..6)`.
- Cascada: QD (11) de unidades → CKA (14) de decenas; QD de decenas → CKA de centenas.
- Reloj: pulsador 0 `sw_hole(Ex,Ey,0,0)` → CKA (14) de unidades (alimentar el tablero de pulsadores con Vcc y GND); o temporizador: `TM_HOLE(80,400,0,0)` (10 Hz) → CKA de unidades, `timer_visible=1`, alimentar el temporizador (DC +5 → `SW_VCC(80,400)`, DC GND → `SW_GND(80,400)`). Un solo cable por agujero de salida: si hace falta la misma señal en dos sitios (p. ej. a un LED), usar otro agujero r de la misma unidad.
- Unidades en el display 2, decenas en 1, centenas en 0 (izquierda a derecha).

## 9. Cómo trabajar con este skill

1. **Entender qué se pide**: explicar el programa, diseñar un circuito o producir el `.txt`.
2. **Diseñar primero**: lista de chips con su columna `a` (sin solaparse), tabla de cables `origen → destino` con la alimentación explícita (Vcc/GND a cada tablero activo y a cada chip), un agujero distinto por cable.
3. **Generar el archivo** con el generador, ejecutar `netlist()` y, si es lógica no trivial, simular en Python antes de entregar.
4. **Probar por etapas** si algo no funciona: (a) display/LEDs con GND directo, (b) un solo chip con prueba de lámparas, (c) circuito completo. Recordar al usuario encender la fuente DC después de abrir el archivo.
5. **Decir con claridad** qué está verificado en ejecución y qué no (PLA, chips distintos de 7490/7447).
6. Para tableros no descifrados (PLA con contenido) no inventar coordenadas: pedir un archivo de muestra o dar los pasos manuales.
7. Alternativa siempre válida: dar el procedimiento manual.

## 10. Limitaciones conocidas

- No verificados en ejecución: PLA con contenido, fidelidad lógica de chips distintos de 7490/7447, límite exacto de iteraciones, comportamiento del pulsador (momentáneo vs. fijo).
- Si una columna de chip necesita más de 4 cables, usar un riel o columna adicional unida por cable.
- La interfaz está en español; los mensajes de error útiles son los de la sección 2.