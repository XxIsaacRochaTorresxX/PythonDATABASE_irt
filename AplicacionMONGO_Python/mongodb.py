
# Clase para conectarnos a MongoDB

import pymongo
from crudmysql import MySQL
from conf import variables
from env import variables as varsmysql


class PyMongo():
    def __init__(self,variables): #host='localhost', db='opensource', port=27017, timeout=1000, user='', password=''
        self.MONGO_DATABASE = variables["db"]
        self.MONGO_URI = 'mongodb://' + variables["host"] + ':' + str(variables["port"])
        self.MONGO_CLIENT =None
        self.MONGO_RESPUESTA = None
        self.MONGO_TIMEOUT = variables["timeout"]

    def conectar_mongodb(self):
        try:
            self.MONGO_CLIENT = pymongo.MongoClient(self.MONGO_URI, serverSelectionTimeoutMS=self.MONGO_TIMEOUT)
        except Exception as error:
            print("ERROR", error)
        else:
            pass
           # print("Conexión al servidor de MongoDB realizada: ", )
        # finally:


    def desconectar_mongodb(self):
        if self.MONGO_CLIENT:
            self.MONGO_CLIENT.close()

    def consulta_mongodb(self,tabla,filtro, atributos={"_id":0}):
        response = {"status": False, "resultado":[]}
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].find(filtro, atributos)
        if self.MONGO_RESPUESTA:
            response["status"] = True
            for reg in self.MONGO_RESPUESTA:
                #print(reg)
                response["resultado"].append(reg)
            #return self.MONGO_RESPUESTA
            #for reg in self.MONGO_RESPUESTA:
            #    print(reg)                                     #ARMAR JSON
        return response

    def consultageneral_mongodb(self, tabla):
        response = {"status": False, "resultado": []}
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].find({})
        if self.MONGO_RESPUESTA:
            response["status"] = True

            for reg in self.MONGO_RESPUESTA:
                response["resultado"].append(reg)

        return response



    # Insertar datos en la coleccion de estudiantes
    def insertar(self,collection, reg):
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][collection].insert_one(reg)
        if self.MONGO_RESPUESTA:
            return self.MONGO_RESPUESTA
        else:
            return False



    #Actualizar documentos en las colecciones
    def actualizar(self, tabla, filtro, nuevos_valores):
        response = {"status":False}
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].update_many(filtro, nuevos_valores)
        if self.MONGO_RESPUESTA:
            response ={"status":True}
            #return self.MONGO_RESPUESTA
        #else:
            #return False
        return response

    def eliminar(self, tabla, filtro):
        response = {"status":False}
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].delete_many(filtro)
        if self.MONGO_RESPUESTA:
            response ={"status":True}
            #return self.MONGO_RESPUESTA
        #else:
            #return False
        return response

    def obtener_promedio_estudiantes(self, tabla):
        response = {"status": False, "resultado":[]}
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].aggregate(
                                                                      [
                                                                        {
                                                                          "$group": {
                                                                            "_id": "$control",
                                                                            "promedio": {"$avg": "$calificacion"}
                                                                          }
                                                                        }
                                                                      ]
                                                                    )
        if self.MONGO_RESPUESTA:
            response["status"] = True
            for reg in self.MONGO_RESPUESTA:
                response["resultado"].append(reg)
        return response

        

def cargar_estudiantes():
    obj_MySQL = MySQL(varsmysql)
    obj_Mongo = PyMongo(variables)
    sql ="SELECT * FROM estudiantes;"
    obj_MySQL.conectar_mysql()
    lista_estudiantes = obj_MySQL.consulta_sql(sql)
    obj_MySQL.desconectar_mysql()
    obj_Mongo.conectar_mongodb()
    for est in lista_estudiantes:
        e = {
            "control": est[0],
            "nombre": est[1]
        }
        print(e)
        obj_Mongo.insertar('estudiantes', e)
    obj_Mongo.desconectar_mongodb()


#cargar_estudiantes()


alumno = {
    'control': 200,
    'nombre':'Piter Pan'
}

# obj_Mongo = PyMongo(variables)
# obj_Mongo.conectar_mongodb()
# obj_Mongo.insertar_estudiante(alumno)
# obj_Mongo.desconectar_mongodb()

