import requests
from bs4 import BeautifulSoup



import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor
import sys
import time
# links = [
#     "https://www.falabella.com.pe/falabella-pe/category/cat250487/Colchon-King?page="
# ]

mongo_client = MongoClient("mongodb://192.168.9.66:27017")  # Ajusta la URL de conexión según tu configuración
db = mongo_client["wong1"]
collection = db["scrap"]


def productId_extract(web):
        
            response = requests.get(web)
            productId_web = []

            print(response.status_code) 
            soup = BeautifulSoup(response.text, 'html.parser')
            template_element = soup.find('template', {'data-type': 'json', 'data-varname': '__STATE__'})


            script_element = template_element.find('script')
            json_content = script_element.get_text(strip=True)
            json_data = json.loads(json_content)

         

        
            for product_key, product_info in json_data.items():
                

                try:
                    product_id = product_info['productId']
                    #print(f"Product ID for {product_id}")
                    productId_web.append("fq=productId:"+product_id+"&")
                except: 
                    continue


              
            productId_web = "".join(productId_web)
            if not productId_web:
                return False
            web = "https://www.wong.pe/api/catalog_system/pub/products/search?"+productId_web
  
            return web


def scrap(url):
      
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    json_content = soup.get_text(strip=True)
    json_data = json.loads(json_content)

    for i in json_data:
        try:
            best_price = i["items"][0]["sellers"][0]["commertialOffer"]["Price"]
        except:
             best_price = 0
        
        try:
         list_price = i["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"]
        except: list_price= 0

        if best_price:
            web_dsct = round(100-(float(best_price)*100/float(list_price)))
        else:
            web_dsct = 0
        
        data = {
             
        "brand" : i["brand"],     
        "product" : i["productName"],
        "link" : i["link"],
        "image" : i["items"][0]["images"][0]["imageUrl"],
        "best_price" :i["items"][0]["sellers"][0]["commertialOffer"]["Price"], 
        "web_dsct": web_dsct,
        "list_price" :i["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"],


        }

        collection.update_one(
            {"product": data["product"]},  # Assuming 'product' is a unique identifier
            {"$set": data},
            upsert=True
        )
        print(json.dumps(data, indent=2))
        #print(data.prettify())
    print(url)



    # for product_key, product_info in json_data.items():
        
    #     product_id = product_info['productId']

    #     print(product_id)
        



# def main():
#     with ThreadPoolExecutor(max_workers=len(webs)) as executor:
#         executor.map(scrap, webs)

# if __name__ == "__main__":
#     main()
        

webs = ["https://www.wong.pe/tecnologia?page=",
        "https://www.wong.pe/electrohogar?page=",
        "https://www.wong.pe/la-jugueteria?page=" ]



# for url in webs:
#     for i in range (20):
     
#         url = productId_extract(url+str(i+1))
#         scrap(url)


for i in webs:

    for e in range (20):
        web = i+str(e+1)
       

        ext = productId_extract(web)
        if ext == False:
            break
            
        scrap(ext)
       