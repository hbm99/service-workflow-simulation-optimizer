# Optimización de la ganancia de un supermercado

## Descripción del problema
El problema consiste en optimizar la distribución de los productos en los estantes de un supermercado con el objetivo de maximizar la ganancia diaria. 

## Descripción de la solución:
Para la optimización se implementó la metaheurística **búsqueda tabú**. Se hizo una búsqueda de cuáles metaheurísticas se utilizaban para este tipo de problemas y se seleccionó esta por sus buenos resultados en problemas altamente combinatorios. Se parte de una solución inicial que consiste en una distribución aleatoria de los productos en los estantes y esta se va modificando a través de una serie de intercambios de posiciones. De esta manera se prioriza la explotación sobre la exploración. La función de evaluación de la metaheurística es la simulación, que da a partir de la distribución de productos escogida la ganancia generada. 


## Simulación de la tienda
Para modelar el problema se definió un ambiente de tienda que consiste en un mapa cuadrado que representa la tienda, una serie de estantes, cajeros y productos disponibles en el almacén de la tienda. Sobre este ambiente se simula el desarrollo de un día en el supermercado desde la llegada de clientes a la tienda, su comportamiento dentro de ella y la ganancia que genera la tienda. 
Para la implementación de la simulación se utilizó la biblioteca `simpy` de Python. Esta biblioteca brinda facilidades para la simulación de eventos discretos, el trabajo con recursos finitos y la concurrencia. Específicamente se utilizó el módulo `rt` de Simpy que permite sincronizar el paso del tiempo de la simulación con el tiempo real.
Como agentes de la simulación se definieron tres tipos de clientes: el cliente apurado, el cliente consumista y el cliente regular. La selección del tipo de cliente se realiza con una variable aleatoria con distribución uniforme. Los agentes utilizan la información del ambiente en la toma de sus decisiones y tienen influencia sobre él. El comportamiento de cada agente se implementó utilizando los algoritmos de inteligencia artificial que más se ajustaban a las características del cliente.

### Descripción de los agentes
Cada cliente tiene una lista de compras, donde aparecen productos que pueden o no estar disponibles en la tienda, un carrito de productos donde va añadiendo los productos que coge en la tienda y un índice de percepción de personas en la tienda al cual se le dará sentido más adelante.

#### Cliente apurado:
**¿Qué se espera de un cliente apurado?**

Un cliente apurado quiere resolver rápido lo que está buscando en la tienda, no está dispuesto a hacer cola para obtener algún producto y se incomoda cuando hay muchas personas en la tienda.

**Planificación al llegar a la tienda:**

La planificación de este cliente es en función de la cantidad de personas que hay en las secciones de las que necesita tomar un artículo en el momento en que se planifica (cuando llega a la tienda). Al trazar el plan, este decide pasar por las secciones que necesita en orden ascendente de la cantidad de clientes, es decir, las secciones que sabe que tienen menos clientes las visita primero dando tiempo a que se liberen un poco aquellas que están más congestionadaas. 

**Obtención de productos:**

El cliente decide tomar o no un objeto en función de la cantidad de personas que hay en la sección en la que está. Si considera que hay muchas personas decide irse sin tomar el producto. 

**Recorrido en la tienda:**

El camino del cliente apresurado entre secciones de la tienda se realiza con una búsqueda A*, para esto se define el costo de ir de una posición del mapa a su adyacente con costo 1 ( función g ), es decir, tienen costo uniforme los movimientos; y la heurística ( función h) que se define es la distancia euclidiana o distancia entre dos puntos, que representa la distancia relajada desde la posición en que se encuentra hasta su siguiente objetivo, obviando cualquier cantidad de obstáculos posibles que se encuentran en el mapa (cajeros o estantes). 



#### Cliente consumista:
**¿Qué se espera de un cliente consumista?**

A un cliente consumista le gusta comprar, busca en la tienda lo que necesita pero se embulla fácilmente con otros productos que encuentra en el camino. A este tipo de cliente le gusta explorar la tienda, ver las opciones que hay y no se preocupa mucho por la cantidad de personas que hay a su alrededor o por si tiene que hacer alguna cola. 

**Planificación al llegar a la tienda:**
Pasa por todas las secciones de la tienda comprando aquellos productos que estén en su lista de compras y elige para comprar otros productos con cierta probabilidad. 

**Obtención de productos:**
A la hora de obtener un producto espera pacientemente el tiempo que corresponda según la cantidad de personas que hay en esa sección de la tienda. 

**Recorrido en la tienda:**
Realiza los movimientos entre sección y sección con el algorirmo A* de forma similar al cliente apurado. 

#### Cliente regular:
**¿Qué se espera de un cliente regular?**

El cliente regular pretende ser un cliente promedio que tiene una lista de los productos que desea comprar y va buscándolos uno por uno, con el objetivo de cumplir con su lista. No se preocupa mucho por el resto de los productos ni por la cantidad de personas que hay en la tienda. 

