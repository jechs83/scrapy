import pymongo
from decouple import config
import sys
lista_num= sys.argv[1]
page_num = sys.argv[2]
db_name = str(sys.argv[3])
# Establecer la conexión a MongoDB
cliente = pymongo.MongoClient(config("MONGODB"))
base_de_datos = cliente[db_name]
coleccion = base_de_datos["links"]



# Ruta al archivo de texto
archivo_texto = "/Users/javier/GIT/scrapy_saga/links_to_db/urls.txt"

# Abrir el archivo y leer línea por línea
with open(archivo_texto, 'r') as file:
    for line in file:
        # Dividir la línea en campos
        #lista, url, page = line.strip().split(',')
        url= line.strip()


        # Convertir la lista y la página a int
        # lista = int(lista)
        # page = int(page)
        lista = lista_num
        page = page_num
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


