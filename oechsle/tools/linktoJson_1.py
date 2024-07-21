import requests
from bs4 import BeautifulSoup
import re
import time
from pymongo import MongoClient

def base_link(lista):
    client = MongoClient('mongodb://192.168.8.66:27017')
    db = client['oechsle']
    collection = db['links']

    # Filtrar documentos con el valor del campo lista=2
    data = collection.find({"lista": lista})
    list_url = []
    for i in data:
        list_url.append(i["url"])

    for base in list_url:
        # Tu código existente para extraer base_url
        response = requests.get(base)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            category = soup.find_all("script")

            base_url = None
            for script in category:
                if "/buscapagina?" in script.text:
                    pattern = re.compile(r'/buscapagina.*?PageNumber=')
                    match = pattern.search(script.text)
                    if match:
                        web = match.group()
                        base_url = "https://www.oechsle.pe" + web
                        print(base_url)

                       

                        break  # Salir del bucle una vez que se encuentra el enlace


            if base_url:
                # Guardar base_url en MongoDB
                save_to_mongodb(base, base_url, lista)
                print("se guardo")

def save_to_mongodb(base, base_url, lista):
    # Conectar a MongoDB
    client = MongoClient('mongodb://192.168.8.66:27017')
    db = client['oechsle']
    collection = db['links']

    # Filtrar por "url": base
    filter_query = { "url": base }

    # Verificar si el documento ya existe
    existing_document = collection.find_one(filter_query)
    
    # Imprimir la URL base
    print(base_url)
    base_url = base_url.replace("PS=36&", "PS=50&")
    if existing_document:
        collection.update_one(filter_query, {"$set": {"json_link": base_url}})
        print(f"Updated document for {base}")
    else:
        print(f"No document found for {base}")

# Ejemplo de llamada a la función

    # else:
    #     # No hacer nada si el documento no existe
    #     print(f"No document found for {base} with lista {lista}, nothing was updated.")

    # # Si el documento existe, imprimir sus valores
    # if existing_document:
    #     for key, value in existing_document.items():
    #         print(value)
    # else:
    #     print("No se encontraron documentos que coincidan con el filtro.")



    # if existing_document:
    #     # Actualizar el documento existente con el nuevo base_url
    #     collection.update_one(filter_query, {"$set": {"json_link": base_url}})
    #     print(f"Updated document for {base}")
    # else:
    #     # No hacer nada si el documento no existe
    #     print(f"No document found for {base} with lista {lista}, nothing was updated.")

    # Cerrar la conexión a MongoDB

    # else:
    #     # Insertar un nuevo documento (esto en principio no debería ocurrir con los filtros aplicados)
    #     new_document = {"_id": base, "json_link": base_url, "lista": lista}
    #     collection.insert_one(new_document)
    #     print(f"Inserted new document for {base}")

    # Cerrar la conexión a MongoDB
 

#Ejemplo de uso:

for i in range (20):
    lista = i+1
    try:
        base_link(lista)
    except:
        continue

