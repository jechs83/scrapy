# import pymongo
# from decouple import config

# # Conéctate a la base de datos MongoDB
# client = pymongo.MongoClient("mongodb://192.168.9.66:27017")
# db = client["brand_allowed"]
# skip_collection = db["todo"]

# # Lee el archivo de texto y agrega los elementos a la base de datos
# archivo_texto = "/Users/javier/GIT/scrapy_saga/skip.txt"

# with open(archivo_texto, "r") as file:
#     for line in file:
#         # Convierte el elemento a minúsculas y elimina espacios en blanco alrededor
#         elemento = line.strip().lower()

#         # Verifica si el elemento ya existe en la colección
#         if skip_collection.find_one({"brand": elemento}):
#             print(f"{elemento} ya existe en la colección, no se agregará.")
#         else:
#             # Si no existe, agrégalo a la colección
#             skip_collection.insert_one({"brand": elemento})
#             print(f"{elemento} agregado a la colección.")

# # Cierra la conexión a la base de datos
# client.close()


import pymongo
from decouple import config

try:
    # Conéctate a la base de datos MongoDB
    client = pymongo.MongoClient("mongodb://192.168.9.66:27017")
    db = client["brand_allowed"]
    skip_collection = db["todo"]

    # Lee el archivo de texto y agrega los elementos a la base de datos
    archivo_texto = "/Users/javier/GIT/scrapy_saga/skip.txt"

    with open(archivo_texto, "r") as file:
        for line in file:
            # Convierte el elemento a minúsculas y elimina espacios en blanco alrededor
            elemento = line.strip().lower()

            # Verifica si el elemento ya existe en la colección
            if skip_collection.find_one({"brand": elemento}):
                print(f"{elemento} ya existe en la colección, no se agregará.")
            else:
                # Si no existe, agrégalo a la colección
                skip_collection.insert_one({"brand": elemento})
                print(f"{elemento} agregado a la colección.")
except Exception as e:
    print(f"Ocurrió un error: {str(e)}")
finally:
    # Cierra la conexión a la base de datos
    if 'client' in locals():
        client.close()

