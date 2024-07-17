import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from pymongo import MongoClient

# Conectar a la base de datos MongoDB
client = MongoClient('mongodb://192.168.8.7:27017/')  
db = client['ripley']  
collection = db['scrap'] 

# Definir las URLs base
base_urls = [
    "https://simple.ripley.com.pe/tecnologia/tv-y-cine-en-casa/televisores?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/tecnologia/smart-home/streaming?page={}&s=mdco",
    # Add more URLs here
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}
print("pasa por aqui")

def scrape_and_store_data(url):
    page = 1
    while True:
        current_url = url.format(page)
        response = requests.get(current_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all('script')

            preloaded_state_content = None
            for script in scripts:
                if 'window.__PRELOADED_STATE__' in str(script):
                    preloaded_state_content = script.string
                    break

            if preloaded_state_content:
                start_index = preloaded_state_content.find("{")
                end_index = preloaded_state_content.rfind("}") + 1
                preloaded_state_content = preloaded_state_content[start_index:end_index]

                preloaded_state_data = json.loads(preloaded_state_content)

                productos = preloaded_state_data.get('products', [])

                if productos:
                    for producto in productos:
                        part_number = producto.get('partNumber', '')
                        name = producto.get('name', '')
                        link = producto.get('url', '')
                        date = datetime.now().strftime("%d/%m/%Y")
                        time_day = datetime.now().strftime("%H:%M:%S")

                        images = producto.get('images', [])
                        first_image = images[0] if images else "https://ripleype.imgix.net/https%3A%2F%2Fmedia-prod-use-1.mirakl.net%2FSOURCE%2Fe5972167b9d14307b7cafa44ab7105cd?w=750&h=555&ch=Width&auto=format&cs=strip&bg=FFFFFF&q=60&trimcolor=FFFFFF&trim=color&fit=fillmax&ixlib=js-1.1.0&s=9c5479a7d8f7e3ff6321285d19132fc1"
                        if first_image and first_image.startswith('//'):
                            first_image = f"https:{first_image}"

                        prices = producto.get('prices', {})
                        list_price = float(prices.get('listPrice', 0.00))
                        offer_price = float(prices.get('offerPrice', 0.00))
                        card_price = float(prices.get('cardPrice', 0.00))
                        discount_percentage = float(prices.get('discountPercentage', 0.00))

                        attributes = producto.get('SKUs', [])
                        for attribute in attributes:
                            valores = attribute.get('Attributes', [])
                            for valor in valores:
                                if valor.get('identifier') == 'marca':
                                    values = valor.get('Values', [])
                                    for v in values:
                                        brand = v.get('values', 'NO HAY PS')
                                      
                        print("sku:", part_number)
                        print("brand:", brand)
                        print("product:", name)
                        print("list_price:", list_price)
                        print("best_price:", offer_price)
                        print("card_price:", card_price)
                        print("web_dsct:", discount_percentage)
                        print("date:", date)
                        print("time:", time_day)
                        print("link:", link)
                        print("image:", first_image)
                        print("---------------------------------------------")

                        product_doc = {
                            "sku": part_number,
                            "brand": brand,
                            "product": name,
                            "list_price": float(list_price),
                            "best_price": float(offer_price),
                            "card_price": float(card_price),
                            "web_dsct": int(discount_percentage),
                            "link": link,
                            "image": first_image,
                            "date": date,
                            "time":time_day,
                            "card_dsct":0,
                            "market":"ripley"
                        }
                        # Insertar documento en MongoDB
                        collection.insert_one(product_doc)
                else:
                    print("No se encontraron productos en la página", page)
                    break  # Salir del bucle while si no hay productos en la página actual
            else:
                print("No se encontró el JSON en la respuesta HTML.")
                break  # Salir del bucle while si no se encuentra el contenido preloaded_state
        else:
            print("Error al acceder a la página:", response.status_code)
            print(current_url)
            time.sleep(10)
            break  # Salir del bucle while si hay un error al hacer la solicitud

        page += 1
        #time.sleep(1)  # Dormir un poco para evitar sobrecargar


    

# Ejecutar la función para cada URL base
for url in base_urls:
    scrape_and_store_data(url)

# Limpiar la base de datos antes de volver a cargarla con los datos actualizados
#collection.delete_many({})
