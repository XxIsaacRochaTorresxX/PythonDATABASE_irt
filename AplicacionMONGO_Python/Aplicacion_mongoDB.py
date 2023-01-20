from caja import Password
from crudmysql import MySQL
from conf import variables
from env import variables as varsmysql
from mongodb import PyMongo


def cargar_estudiantes():
    obj_MySQL = MySQL(varsmysql)
    obj_Mongo = PyMongo(variables)

    sql_estudiante ="SELECT * FROM estudiantes;"
    sql_kardex = "SELECT * FROM kardex;"
    sql_usuarios = "SELECT * FROM usuarios;"

    obj_MySQL.conectar_mysql()
    #print("CONEXIÓN REALIZADA CORRECTAMENTE")

    lista_estudiantes = obj_MySQL.consulta_sql(sql_estudiante)
    lista_kardex = obj_MySQL.consulta_sql(sql_kardex)
    lista_usuarios = obj_MySQL.consulta_sql(sql_usuarios)

    print(lista_estudiantes)

    obj_MySQL.desconectar_mysql()

    #Para Insertar datos en MONGO
    obj_Mongo.conectar_mongodb()

    #ESTUDIANTES
    for est in lista_estudiantes:
        e = {
            "control": est[0],
            "nombre": est[1]
        }
        #print(e)
        obj_Mongo.insertar('estudiantes', e)

    #MATERIAS
    for mat in lista_kardex:
        m = {
            "idkardex": mat[0],
            "control": mat[1],
            "materia": mat[2],
            "calificacion": float(mat[3])
        }
        #print(e)
        obj_Mongo.insertar('kardex', m)

    #USUARIOS
    for usu in lista_usuarios:
        u = {
            "idUsuario": usu[0],
            "control": usu[1],
            "clave": usu[2],
            "clave_cifrada": usu[3]
        }
        #print(e)
        obj_Mongo.insertar('usuarios', u)

    obj_Mongo.desconectar_mongodb()


#cargar_estudiantes()


def insertar_estudiante():
    obj_PyMongo=PyMongo(variables)
    print("== Insertar estudiante ==")
    ctrl =input("Dame el numero de control: ")
    nombre=input("Dame el nombre del estudiante: ")
    clave=input("Dame la clave de acceso: ")
    obj_usuario = Password(longitud=len(clave), contrasena=clave)
    json_estudiante={'control':ctrl,'nombre':nombre}
    json_usuarios={'idUsuario':100,'clave':clave,'clave_cifrada':obj_usuario.contrasena_cifrada.decode()}
    obj_PyMongo.conectar_mongodb()
    obj_PyMongo.insertar('estudiantes',json_estudiante)
    obj_PyMongo.insertar('usuarios',json_usuarios)
    obj_PyMongo.desconectar_mongodb()
    print("Datos insertados Correctamente")

def actualizar_calificacion():
    obj_PyMongo=PyMongo(variables)
    print("==Actualizar calificacion==")
    ctrl = input("Dame el numero de control: ")
    materia = input("Dame la materia a calificar: ")
    filtro_buscar_materia= {'control': ctrl, 'materia': materia}

    obj_PyMongo.conectar_mongodb()
    respuesta=obj_PyMongo.consulta_mongodb('kardex',filtro_buscar_materia)
    for reg in respuesta:
        print(reg)
    if respuesta:
        print("Encontrado")
        promedio = float(input("Dame el nuevo promedio: "))
        json_act_prom={"$set":{"calificacion": promedio}} #ACTUALIZAR
        resp=obj_PyMongo.actualizar('kardex', filtro_buscar_materia, json_act_prom)
        if resp['status']:
            print("Promedio actualizado")
        else:
            print("Ocurrió un error al actualizar")
    else:
        print(f"El estudiante con numero de control {ctrl} o la materia {materia} no existe")
    obj_PyMongo.desconectar_mongodb()

