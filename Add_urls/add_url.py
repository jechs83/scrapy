import pymongo
from decouple import config

# Establecer la conexión a MongoDB
cliente = pymongo.MongoClient(config("MONGODB"))
base_de_datos = cliente["saga"]
coleccion = base_de_datos["links"]

# Ruta al archivo de texto
archivo_texto = "/Users/javier/GIT/scrapy_saga/Add_urls/urls.txt"

# Abrir el archivo y leer línea por línea
with open(archivo_texto, 'r') as file:
    for line in file:
        # Dividir la línea en campos
        lista, url, page = line.strip().split(',')

        # Convertir la lista y la página a int
        lista = int(lista)
        page = int(page)

        # Crear un documento para MongoDB
        documento = {
            "lista": lista,
            "url": url,
            "page": page
        }

        # Utilizar update_one con upsert=True para evitar duplicados
        coleccion.update_one(
            {"url": url},
            {"$set": documento},
            upsert=True
        )

print("Datos insertados en la colección 'links'.")


