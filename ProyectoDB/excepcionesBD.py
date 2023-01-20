'''
Autor:Isaac Rocha Torres
'''

import json

import mysql.connector


productos = []
def connectarmysql(host, user, pwd, bd):

    try:
        conexion = mysql.connector.connect(host=host,user=user,password=pwd, database=bd)
    except Exception as error:
        print("Error: ", error)
    else:
        # crear consulta a la base de datos
        mi_cursor = conexion.cursor()
        try:
            mi_cursor.execute("select id, nombre, precio from productos")
        except mysql.connector.errors.ProgrammingError as e:
            print("Error en la consulta: ", e)
        except Exception as error:
            print("ERROR: ", error)
        else:

            for reg in mi_cursor:
                producto = {}
                clave, nombre, precio = reg
                producto["Clave: "]= clave
                producto["Nombre: "] = nombre
                producto["Precio: "] = str(precio)
                productos.append(producto)
            print(productos)
            mi_cursor.close()
        conexion.close()

connectarmysql("localhost", "root","", "opensource")

with open('Producto.json', 'w') as file:
    json.dump(productos, file, indent=4)