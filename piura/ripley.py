import asyncio
import aiohttp
import json
import random
import re
import time
from datetime import datetime
from datetime import date
from pymongo import MongoClient
from fake_useragent import UserAgent


# Conectar a la base de datos MongoDB
client = MongoClient("mongodb://192.168.1.66:27017")  
db = client['ripley']  
collection = db['productos']  


# Definir las URL base de las páginas web
base_urls = [

    "https://simple.ripley.com.pe/tecnologia/tv-y-cine-en-casa/televisores?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/tecnologia/smart-home/streaming?page={}&s=mdco",
    "https://simple.ripley.com.pe/tecnologia/tv-y-cine-en-casa/proyectores?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/tecnologia/celulares/celulares-y-smartphones?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/tecnologia/celulares/smartwatch-y-wearables?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/tecnologia/computacion/laptops?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/tecnologia/computacion/tablets?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/tecnologia/computacion/impresoras-y-tintas?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/tecnologia/computacion/computadoras-de-escritorio?source=menu&page={}&s=mdco", 
    "https://simple.ripley.com.pe/tecnologia/computacion-gamer/laptops-gamer?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/tecnologia/videojuegos/consolas?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/tecnologia/videojuegos/playstation-5?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/tecnologia/videojuegos/nintendo-consolas?page={}&s=mdco",
    "https://simple.ripley.com.pe/tecnologia/especiales/iphone?page={}&s=mdco",
    "https://simple.ripley.com.pe/tecnologia/audio/audifonos?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/tecnologia/parlantes/todo-parlantes?page={}&s=mdco",
    "https://simple.ripley.com.pe/tecnologia/audio/equipos-de-sonido?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/tecnologia/smart-home/asistente-de-voz?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/tecnologia/camara-de-fotos/drones?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/electrohogar/refrigeracion/refrigeradoras?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/electrohogar/refrigeracion/frigobares-y-cavas?page={}&s=mdco",
    "https://simple.ripley.com.pe/electrohogar/refrigeracion/congeladores?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/electrohogar/refrigeracion/dispensadores-de-agua?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/electrohogar/lavado/lavadoras?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/electrohogar/electrodomesticos/licuadoras?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/electrohogar/electrodomesticos/freidoras-de-aire-y-vaporeras?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/electrohogar/cocina/cocinas-de-pie?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/electrohogar/cocina/hornos-microondas?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/electrohogar/cocina/cocinas-empotrables?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/electrohogar/cocina/campanas?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/electrohogar/limpieza-del-hogar/aspiradoras-de-arrastre?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/electrohogar/aspiradoras/ver-todo?page={}&s=mdco",
    "https://simple.ripley.com.pe/calzado/zapatos-hombre/zapatillas-urbanas?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/deporte/zapatillas/zapatillas-deportivas-hombre?page={}&s=mdco",
    "https://simple.ripley.com.pe/calzado/zapatos-hombre/zapatos-casuales?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/calzado/zapatos-hombre/zapatos-de-vestir?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/calzado/zapatos-mujer/zapatillas-urbanas?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/deporte/zapatillas/zapatillas-deportivas-mujer?page={}&s=mdco",
    "https://simple.ripley.com.pe/calzado/zapatos-mujer/zapatos-de-vestir?source=menu&page={}&s=mdco",
    "https://simple.ripley.com.pe/calzado/zapatos-mujer/zapatos-casuales?source=menu&page={}&s=mdco"

]


def load_datetime():
    
    today = date.today()
    now = datetime.now()
    date_now = today.strftime("%d/%m/%Y")  
    time_now = now.strftime("%H:%M:%S")
        
    return date_now, time_now, today

current_day = load_datetime()[0]

# Generar un agente de usuario aleatorio
user_agent = UserAgent()

async def fetch(session, url):
    async with session.get(url, headers={'User-Agent': user_agent.random, 'Referer': 'https://simple.ripley.com.pe/', 'Accept-Encoding': 'gzip, deflate, br'}) as response:
        return await response.text()

async def process_page(url, session):


    try:
        response_text = await fetch(session, url)

        print(response_text)
        time.sleep(10)

        json_match = re.search(r'window\.__PRELOADED_STATE__\s*=\s*({.*?})\s*;\s*<\/script>', response_text)

     
        if json_match:
            json_data = json_match.group(1)
            data = json.loads(json_data)
            products = data.get('products', [])
            for product in products:
                part_number = product.get('partNumber')
                name = product.get('name')
                link = product.get('url')
                images = product.get('images', [])
                first_image = images[0] if images else None
                if first_image and first_image.startswith('//'):
                    first_image = f"https:{first_image}"
                prices = product.get('prices', {})
                list_price = float(prices.get('listPrice', 0.00))
                offer_price = float(prices.get('offerPrice', 0.00))
                card_price = float(prices.get('cardPrice', 0.00))
                discount_percentage = float(prices.get('discountPercentage', 0.00))
                attributes = product.get('attributes', [])
                brand = next((attribute.get('value') for attribute in attributes if attribute.get('identifier') == 'marca'), "NO HAY PS")
                print("partNumber:", part_number)
                print("brand:", brand)
                print("name:", name)
                print("listPrice:", list_price)
                print("offerPrice:", offer_price)
                print("cardPrice:", card_price)
                print("discountPercentage:", discount_percentage)
                print("link:", link)
                print("first_image:", first_image)
                print("---------------------------------------------")
                # Crear documento para MongoDB
                product_doc = {
                    "sku": part_number,
                    "brand": brand,
                    "product": name,
                    "listPrice": float(list_price),
                    "best_price": float(offer_price),
                    "card_price": float(card_price),
                    "web_dsct": float(discount_percentage),
                    "link": link,
                    "image": first_image,
                    "date":current_day,
                    "home_list":"https//ripley.pe",
                    "time": load_datetime()[1],
                    "market":"Ripley",
                    "card_dsct":int(0)
                }
                # Insertar documento en MongoDB
                collection.insert_one(product_doc)
                pass
        else:
            print(f"No se encontró el JSON en el código fuente de la página: {url}")
    except aiohttp.ClientError as e:
        print(f"Error de conexión al procesar la página {url}: {e}")
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON de la página {url}: {e}")
    except Exception as e:
        print(f"Error desconocido al procesar la página {url}: {e}")

async def main():
    while True:
        for base_url in base_urls:
            page_numbers = range(1, 50)  
            async with aiohttp.ClientSession() as session:
                tasks = []
                for page_number in page_numbers:
                    url = base_url.format(page_number)
                    tasks.append(asyncio.create_task(process_page(url, session)))
                    await asyncio.sleep(random.uniform(1, 1))  # Introducir un retraso aleatorio
                await asyncio.gather(*tasks)

        collection.delete_many({})

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Programa terminado por el usuario.")
