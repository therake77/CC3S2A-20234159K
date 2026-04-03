import re
from tokenize import group
from typing import Callable

#Clase que abstrae una ruta dada, por ejemplo /users/:id
#Provee de operaciones para la construcción de esta y la resolución de la ruta con parámetros dados
class Route:
    #Los nombres que aparecen en una ruta. Por ejemplo /users/:id se descompone en ['users',':id']
    labels:list
    #Requerimos mantener registro de los argumentos encontrados. Nota: No se permite argumentos repetidos, como /users/:id/profile/:id (inválido)
    args:set[str]
    #La resolución de rutas se hará usando un regex
    regex:re.Pattern

    def __init__(self,routeStr:str) -> None:
        self.args = set()
        self.labels = routeStr.split("/")
        #Dado que una ruta empieza siempre con '/', entonces el primer elemento que retorna split('/') es el caracter vacío
        self.labels.pop(0)
        #Y si la ruta es simplemente "/", el caracter final también es vacío
        if(self.labels[len(self.labels)-1] == ""): self.labels.pop(len(self.labels)-1)
        #Si la ruta es únicamente "/", entonces ya se sabe el regex
        if(len(self.labels) == 0):
            self.regex = re.compile(r"\/")
        #Caso contrario hay que construir el regex a partir de `labels`
        else:
            string = ""
            for label in self.labels:
                #Si la etiqueta encontrada empieza con ':' claramente es un parámetro
                if(label.startswith(':')):
                    argName = label.lstrip(':')
                    if(argName in self.args): raise SyntaxError(f"Duplicated name parameters are not allowed: {argName}")
                    self.args.add(argName)
                    string += r"\/(?P<"+argName+r">[^\/]+)"
                else:
                    string += r"\/"+label
            self.regex = re.compile(string)

    def match(self,string:str) -> tuple[bool,dict[str,str]]:
        #Se realiza el match con el regex
        matches = self.regex.fullmatch(string)
        if(not matches):
            #Retorna falso si no coincide
            return (False,{})
        else:
            #Retorna los parámetros y sus valores en forma de diccionario
            return (True, matches.groupdict())

stateRegex = re.compile(r"^([a-zA-Z0-9]+)(?: {([a-zA-Z0-9]+(?:,[a-zA-Z0-9]+)*)}){0,1}$")
#Abstrae un 'Estado' (el destino de una ruta, por así decirlo)
class State:
    #Todo estado tiene su nombre
    name:str
    #Y una lista de parámetros
    args:set[str]
    def __init__(self,stateStr:str) -> None:
        self.args = set()
        matches = stateRegex.fullmatch(stateStr)
        if(not matches):
            raise SyntaxError(f"Invalid state string: {stateStr}")
        groups = matches.groups()
        self.name = groups[0]
        if(groups[1]):
            args = groups[1].split(',')
            self.args = set(args)



inputRegex = re.compile(r"^(\/|(?:\/[a-zA-Z0-9]+(?:\/:[a-zA-Z0-9]+){0,1})+) ([a-zA-Z0-9]+(?: {[a-zA-Z0-9]+(?:,[a-zA-Z0-9]+)*}){0,1})$")
transitionRegex = re.compile(r"^(\/|(?:\/[a-zA-Z0-9]+)+)$")

#Esta función captura los datos desde stdin (o a donde apunte input())
#Uso distintos regexes para comprobar que son válidos
def captureInputs() -> tuple[dict[str,str],list[str]]:
    a = int(input("Numero de rutas: "))
    routeMap = {}
    for _ in range(a):
        line = str(input("(/ruta estado): "))
        matches = inputRegex.fullmatch(line) 
        if(not matches):
            raise SyntaxError(f"Input '{line}' is not valid")
        else:
            routeMap[matches.group(1)] = matches.group(2)

    b = int(input("Numero de pruebas: "))
    transitions = []
    for _ in range(b):
        line = input("(/ruta): ")
        matches = transitionRegex.fullmatch(line)
        transitions.append(matches.group(0))

    return (routeMap,transitions)
#Esta función se encarga de obtener los datos desde un archivo con nombre "inputA.txt"
#También usa regexes para comprobar la validez de los datos
def readFromFile() -> tuple[dict[str,str],list[str]]:
    routeMap = {}
    transitions = []
    with open("inputA.txt","r") as file:
        a = int(file.readline().rstrip('\n'))
        for _ in range(a):
            line = file.readline().rstrip('\n')
            matches = inputRegex.fullmatch(line) 
            if(not matches):
                raise SyntaxError(f"Input '{line}' is not valid")
            else:
                routeMap[matches.group(1)] = matches.group(2)
        b = int(file.readline())
        for _ in range(b):
            line = file.readline().rstrip('\n')
            matches = transitionRegex.fullmatch(line)
            if(not matches):
                raise SyntaxError(f"Invalid transition string: {line}")
            transitions.append(matches.group(0))
        
    return (routeMap,transitions)    

#Main
if __name__ == "__main__":
    notValidInput = True    #Para continuar pidiendo entradas
    stringRouteMap = {}     #Mapa ruta:estado pero en strings
    transitions = []        #Transiciones
    captureMode:Callable[[],tuple[dict[str,str],list[str]]] = captureInputs

    #Deseas ingresar datos desde stdin o el archivo?
    option = str(input("Load from file?(should be named inputA.txt) [Y/n]: "))
    if(option.capitalize() == "Y"): #Cualquier letra distinta a 'y' o 'Y' se considera NO
        captureMode = readFromFile

    #Captura de datos
    while(notValidInput):
        try:
            stringRouteMap,transitions = captureMode()
            notValidInput = False
        except Exception as e:
            print(f"Problem detected: {e}")
            input("Continue? [press any key]")
    
    routeMap:dict[Route,State] = {}
    for k,v in stringRouteMap.items():
        try:
            #Primero construyamos los objetos
            r = Route(k)
            s = State(v)
            #No se permite que los nombres de los parámetros varían entre la declaración
            # de ruta y de estado. Deben ser los mismos, 
            if(r.args != s.args):
                raise SyntaxError(f"Name parameters don't match: {list(r.args)}, {list(s.args)}")
            routeMap[r] = s
        except Exception as e:
            print("Fatal error parsing routes and states")
            raise e
    
    #Empieza las resoluciones de rutas
    for t in transitions:
        validRoute = False
        for route in routeMap.keys():
            isMatch, args = route.match(t)
            if(not isMatch):
                continue
            else:
                #Si ha coincidido, hay que manejar si tiene argumentos la ruta, o no
                #args es un diccionario de pares 'nombreParametro:valorEncontrado'
                if(len(args) > 0):
                    print(f"{routeMap[route].name}",end=" ")
                    for arg in route.args:
                        print(f"{arg}:{args[arg]}",end=" ")
                    validRoute = True
                    print("")
                else:
                    print(f"{routeMap[route].name}")
                    validRoute = True
                break
        #Si no hubo ningún match, error
        if(not validRoute):
            print(f"{t}: NotFoundError 404")
    