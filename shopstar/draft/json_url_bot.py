
from jsonTolink import productId_extract
import pymongo
from decouple import config
from multiprocessing import Pool
import time
import sys

# Your existing code...

#lista = (sys.argv[1])
lista = 1


def process_url(lkn):
    print(lkn)
  
    cliente = pymongo.MongoClient(config("MONGODB"))
    base_de_datos = cliente["shopstar"]
    coleccion = base_de_datos["json_link"]

    for i in range(50):
        
        link1 = lkn + "&page="+str(i + 1)
  
        web = productId_extract(link1)
        print(web)

        if web == False:
            continue
      

        if web == "https://shopstar.pe/api/catalog_system/pub/products/search?":
            break
      
        # lista = arg_
        print(web)
        documento = {
   
            "category": link1,
            "lista":int(1),
            "url": web,
        }

        coleccion.update_one(
            {"_id": link1},
            {"$set": documento},
            upsert=True
        )

def web_to_jsonUrl_parallel(urls):

   
    with Pool(processes=10) as pool:  # Adjust the number of processes as needed
        pool.map(process_url, urls)



# Rest of your code...
cliente = pymongo.MongoClient(config("MONGODB"))
base_de_datos = cliente["shopstar"]
coleccion = base_de_datos["links"]


if __name__ == '__main__':



    webs = []
    documentos = coleccion.find()


    for documento in documentos:
     
            url = documento["url"]
            webs.append(url)

    while True:
       
             web_to_jsonUrl_parallel(webs)