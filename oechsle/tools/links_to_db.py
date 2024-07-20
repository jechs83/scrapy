import re
from pymongo import MongoClient
#from linktoJson_1 import base_link

def insertar_o_actualizar_link_en_db(url, lista, page, market):
    # Conectarse a la base de datos MongoDB
    client = MongoClient('mongodb://192.168.8.66:27017/')  # Cambia la URL si tu MongoDB está en otro lugar
    db = client[market]  # Nombre de la base de datos
    collection = db['links']  # Nombre de la colección

    # Crear el documento a insertar o actualizar
    documento = {
        "_id": url,
        'lista': lista,
        'url': url,
        'page': page
    }

    # Actualizar el documento si existe, o insertar si no existe
    result = collection.update_one(
        {"_id": url},
        {"$set": documento},
        upsert=True
    )

    # Imprimir el resultado de la operación
    if result.upserted_id is not None:
        print(f'Documento insertado con el ID: {result.upserted_id}')
    else:
        print(f'Documento con ID: {url} actualizado')

def procesar_archivo_y_insertar_o_actualizar(archivo, market):
    with open(archivo, 'r') as file:
        for linea in file:
            # Quitar cualquier espacio en blanco al principio o al final de la línea
            linea = linea.strip()
            if linea:  # Ignorar líneas vacías
                # Separar los valores por espacios en blanco
                valores = re.split(r'\s+', linea)
                if len(valores) == 3:  # Asegurarse de que hay exactamente 3 valores
                    url, lista, page = valores
                    # Insertar o actualizar en la base de datos
                    insertar_o_actualizar_link_en_db(url, int(lista), int(page), market)
                else:
                    print(f"Línea ignorada (número incorrecto de valores): {linea}")

# Ejemplo de uso de la función
archivo = '/Users/javier/GIT/scrapy_saga/oechsle/tools/datos.txt'  # Nombre del archivo de texto
market = "oechsle"
procesar_archivo_y_insertar_o_actualizar(archivo, market)

# for i in range (20):
#     lista = i+1
#     try:
#         base_link(lista)
#     except:
#         continue