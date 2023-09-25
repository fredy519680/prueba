# -*- coding: utf-8 -*-
import tkinter 
from tkinter import filedialog
from collections import namedtuple
import json

archivoac = None
Token = namedtuple("Token",["value", "line", "col"])
Errors = namedtuple("Error",["value", "linea", "col"])

linea= 1
colum = 1 
tokens = []
Errores= []

def tokenstring(texto, i):
    token=""
    for char in texto:
        if char == '"':
            return [token.lower(), i]
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
    global linea, colum, tokens, Errores

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
            error = Errors(char,linea,colum)
            Errores.append(error)
            i += 1
            colum += 1

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


def abrir_archivo():
    global archivo_actual
    archivo = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
    if archivo:
        with open(archivo, "r") as f:
            contenido = f.read()
            cajatexto.delete(1.0, tkinter.END)   
            cajatexto.insert(tkinter.END, contenido)
        archivo_actual = archivo

def guardar_archivo():
    global archivo_actual
    if archivo_actual:
        with open(archivo_actual, "w") as f:
            contenido = cajatexto.get(1.0, tkinter.END)
            f.write(contenido)
            print("El archivo se guardo exitosamente")
    else:
        print("no existe ruta para guardar el archivo")
    
def guardar_como():
    archivo = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
    if archivo:
        with open(archivo, "w") as f:
            contenido = cajatexto.get(1.0, tkinter.END)
            f.write(contenido)

def get_cajatexto():
    contenido = cajatexto.get(1.0, tkinter.END)
    return contenido

def borrar_cajatexto():
    cajatexto.delete(1.0, tkinter.END)
    archivoac = None

def analizar_archivo():
    entrada =  cajatexto.get(1.0, tkinter.END)
    leertexto(entrada)
    borrar_cajatexto()
    for i in tokens:
        tf = f">>> {i}\n"
        cajatexto.insert(tkinter.END, tf)

def guardar_json():
    contenido_json = cajatexto.get("1.0", "end")  

    try:
        datos = json.loads(contenido_json)
        with open("datos.json", "w") as archivo:
            json.dump(datos, archivo, indent=4)
            print("Archivo JSON guardado correctamente.")

    except json.JSONDecodeError as e:
        print("Error al analizar el JSON:", e)

def mostrar_errores():
    global Errores
    borrar_cajatexto()
    secciones = []
    json_data = {
    "errores": secciones
    }
    cont=1
    for i in Errores:
        nueva_seccion = {
        "No": cont,
        f"Descripción": {
            "lexema": f"{i.value}",
            "tipo": f"error lexico",
            "columna": i.linea,
            "fila": i.col
        }
    }
        secciones.append(nueva_seccion)
        cont +=1

        #tf = f">>>   {i.value}\n"
        #cajatexto.insert(tkinter.END, tf)
    cadena_json = json.dumps(json_data, indent=4, ensure_ascii=False)
    cajatexto.insert(tkinter.END, cadena_json)
    guardar_json()


        

ventana = tkinter.Tk()
ventana.title("Analizador Léxico")
ventana.geometry("1000x700")
ventana.configure(bg="gray25")

superior = tkinter.Frame(ventana, bg="blue")
superior.pack(fill="both", expand=True)

superior.grid_rowconfigure(0, weight=1)
superior.grid_columnconfigure(0, weight=1)

botones = tkinter.Frame(superior, bg="blue")
botones.grid(row=0, column=0, sticky="nsew")

boton1 = tkinter.Menubutton(botones, text="Archivo", width=10 , height= 2, bg="lightgray")
boton1.menu = tkinter.Menu(boton1, tearoff=0)
boton1["menu"]= boton1.menu
boton1.menu.add_command(label="Abrir", command=lambda: abrir_archivo())
boton1.menu.add_command(label="Guardar", command=lambda: guardar_archivo())
boton1.menu.add_command(label="Guardar Como", command=lambda: guardar_como())
boton1.menu.add_separator()
boton1.menu.add_command(label="Salir", command=ventana.quit)

boton2 = tkinter.Button(botones, text="Analizar",width=10 , height= 2, bg="lightgray", command=lambda: analizar_archivo())
boton3 = tkinter.Button(botones, text="Errores",width=10 , height= 2, bg="lightgray", command=lambda: mostrar_errores())
boton4 = tkinter.Button(botones, text="Reporte",width=10 , height= 2, bg="lightgray")

boton1.pack(side="left", padx=50)
boton2.pack(side="left", padx=50)
boton3.pack(side="left", padx=50)
boton4.pack(side="left", padx=50)

inferior = tkinter.Frame(ventana, bg="white")
inferior.pack(fill="both", expand=True)


cajatexto = tkinter.Text(inferior,borderwidth=7,relief="solid", font=("Arial", 12))
cajatexto.pack(fill="both", expand=True)
cajatexto.config(highlightbackground="gray")


ventana.mainloop()