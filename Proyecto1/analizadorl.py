from collections import namedtuple


Token = namedtuple("Token",["value", "line", "col"])
Error = namedtuple("Error",["value", "linea", "col"])

linea= 1
colum = 1 
tokens = []
Errores= []

def tokenstring(texto, i):
    token=""
    for char in texto:
        if char == '"':
            return [token, i]
        token +=char
        i+=1
    print("String no cerrado", token)


def tokennumero(texto, i):
    token=""
    decimal = False
    for char in texto:
        if char.isdigit():
            token += char
            i +=1
        elif char ==".":
            token+=char
            i += 1
            decimal = True
        else: 
            break
    if decimal:
        return [float(token), i]
    
    return [int(token),i]

def leertexto(texto):
    global linea, colum, tokens

    i =0

    while i < len(texto):
        char = texto[i]
        if char.isspace():
            if char== "\n":
                linea += 1
                colum = 1
            elif char == "\t":
                colum += 4
            i +=1
        elif char == '"':
            string, pos = tokenstring(texto[i+1:], i)
            colum += len(string) + 1
            i= pos+2
            token = Token(string, linea, colum)
            tokens.append(token)
        elif char in ["{", "}", "[", "]", ",", ":"]:
            colum += 1
            i+= 1
            token = Token(char, linea, colum)
            tokens.append(token)
        elif char.isdigit():
            numero, pos = tokennumero(texto[i:],i)
            colum += pos-i
            i = pos
            token = Token(numero, linea, colum)
            tokens.append(token)
        else:
            print(
                "Error: caracter desconocido:",
                char,
                "en linea:",
                linea,
                "columna:",
                colum,
            )
            error = Error(char,linea,colum)
            Errores.append(error)
            i += 1
            colum += 1

entrada = open("entrada.json", "r").read()
leertexto(entrada)

def get_instruction():
    global tokens
    operacion = None
    value1 = None
    value2 = None
    while tokens:
        token = tokens.pop(0)
        if token.value == "operacion":
            tokens.pop(0)
            operacion = tokens.pop(0).value
        elif token.value == "valor1":
            tokens.pop(0)
            value1 = tokens.pop(0).value
            if value1 == "[":
                value1 = get_instruction()
        elif token.value == "valor2":
            tokens.pop(0)
            value2 = tokens.pop(0).value
            if value2 == "[":
                value2 = get_instruction()
        else:
            pass

        if operacion and value1 and value2:
            return [operacion, value1, value2]
        elif operacion and operacion in ["seno"] and value1:
            return [operacion, value1]
    return None



def create_instructions():
    global tokens
    instrucciones = []
    while tokens:
        instruccion = get_instruction()
        if instruccion:
            instrucciones.append(instruccion)
    return instrucciones




for i in tokens:
    print(i)
        
        

print("Instrucciones: ", create_instructions())
print(Errores[0])