import requests
from bs4 import BeautifulSoup
import json
import pymongo
from decouple import config
import time
MONGOdb = "mongodb+srv://spok:Vulcano.2013@cluster0.wkqej.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# MongoDB client initialization
client = pymongo.MongoClient(MONGOdb)
db = client["shopstar"]
collection = db["links2"]

# Function to extract product IDs and construct the search URL
def productId_extract(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')
        template_element = soup.find('template', {'data-type': 'json', 'data-varname': '__STATE__'})
        if template_element:
            script_element = template_element.find('script')
            if script_element:
                json_content = script_element.get_text(strip=True)
                try:
                    json_data = json.loads(json_content)
                    productId_web = [f"fq=productId:{product_info['productId']}&" for product_info in json_data.values() if 'productId' in product_info]
                    if productId_web:
                        productId_web = "".join(productId_web)
                        web = f"https://shopstar.pe/api/catalog_system/pub/products/search?{productId_web}"
                        return web
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return None

# Function to save links to MongoDB
def save_link(url):
    client = pymongo.MongoClient(MONGOdb)
    db = client["shopstar"]
    collection = db["links2"]
    fail_count = 0  # Initialize failure counter
    for i in range(50):
        page_url = url + str(i + 1)
        web = productId_extract(page_url)
        if web:
            document = {
                "lista": 1,
                "_id": page_url,
                "url": web,
            }
            existing_doc = collection.find_one({"_id": page_url})
            if existing_doc and existing_doc.get("url") == web:
                print(f"Documento con ID {page_url} y URL {web} ya existe. No se actualiza.")
            else:
                collection.update_one({"_id": page_url}, {"$set": document}, upsert=True)
                print(f"Documento con ID {page_url} actualizado/insertado.")
            fail_count = 0  # Reset failure counter on success
        else:
            print(f"Failed to extract product ID from {page_url}")
            fail_count += 1  # Increment failure counter
            if fail_count > 3:
                print(f"Failed to extract product ID from {page_url} more than 3 times. Skipping to next URL.")
                break


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


# Run tasks sequentially
def run_tasks():
    for url in urls:
        save_link(url)

if __name__ == "__main__":
    while True:
        run_tasks()
        print("Iteration complete, waiting before next run...")
        time.sleep(30)  # Wait for 1 hour before the next iteration