import re
from typing import Callable

regex1 = re.compile(r"^[ ]*([0-9]+)[ ]+([0-9]+)[ ]+([0-9]+)[ ]*$")
regex2 = re.compile(r"^[ ]*([0-9]+)[ ]+([0-9]+)[ ]*$")


#Ingresar valores via stdin
def captureInputs()  -> tuple[dict[int, set[int]], dict[int, set[int]]]:
    #Usamos un regex para obtener los números
    numbers = input("Ingrese S,N,M (S N M): ")
    matches = regex1.fullmatch(numbers)
    if(not matches): raise SyntaxError(f"No valid numbers: {numbers}")
    #De tupla de strings a ints
    n,m,s = map(int , matches.groups())
    if(n < 1 or n > 1000 or m < 1 or m > 1000 or s < 1 or s > 1000): SyntaxError(f"Numbers out of bounds: {n} {m} {s}")
    #Mapa socio -> terminal. Notar que se mantiene un set para evitar valores duplicados 
    partnerTerminalMap:dict[int,set[int]] = {}
    asignedTerminalsPool = set()
    #Más lógica de ingreso de datos
    for _ in range(m):
        line = input("(t p): ")
        matches = regex2.fullmatch(line)
        if(not matches): raise SyntaxError(f"No valid line: {line}")
        p,t = map(int , matches.groups())
        if(p < 1 or p > n): raise SyntaxError(f"Partner ID out of bounds: {p}")
        if(t < 1 or t > 10000): raise SyntaxError(f"Terminal ID out of bounds: {t}")
        
        if(t in asignedTerminalsPool): raise SyntaxError(f"Terminal ID is already in used")
        asignedTerminalsPool.add(t)    
        if(not partnerTerminalMap.get(p)):
            partnerTerminalMap[p] = {t}
        else:
            partnerTerminalMap[p].add(t)
    #Mapa terminal -> cliente. Notar que se mantiene un set para evitar valores duplicados
    terminalClientMap:dict[int,set[int]] = {}
    #Más lógica de ingreso de datos
    for _ in range(s):
        line = input("(c t): ")
        matches = regex2.fullmatch(line)
        if(not matches): raise SyntaxError
        c,t = map(int , matches.groups())
        if(not terminalClientMap.get(t)): terminalClientMap[t] = {c}
        else: terminalClientMap[t].add(c)
    
    return (partnerTerminalMap,terminalClientMap)

#Mismo que captureInputs pero para leer desde un archivo
def readFromFile() -> tuple[dict[int, set[int]], dict[int, set[int]]]:
    partnerTerminalMap:dict[int,set[int]] = {}
    terminalClientMap:dict[int,set[int]] = {}
    #Abrir el archivo
    with open("inputB.txt","r") as file:
        #Obtener los tres números
        numbers = file.readline().rstrip('\n')
        matches = regex1.fullmatch(numbers)
        if(not matches): raise SyntaxError(f"No valid numbers: {numbers}")
        #Cast de str a int de los tres números
        n,m,s = map(int , matches.groups())
        if(n < 1 or n > 1000 or m < 1 or m > 1000 or s < 1 or s > 1000): SyntaxError(f"Numbers out of bounds: {n} {m} {s}")
        #Usado para saber si una terminal ya se asignó (dado que son únicas incluso entre socios)
        asignedTerminalsPool = set()
        #Leer datos de socios - terminales
        for _ in range(m):
            line = file.readline().rstrip('\n')
            matches = regex2.fullmatch(line)
            if(not matches): raise SyntaxError(f"Error parsing string {line}")
            p,t = map(int , matches.groups())
            if(p < 1 or p > n): raise SyntaxError(f"Out of bounds or invalid int cast: {p}")
            if(t < 1 or t > 10000): raise SyntaxError(f"Terminal ID out of bounds: {t}")

            if(t in asignedTerminalsPool): raise SyntaxError(f"Terminal ID is already in used")
            asignedTerminalsPool.add(t)
            
            if(not partnerTerminalMap.get(p)):
                partnerTerminalMap[p] = {t}
            else:
                partnerTerminalMap[p].add(t)
        #Leer datos de terminales - clientes
        for _ in range(s):
            line = file.readline().rstrip('\n')
            matches = regex2.fullmatch(line)
            if(not matches): raise SyntaxError(f"Error parsing line: {line}")
            c,t = map(int , matches.groups())
            if(not terminalClientMap.get(t)): terminalClientMap[t] = {c}
            else: terminalClientMap[t].add(c)

    return (partnerTerminalMap,terminalClientMap)

#Main
if __name__ == "__main__":
    
    #Input
    notValidInput = True
    captureMode:Callable[[],tuple[dict[str,str],list[str]]] = captureInputs
    option = str(input("Load from file?(should be named inputB.txt) [Y/n]: "))
    if(option.capitalize() == "Y"):
        captureMode = readFromFile
    #Input loop
    while(notValidInput):
        try:
            ptMap, tcMap = captureMode()
            notValidInput = False
        except Exception as e:
            print(f"Problem detected: {e}")
            input("Continue? [press any key]")

    #Por cada socio...
    for p in ptMap.keys():
        #Mantenemos un mapa cliente:numero de terminales de socio asociadas con él
        clientCount = {}
        for t in ptMap[p]:
            #Si no hay ningún cliente en aquella terminal, saltarla
            if(not tcMap.get(t)): continue
            #Sino...
            for c in tcMap[t]:
                #Actualiza la cantidad de veces que el cliente aparece, en el diccionario
                if(not clientCount.get(c)): clientCount[c] = 1
                else: clientCount[c]+=1

        print(f"Socio: {p} \
            Cliente fiel: {
                #Imprime la llave del máximo par (según valor) del diccionario 
                max(clientCount.items(),key=lambda x : x[1])[0] if (len(clientCount) > 0) else -1
                }"
            )
