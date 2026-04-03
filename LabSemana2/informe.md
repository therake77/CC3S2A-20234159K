## Laboratorio 2
### Pregunta 1
#### Introducción
`problema1.py` resuelve rutas que consisten de la forma `\name1[\:param1]\name2[\:param2]...` a estados especificados con formato `stateName [{param1[,param2,...]}]`. Para ello, utiliza un enfoque basado en expresiones regulares para validar entradas (declaración de rutas y estados), así como también para resolver rutas dadas a estados.
#### Estructura
El programa a grandes rasgos está compuesto de  
- La clase `Route`:
- La clase `State`
- Dos funciones para ingresar datos (desde la terminal o un archivo)
- La función principal
```python
class Route: ...
class State: ...
def captureInputs() -> tuple[dict[str,str],list[str]] : ...
def readFromFile() -> tuple[dict[str,str],list[str]] : ...
...
```  
**`Route`**: Clase que representa una ruta literal. Consiste de dos métodos  
- `__init__`: Toma una ruta literal y realiza una serie de operaciones sobre ella:  
    - Primero divide la ruta en sus segmentos: las etiquetas separadas por el caracter `\`
    - Luego procede a construir una expresión regular que será guardada en la clase como sigue:
        - Si la etiqueta no comienza con `:` es simplemente una etiqueta más y se la agrega de forma literal a la expresión regular, además de guardarse el nombre del parámetro en la variable `Route.args`
        - Caso contrario es un parámetro a capturar, cuya expresión regular es `(?:P<name>[^\/])`
- `match`: Toma una cadena y la compara con la expresión regular de la clase:
    - Si coinciden, entonces se devuelve un diccionario que consiste en pares cuyas llaves son el nombre correspondiente de parámetro, y el valor capturado  
      
**`State`**: Clase que encapsula un estado y se encarga de su correcta interpretación. Sólo tiene como método su constructor:
- `__init__`: Toma un literal de forma `name {param1,...}`, guarda el nombre `name` como nombre del estado y almacena los nombres de los parámetros `param1,param2,...` en un conjunto. De no haber, el conjunto simplemente es vacío.