def consultar_materias():
    obj_PyMongo=PyMongo(variables)  # *********************************
    print(" == CONSULTAR MATERIAS POR ESTUDIANTE ==")
    ctrl = input("Dame el numero de control: ")
    filtro= {'control':ctrl}
    atributos_estudiante = {"_id": 0, "nombre":1}
    atributos_kardex = {"_id": 0, "materia":1, "calificacion": 1}
    #sql_materias = "SELECT E.nombre, K.materia, K.calificacion " \
    #               "FROM estudiantes E, kardex K " \
    #               f"WHERE E.control = K.control and E.control='{ctrl}';"
    #print(sql_materias)
    obj_PyMongo.conectar_mongodb()


    respuesta1 = obj_PyMongo.consulta_mongodb('estudiantes', filtro, atributos_estudiante)
    respuesta2 = obj_PyMongo.consulta_mongodb('kardex', filtro, atributos_kardex)

    if respuesta1["status"] and respuesta2["status"]:
        print("Estudiantes: ", respuesta1["resultado"][0]["nombre"])
        for mat in  respuesta2["resultado"]:
            print(mat["materia"], mat["calificacion"])

    #print("Respuesta_1", respuesta1)
    #print("Respuesta_2", respuesta2)

    obj_PyMongo.desconectar_mongodb()

def consulta_general():
    obj_PyMongo = PyMongo(variables)  # *********************************
    print(" == CONSULTA GENERAL ==")
    obj_PyMongo.conectar_mongodb()
    respuesta_1 = obj_PyMongo.consultageneral_mongodb("estudiantes")
    respuesta_2 = obj_PyMongo.consultageneral_mongodb("kardex")
    obj_PyMongo.desconectar_mongodb()
    i = 0;
    if respuesta_1["status"] and respuesta_2["status"]:
        print("N_Control        Nombre               Promedio")
        for res1 in respuesta_1["resultado"]:
            j=0
            prom = 0
            cont = 0
            for res2 in respuesta_2["resultado"]:
                if respuesta_1["resultado"][i]["control"] == respuesta_2["resultado"][j]["control"]:
                    prom += respuesta_2["resultado"][j]["calificacion"]
                    cont += 1
                j+=1
            if(cont>0):
                prom = prom/cont
            print(respuesta_1["resultado"][i]["control"], respuesta_1["resultado"][i]["nombre"], prom)
            i+=1

# funcion que consulta promedio de un solo estudiante
def promedio_estudiante(promedios, ctrl):
    for prom in promedios:
        if prom['_id'] == ctrl:
            return prom['promedio']
    return 0


def consulta_general_profesor():
    obj_PyMongo = PyMongo(variables)
    filtro = {}
    obj_PyMongo.conectar_mongodb()
    lista_estudaintes = obj_PyMongo.consulta_mongodb('estudiantes', filtro)
    lista_promedios = obj_PyMongo.obtener_promedio_estudiantes('kardex')
    obj_PyMongo.desconectar_mongodb()
    print(lista_estudaintes)
    print(lista_promedios)

    for est in lista_estudaintes['resultado']:
        promedio = promedio_estudiante(lista_promedios['resultado'],est['control'])
        print(est['control'], est['nombre'], round(promedio,1))


def eliminar():
    obj_PyMongo=PyMongo(variables)
    print("==ELIMINAR==")
    ctrl = input("Dame el numero de control: ")
    filtro_buscar= {'control': ctrl}

    obj_PyMongo.conectar_mongodb()
    respuesta=obj_PyMongo.consulta_mongodb('estudiantes',filtro_buscar)


    if respuesta["status"]:
        print("Estudiante ha sido eliminado")
        obj_PyMongo.eliminar('estudiantes', filtro_buscar)
        obj_PyMongo.eliminar('kardex', filtro_buscar)
        obj_PyMongo.eliminar('usuarios', filtro_buscar)
    else:
        print(f"El estudiante con numero de control {ctrl} no existe")
    obj_PyMongo.desconectar_mongodb()


def menu():
    while True:
        print("================MENÚ PRINCIPAL====================")
        print("1. Insertar Estudiante")
        print("2. Actualizar Callificación")
        print("3. Consultar Materias por estudiante")
        print("4. Consulta General de Estudiante")
        print("5. Eliminar un Estudiante")
        print("6. Salir")
        print()

        try:
             op = int(input("¿Qué deseas realizar?: "))
        except Exception as error:
            print("ERROR: ", error)
            break
        else:
            if op == 1:
               insertar_estudiante()
            elif op == 2:
                actualizar_calificacion()
            elif op == 3:
                consultar_materias()
            elif op == 4:
                consulta_general_profesor()
            elif op == 5:
                eliminar()
            elif op == 6:
                break
            else:
                print("Opción incorrecta")

menu()