

import pymongo


from decouple import config


# Establecer la conexión a MongoDB
cliente = pymongo.MongoClient(config("MONGODB"))
base_de_datos = cliente["shopstar"]
coleccion = base_de_datos["json_link"]



# Obtener los documentos de la colección

# Iterar sobre los documentos y clasificar según el valor de "lista"
def links():
    webs = []
    documentos = coleccion.find()
    for documento in documentos:
    
        lista = documento["lista"]
        url = documento["url"]
        webs.append(url)


    print(len(webs))

links()