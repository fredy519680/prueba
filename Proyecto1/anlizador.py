from collections import namedtuple

Token = namedtuple("Token", ["value", "line", "col"])


line = 1
col = 1

tokens = []


def tokenize_string(input_str, i):
    token = ""
    for char in input_str:
        if char == '"':
            return [token, i]
        token += char
        i += 1
    print("String no cerrado", token)



def tokenize_number(input_str, i):
    token = ""
    isDecimal = False
    for char in input_str:
        if char.isdigit():
            token += char
            i += 1
        elif char == ".":
            token += char
            i += 1
            isDecimal = True
        else:
            break
    if isDecimal:
        return [float(token), i]

    return [int(token), i]


def tokenize_input(input_str):
    global line, col, tokens

    i = 0
    while i < len(input_str):
        char = input_str[i]
        if char.isspace():
            if char == "\n":
                line += 1
                col = 1
            elif char == "\t":
                col += 4
            i += 1
        elif char == '"':
            string, pos = tokenize_string(input_str[i + 1:], i)
            col += len(string) + 1
            i = pos + 2
            token = Token(string, line, col)
            tokens.append(token)
        elif char in ["{", "}", "[", "]", ",", ":"]:
            col += 1
            i += 1
            token = Token(char, line, col)
            tokens.append(token)
        elif char.isdigit():
            number, pos = tokenize_number(input_str[i:], i)
            col += pos - i
            i = pos
            token = Token(number, line, col)
            tokens.append(token)
        else:
            print(
                "Error: caracter desconocido:",
                char,
                "en linea:",
                line,
                "columna:",
                col,
            )
            i += 1
            col += 1

entrada = open("entrada.json", "r").read()
tokenize_input(entrada)


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
            # eliminar el :
            tokens.pop(0)
            value1 = tokens.pop(0).value
            if value1 == "[":
                value1 = get_instruction()
        elif token.value == "valor2":
            # eliminar el :
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

print("INSTRUCCIONES: ", create_instructions())