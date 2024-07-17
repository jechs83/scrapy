import requests
from bs4 import BeautifulSoup
import json
import pymongo
from decouple import config

# Function to extract product IDs and construct the search URL
def productId_extract(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        template_element = soup.find('template', {'data-type': 'json', 'data-varname': '__STATE__'})
        if template_element:
            script_element = template_element.find('script')
            if script_element:
                json_content = script_element.get_text(strip=True)
                try:
                    json_data = json.loads(json_content)
                    productId_web = []
                    for product_key, product_info in json_data.items():
                        if 'productId' in product_info:
                            product_id = product_info['productId']
                            productId_web.append(f"fq=productId:{product_id}&")
                    productId_web = "".join(productId_web)
                    web = f"https://shopstar.pe/api/catalog_system/pub/products/search?{productId_web}"
                    return web
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
    return None

# List of URLs to process
urls = [
    "https://www.shopstar.pe/tecnologia/televisores?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/televisores/4k-ultra-hd?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/televisores/nanocell-tv?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/televisores/oled-tv?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/televisores/qled-tv?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/televisores/smart-tv?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/televisores/proyectores?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/streaming-2024?page=",
    "https://www.shopstar.pe/tecnologia/computo?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/computo/all-in-one-y-desktops?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/computo/impresoras?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/computo/laptops?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/computo/laptops/laptops-gamer?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/computo/monitores?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/computo/tablets?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/computo/tintas-y-consumibles?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/computo/laptops/macbooks?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/computo/tablets/ipads?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/telefonia?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/telefonia/celulares?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/telefonia/smartwatch?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/videojuegos?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/videojuegos/consolas?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/videojuegos/nintendo?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/videojuegos/juegos-ps4?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/videojuegos/juegos-ps5?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/camaras?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/camaras/camaras-de-seguridad?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/camaras/camaras-deportivas-y-acuaticas?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/camaras/camaras-digitales?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/camaras/drones?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/camaras/camaras-instantaneas?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/audio?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/audio/audifonos?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/audio/parlantes?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/audio/soundbar-y-home-theater?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/audio/audio-y-video?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/audio/equipos-y-torres-de-sonido?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/audio/audio-profesional?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/audio/radios---radioreloj---autoradios?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/audio/instrumentos-musicales?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/smart-home?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/smart-home/asistente-de-voz?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/smart-home/seguridad-inteligente?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/computo/accesorios-de-computo/mouse?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/computo/accesorios-de-computo/teclados?order=OrderByReleaseDateDESC&page=",
    "https://www.shopstar.pe/tecnologia/computo/accesorios-de-computo/parlantes-y-aud%C3%ADfonos?order=OrderByReleaseDateDESC&page=",
]

# Function to save links to MongoDB
def save_links():
    cliente = pymongo.MongoClient(config("MONGODB"))
    base_de_datos = cliente["shopstar"]
    coleccion = base_de_datos["links2"]

    for url in urls:
        for i in range(50):
            web = productId_extract(url+str(i+1))
            print(web)
            if web:
                documento = {
                    "_id": web,
                    "url": web,
                }
                coleccion.update_one(
                    {"_id": web},
                    {"$set": documento},
                    upsert=True
                )
            else:
                print(f"Failed to extract product ID from {url}")





save_links()
