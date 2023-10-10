import pymongo
from decouple import config

# Conéctate a la base de datos MongoDB
client = pymongo.MongoClient(config("MONGODB"))
db = client["brand_allowed"]
skip_collection = db["sport"]

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

# Cierra la conexión a la base de datos
client.close()