**Planificación al llegar a la tienda:**

Para simular en comportamiento planificado del cliente regular se utilizó **Planificación**, una herramienta de la Inteligencia Artificial, que permite dado un dominio, un inicio, un objetivo y un conjunto de acciones válidas, formular un problema de búsqueda que al resolverse devuelve una especie de planificación , o sea, un sistema de pasos concretos para cumplir el objetivo.

**Formulación general del problema:**

**Inicio**: El cliente está en la entrada de la tienda

**Objetivo**: El cliente compra todos los productos de su lista de compras

**Dominio**: Los productos, las secciones de la tienda, y la sección en que se encuentra cada producto

**Acciones:** Tomar un producto (`Take`) y Caminar (`Go`)

El árbol de búsqueda resultante se explora con **Breadth First Search** (`BFS`)

**Obtención de productos:**

A la hora de obtener un producto espera pacientemente el tiempo que corresponda según la cantidad de personas que hay en esa sección de la tienda.

**Recorrido en la tienda:**

Se decidió que este cliente se movería por la matriz que representa la tienda utilizando un **Depth First Search** (`DFS`), simulando así, el comportamiento de explorar a lo largo a través de los estantes.

### Modelo fuzzy para la obtención de propinas

El "problema de las propinas" se usa comúnmente para ilustrar el poder de los principios de la lógica difusa para generar un comportamiento complejo a partir de un sistema compacto e intuitivo.
Inspirado en ese problema se decidió utilizar lógica difusa para aproximar la propina que debía dejar el cliente al pagar en la caja, teniendo en cuenta si percibió la tienda más llena o vacía.

#### Formulación general del problema:

#### Antecedentes
**Universo:** ¿Había muchas personas en la tienda?

**Conjunto difuso:** pocas (few), cantidad aceptable (fair), muchas (lot)

#### Consecuencias
**Universo:** ¿Cuánto se debe dejar de propina del 0% al 25%?

**Conjunto difuso:** baja (low), media (medium), mucha (high)

#### Reglas
    -Si había pocas personas en la tienda entonces la propina debe ser alta
    
    -Si había una cantidad aceptable de personas en la tienda entonces la propina debe ser media
    
    -Si había muchas personas en la tienda entonces la propina debe ser baja

Se decidió que cada cliente tuviera una percepción personal de la cantidad total de clientes, teniendo en cuenta la personalidad anteriormente definida: El cliente regular percibe la cantidad real de personas que hay en la tienda, el cliente apurado percibe un 20 por ciento más de la cantidad de personas que hay en la tienda y el cliente consumista percibe un 10 por ciento menos de la cantidad de personas que hay en la tienda.

Cuando el cliente va a pagar al cajero, se calcula el por ciento de propina que debe dejar según el sistema difuso definido, y se halla la propina a partir de su gasto general en la tienda.

Se utilizó el módulo de python `skfuzzy` para facilitar la implementación de la lógica anteriormente definida.

## Resultados
Sobre una tienda con los siguientes parámetros:
- shop_size = 10
- num_cashiers = 2
- list_product = [Product('PIZZA', 10), Product('PAN', 5), Product('TOMATE', 3), Product('LECHUGA', 1), Product('JUGUETE', 20), Product('CERVEZA', 3), Product('CHOCOLATE', 2)]
- simulation_time = 60 * 60
- shelves_count= 4

Se realizaron cada vez más de 30 simulaciones para tener una percepción más realista del funcionamiento de la tienda. 

A continuación se muestran algunos resultados obtenidos. 

| Distribución de productos  | Ganancia |
| ------------- | ------------- |
| [2, 4, 5, 4]  |788|
| [3, 3, 6, 1]  |185|
| [3, 0, 1, 1]  |391|
| [6, 4, 6, 4]  |764|
| [3, 1, 4, 1]  |689|
| [6, 1, 4, 1]  |704|
| [6, 4, 2, 6]  |610|
| [1, 6, 1, 1]  |200|
| [3, 0, 1, 2]  |458|
| [1, 0, 3, 1]  |437|
| [3, 6, 1, 6]  |188|
| [6, 1, 0, 0]  |441|
| [2, 6, 2, 3]  |143|
| [3, 5, 1, 1]  |230|
| [3, 3, 3, 1]  |165|
| [3, 3, 6, 5]  |132|
| [3, 6, 4, 4]  |651|
| [0, 0, 0, 6]  |386|
| [6, 0, 1, 2]  |469|
| [2, 0, 5, 2]  |405|
| [3, 2, 2, 3]  |120|
| [5, 1, 2, 1]  |278|
| [1, 6, 0, 1]  |457|
| [3, 0, 1, 0]  |475|
| [6, 6, 3, 3]  |81|
| [2, 5, 1, 0]  |419|
| [3, 0, 4, 2]  |827|
| [3, 1, 2, 6]  |231|
| [3, 1, 2, 5]  |223|