'''
Autor:Isaac Rocha Torres
'''
import pymongo

def conexion_mongo(host='localhost', db='opensource', port=27017, timeout=1000,user='', pwd=''):
    #Crear cadena de conexión
    MONGO_URI = 'mongodb://' + host + ':' + str(port)
    MONGO_CLIENT = None
    MONGO_RESPUESTA = None


    try:
        MONGO_CLIENT = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS= timeout)
        MONGO_RESPUESTA = MONGO_CLIENT[db]['productos'].find({})
        for reg in MONGO_RESPUESTA:
            print(reg['nombre'])
    except Exception as error:
        print("ERROR: ", error)
    else:
        print("correcto")
    finally:
        if MONGO_CLIENT:
            MONGO_CLIENT.close()

conexion_mongo()