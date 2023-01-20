'''
Tema: Aplicación de estructuras de Python: archivos, JSON, cifrado de contraseñas
Fecha: 07 de septiembre del 2022
Autor: Isaac Rocha Torres
PRÁCTICA 7
'''


import json
import random
import bcrypt


def regresa_conjunto_estudiantes():

    arch = "Estudiantes.prn"
    fh = open(arch, 'r') #Abrimos el archivo
    estudent = set()
    lista_estudent = fh.readlines()

    for i in lista_estudent[0:]:
        estudiante = i.split("\n")
        ctrl1 = estudiante[0][0:8]
        nombre = estudiante[0][8:]
        tupla_est = (ctrl1, nombre) #Hacemos las tuplas
        estudent.add(tupla_est)
    return estudent

def regresa_conjunto_promedios():

    arch = "Kardex.txt"
    fk = open(arch, 'r') #abrimos el archivos
    materias= set()
    lista_materias = fk.readlines()

    for i in lista_materias[0:]:
        materia = i.split("\n")
        datos = materia[0].split('|')
        ctrl2 = datos[0]
        nomMat = datos[1]
        calif = int(datos[2])
        materias.add((ctrl2,nomMat,calif)) #Hacemos las tuplas
    return materias
#print(regresa_conjunto_promedios())

def regresa_materias_por_estudiante(ctrl):
    promedios = regresa_conjunto_promedios()
    lista_materias=[]
    for mat in promedios:
        c,m,p = mat #destructurar la variable
        if ctrl == c:
            lista_materias.append({"Nombre: ":m})
    return  json.dump(lista_materias)

def generar_letra_mayuscula(): #Regresa una letra de la A-...-Z
    return chr(random.randint(65,90)) # si te invluye los límites

def generar_letra_minuscula():
    return chr(random.randint(97,122)) #regresa letra minuscula de la a..z

def generar_numeros():
    return chr(random.randint(48,57)) #regresa un numero entre 0 y 9

def genera_caracter_especial(): # regresa un caracter especial
    lista_caracteres = ['@', '#','$', '%', '&','_', '?','!']
    return lista_caracteres[random.randint(0,7)]

def generar_contrasena():
    clave = ""

    for i in range(0,10):
        numero = random.randint(1,5)

        if numero == 1:
            clave = clave + generar_letra_mayuscula()
        elif numero == 2:
            clave = clave + generar_letra_minuscula()
        elif numero == 3:
            clave = clave + genera_caracter_especial()
        elif numero >= 4 and numero <= 5:
            clave = clave + generar_numeros()
            #regresar clave
    return clave

#print(generar_contrasena())

#Cifrar contraseñas con bcrypt

def cifrar_contrasena(contrasena):#la cadena debe convertirse a bytes antes de convertirla
    sal = bcrypt.gensalt() # default tiene 12
    contrasena_cifrada = bcrypt.hashpw(contrasena.encode('utf-8'), sal)
    return contrasena_cifrada

#clave =generar_contrasena()
#print("Contraseña generada: ",clave,"\n","Contraseña cifrada: ",cifrar_contrasena(clave))


#Generar el archivo de usuarios


'''

6. Crear un método "autenticar_usuario(usuario,contrasena)" que regrese una bandera que 
   indica si se pudo AUTENTICAR, el nombre del estudiante y un mensaje, regresar el JSON:
   {
        "Bandera": True,
        "Usuario": "Leonardo Martínez González",
        "Mensaje": "Bienvenido al Sistema de Autenticación de usuarios"
   }

   ó

   {
        "Bandera": False,
        "Usuario": "",
        "Mensaje": "No existe el Usuario"
   }

   ó

    {
        "Bandera": False,
        "Usuario": "Leonardo Martínez González",
        "Mensaje": "Contraseña incorrecta"
   }
'''

def generar_archivo_usuarios():
    #obtener lista de estudiantes
    estudiantes = regresa_conjunto_estudiantes()
    usuarios = open("usuarios.txt", "w")
    contador = 1
    for est in estudiantes:
        c,n =est
        clave = generar_contrasena()
        clave_cifrada = cifrar_contrasena(clave)
        registro = c + " " +  clave + " " +  str(clave_cifrada, 'utf-8') +  " \n"
        usuarios.write(registro)
        contador += 1
        print(contador)
    print("Archivo generado")

#generar_archivo_usuarios()


def autenticar_usuario (usuario, contrasena):

    archivo_usuario = open("usuarios.txt", "r")
    archivo_estudiantes = regresa_conjunto_estudiantes()
    lista_usuario = archivo_usuario.readlines()

    flag = True
    user = usuario
    passw =contrasena
    msj = " "
    u=""
    log={}

#evaluar si existe el usuario

    for est in archivo_estudiantes:
        c, n = est
        u=c

        if c == user:
            for u in lista_usuario[0:]:
                usuarios = u.split(" ")
                if usuarios[1] == passw and (bcrypt.checkpw(passw.encode('utf-8'),usuarios[2].encode('utf-8'))):
                 flag = True
                 msj = "Bienvenido al Sistema de Autenticación de usuarios"
                 log["Bandera: "] = flag
                 log["Usuario: "] = n
                 log["Mensaje: "] = msj

                 print(log)
                 break
                elif usuarios[1] != passw:
                   # print(usuarios[1] ,"....", passw)
                    flag = False
                    msj ="Contraseña incorrecta"
            if flag == False and msj == "Contraseña incorrecta":
                log["Bandera: "] = flag
                log["Usuario: "] = n
                log["Mensaje: "] = msj
                print(log)
                break
    if u != user and msj == " ":
        flag = False
        msj = "No existe el Usuario"
        log["Bandera: "] = flag
        log["Usuario: "] = ""
        log["Mensaje: "] = msj
        print(log)
    return log

def solicitar_usuario():
    user = input("Ingresa el número de control a utilizar: ")
    return user

def solicitar_pass():
    contra = input("Ingresa contraseña: ")
    return contra

with open('consulta.json', 'w') as file:
    json.dump(autenticar_usuario(solicitar_usuario(),solicitar_pass()), file, indent=4)