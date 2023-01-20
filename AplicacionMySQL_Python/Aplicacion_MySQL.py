from crudmysql import MySQL
from caja import Password
from env import variables
#ruta=("C:\Users\UnaTacitadeCafe\PycharmProjects\Unidad2")
ar=[]
tupla=[]
def Alumnos():
    archivo = open("Estudiantes.prn", "r")
    for x in archivo:
        ar.append(x[0:8])
        ar.append(x[8:].replace("\n",""))
        tupla.append(tuple(ar))
        ar.clear()
    archivo.close()
    #print(tupla)
    # print(tupla)
    return tupla
Coj=set()
def Materias():
    MA = open("Kardex.txt", "r")
    matr = []
    lis = []

    for x in MA:
        lis = x.split("|")
        matr.append(lis[0])
        matr.append(lis[1])
        matr.append(lis[2].replace("\n", ""))
        Coj.add(tuple(matr))
        matr.clear()
    # print(Coj)
    MA.close()
    return (Coj)
def Usuarios():          #Ejercicio 1
    archivo = open("usuarios.txt", "r")
    usuarios = set()
    for linea in archivo:
        d2 = linea.split(" ")
        usuarios.add((d2[0], d2[1], d2[2]))
    return usuarios

def cargar_datos():
    obj_estudiante=MySQL(variables)
    lista_estudiante=Alumnos()
    print(lista_estudiante)
    obj_estudiante.conectar_mysql()
    for ctrl,nom in lista_estudiante:
        sql=f"INSERT INTO estudiantes() values('{ctrl}','{nom}');"
        print(sql)
        obj_estudiante.consulta_sql(sql)
    # print(lista_estudiante)
    obj_estudiante.desconectar_mysql()

def cargar_Kardex():
    obj_estudiante = MySQL(variables)
    lista_karnex=Materias()
    #print(Materias())
    obj_estudiante.conectar_mysql()
    for ctrl,NomMateria,cali in lista_karnex:
        sql = f"INSERT INTO kardex(control,materia,calificacion) values('{ctrl}','{NomMateria}',{cali});"
        obj_estudiante.consulta_sql(sql)
        print(sql)
    obj_estudiante.desconectar_mysql()

def cargar_usuario():
    obj_estudiante = MySQL(variables)
    lista_Usuario = Usuarios()
    obj_estudiante.conectar_mysql()
    for ctrol,clave,clave_cifrada in lista_Usuario:
        sql = f"INSERT INTO usuarios(control,clave,clave_cifrada) values('{ctrol}','{clave}','{clave_cifrada}');"
        obj_estudiante.consulta_sql(sql)
        print(sql)
    obj_estudiante.desconectar_mysql()

def menu():
    while True:
        print("============================Menu=============================");
        print("1, Insertar estudiantes");
        print("2. Actualizar calificaciones");
        print("3. Consultar materia por estudiante");
        print("4. Consulta general de estudiante");
        print("5. Eliminar a un estudiante");
        print("6. Salir");
        print("==============================================================");
        print("Dame la opcion que deseas");
        try:
            opcion = int(input(""));
        except Exception as error:
            print("Error: ",error);
            break
        if opcion==1:
            insertar_Estudiante()
        if opcion==2:
            actualizar_calificacion()
        if opcion==3:
            Consultar_Materias()
        if opcion==4:
            Consulta_Generar()
        if opcion==5:
            Eliminar_Estudiante()
        if opcion==6:
            break
    else:
         print("opcion no validad");
def Eliminar_Estudiante():
    obj_MySQL = MySQL(variables)
    print("==Eliminar Estudiante==")
    ctrl = input("Dame el numero de control: ")
    obj_eliminar1= f"delete from kardex where control='{ctrl}';"
    obj_eliminar2 = f"delete from usuarios where control='{ctrl}';"
    obj_eliminar3 = f"delete from estudiantes where control='{ctrl}';"
    obj_MySQL.consulta_sql(obj_eliminar1)
    obj_MySQL.consulta_sql(obj_eliminar2)
    obj_MySQL.consulta_sql(obj_eliminar3)

def Consulta_Generar():
    obj_MySQL = MySQL(variables)
    print("==Consulta General==")
    obj_consulta_general=f"select E.control,E.nombre, format(avg(K.calificacion),1) as promedio from estudiantes E, kardex K where E.control=K.control group by K.control;"
    estu=obj_MySQL.consulta_sql(obj_consulta_general)
    print("N_Control        Nombre               Promedio")
    for est in estu:
        print(est[0], est[1] ,est[2])

def Consultar_Materias():
    obj_MySQL = MySQL(variables)  # *********************************
    print(" == CONSULTAR MATERIAS POR ESTUDIANTE ==")
    ctrl = input("Dame el numero de control: ")
    sql_materias = "SELECT E.nombre, K.materia, K.calificacion " \
                   "FROM estudiantes E, kardex K " \
                   f"WHERE E.control = K.control and E.control='{ctrl}';"
    print(sql_materias)
    resp = obj_MySQL.consulta_sql(sql_materias)
    if resp:
        print("Estudiante: ", resp[0][0])
        for mat in resp:
            print("Materia: ", mat[1], " Calificación: ", mat[2])
    else:
        print(f"El estudiante con Número de control: {ctrl} NO existe")

def actualizar_calificacion():
    obj_MySQL = MySQL(variables)
    print("==Actualizar calificacion==")
    ctrl = input("Dame el numero de control: ")
    materia = input("Dame la materia a calificar: ")
    sql_buscar_materia=f"SELECT 1 From kardex where control='{ctrl}' AND materia='{materia.strip()}';"
    respuesta=obj_MySQL.consulta_sql(sql_buscar_materia)
    if respuesta:
        promedio=float(input("Dame  el nuevo promedio: "))
        sql_actualizar_prom=f"update karnex set calificacion={promedio} where control='{ctrl} AND materia='{materia}';'"
        print("El promedio ha sido actualizado")
    else:
        print(f"El estudiante con numero de control {ctrl} o la materia {materia} no existe")
   # sql_materia = input(f"update kardex set calificacion=100 where control='14420999'and materia='Inteligencia Artificial';")

def insertar_Estudiante():
    obj_MySQL =MySQL(variables)
    print("== Insertar estudiantes==")
    ctrl =input("Dame el numero de control: ")
    nombre=input("Dame el nombre del estudiante: ")
    clave=input("Dame la clave de acceso: ")
    obj_usuario = Password(longitud=len(clave), contrasena=clave)
    sql_estudiante=f"INSERT INTO estudiantes VALUES('{ctrl}','{nombre}');"
    sql_usuarios=f'INSERT INTO usuarios(control, clave,clave_cifrada) VALUES("{ctrl}","{clave}","{obj_usuario.contrasena_sifrada}"); ';
    obj_MySQL.consulta_sql(sql_estudiante)
    obj_MySQL.consulta_sql(sql_usuarios)

menu()
#cargar_datos()
#cargar_Kardex()
#cargar_usuario()

