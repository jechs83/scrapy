import requests
from bs4 import BeautifulSoup
import json
import pymongo
from decouple import config
import time
from concurrent.futures import ProcessPoolExecutor

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

urls2=[
    "https://www.shopstar.pe/muebles/sala?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/muebles/sala/centro-de-entretenimiento?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/muebles/sala/sofas-y-seccionales?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/muebles/sala/sofa-cama?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/muebles/sala/reclinables?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/muebles/sala/juegos-de-living?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/muebles/sala/mesas-de-centro?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/muebles/sala/bares?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/muebles/sala/complementos-de-sala?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/muebles/comedor?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/muebles/comedor/juego-de-comedor?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/muebles/comedor/mesas?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/muebles/comedor/sillas?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/muebles/comedor/bares?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/muebles/dormitorio?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/muebles/dormitorio/roperos?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/muebles/dormitorio/comodas-y-mesas-de-noche?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/muebles-de-dormitorio/tocadores?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/muebles/dormitorio/camas?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/muebles/dormitorio/combos-de-dormitorio?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/muebles/dormitorio/juegos-de-dormitorio?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/muebles/dormitorio/muebles-infantiles?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/colchones?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/colchones/1-plaza?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/colchones/1-5-plazas?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/colchones/2-plazas?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/colchones/queen?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/colchones/king?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/colchones/cuna?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/camas-box-tarima?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/camas-box-tarima/1-plaza?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/camas-box-tarima/1-5-plazas?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/camas-box-tarima/2-plazas?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/camas-box-tarima/queen?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/camas-box-tarima/king?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/cama-americana?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/cama-americana/1-plaza?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/cama-americana/1-5-plazas?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/cama-americana/2-plazas?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/cama-americana/queen?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/cama-americana/king?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/cama-estandar?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/cama-estandar/1-plaza?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/cama-estandar/2-plazas?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/dormitorio/cama-estandar/king?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/construccion-y-herramientas/electricidad?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/construccion-y-herramientas/electricidad/cables-y-alambres-electricos?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/construccion-y-herramientas/electricidad/extensiones?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/construccion-y-herramientas/electricidad/interruptores-y-tomacorrientes?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/construccion-y-herramientas/electricidad/linternas-pilas-y-baterias?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/construccion-y-herramientas/electricidad/transformadores-y-estabilizadores?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/construccion-y-herramientas/ferreteria?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/construccion-y-herramientas/ferreteria/chapas-y-cerrajeria?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/construccion-y-herramientas/gasfiteria?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/construccion-y-herramientas/gasfiteria/bombas-de-agua-y-motobombas?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/construccion-y-herramientas/gasfiteria/filtros-y-purificadores-de-agua?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/construccion-y-herramientas/gasfiteria/tanques-de-agua-y-accesorios?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/construccion-y-herramientas/herramientas?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/construccion-y-herramientas/herramientas/accesorios-para-herramientas-electricas?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/construccion-y-herramientas/herramientas/equipos-para-soldar?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/construccion-y-herramientas/herramientas/herramientas-electricas-estacionarias?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/construccion-y-herramientas/herramientas/herramientas-electricas-portatiles?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/construccion-y-herramientas/herramientas/maquinaria-de-construccion?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/construccion-y-herramientas/materiales-de-construccion/herramientas-de-construccion?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/construccion-y-herramientas/seguridad/camaras-de-seguridad?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/construccion-y-herramientas/pisos-y-ceramicos/cortadoras-y-accesorios?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/automovil/accesorios-y-baterias-para-autos?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/automovil/accesorios-y-baterias-para-autos/accesorios-de-exterior?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/automovil/accesorios-y-baterias-para-autos/baterias-y-accesorios?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/automovil/accesorios-y-baterias-para-autos/seguridad-del-auto?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/automovil/motocicletas?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/automovil/llantas?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/deportes-y-aire-libre/mundo-fitness?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/deportes-y-aire-libre/mundo-fitness/elipticas?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/deportes-y-aire-libre/mundo-fitness/maquinas-de-abdominales?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/deportes-y-aire-libre/mundo-fitness/mini-gimnasios?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/deportes-y-aire-libre/mundo-fitness/spinning?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/deportes-y-aire-libre/mundo-fitness/trotadoras?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/deportes-y-aire-libre/aire-libre-y-camping/piscinas-inflables-y-estructurales?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/deportes-y-aire-libre/aire-libre-y-camping/piscinas-inflables-y-estructurales/inflables?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/deportes-y-aire-libre/bicicletas-y-electricos/bicicletas-hombre?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/deportes-y-aire-libre/bicicletas-y-electricos/bicicletas-mujer?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/deportes-y-aire-libre/bicicletas-y-electricos/bicicletas-ninos?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/deportes-y-aire-libre/bicicletas-y-electricos/scooters-electricos?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/deportes-y-aire-libre/aire-libre-y-camping?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/deportes-y-aire-libre/aire-libre-y-camping/coolers?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/deportes-y-aire-libre/aire-libre-y-camping/carpas?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/hogar/menaje-cocina/ollas?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/hogar/menaje-cocina/juego-de-ollas?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/hogar/menaje-cocina/sartenes-y-woks?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/hogar/parrillas-cilindros-y-cajas-chinas?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/hogar/Parrillas-cilindros-y-cajas-chinas/cajas-chinas?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/hogar/Parrillas-cilindros-y-cajas-chinas/cilindros?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/hogar/Parrillas-cilindros-y-cajas-chinas/parrillas?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/hogar/bano/duchas-electricas?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/hogar/bano/inodoros-y-asientos?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/hogar/bano/lavatorios?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/hogar/bano/puertas-y-cabinas-de-ducha?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/hogar/bano/tinas-e-hidromasajes?order=OrderByReleaseDateDESC&page=",
"https://www.shopstar.pe/hogar/bano/griferia-para-bano?order=",
]

# Function to save links to MongoDB
def save_link(url):
    # BASE DDE DATOS DONDE QUIRES QUE LO GUARDE
    cliente = pymongo.MongoClient(config("MONGODB"))
    base_de_datos = cliente["shopstar"]
    coleccion = base_de_datos["links"]
    

    for url in urls:
        for i in range(50):
            
            web = productId_extract(url + str(i + 1))
            if web =="https://shopstar.pe/api/catalog_system/pub/products/search?":
                break
                
          
     

            if web:
                documento = {
                    "lista": 1,
                    "_id": url + str(i + 1),
                    "url": web,
                }
                
                # Comprobar si ya existe un documento con el mismo ID y URL
                existing_doc = coleccion.find_one({"_id": url + str(i + 1)})
                if existing_doc and existing_doc.get("url") == web:
                    print(f"Documento con ID {url + str(i + 1)} y URL {web} ya existe. No se actualiza.")
                else:
                    coleccion.update_one(
                        {"_id": url + str(i + 1)},
                        {"$set": documento},
                        upsert=True
                    )
                    print(f"Documento con ID {url + str(i + 1)} actualizado/insertado.")
            else:
                print(f"Failed to extract product ID from {url}")

# Using ProcessPoolExecutor to parallelize the save_links function
def main():
    with ProcessPoolExecutor(max_workers=8) as executor:
        executor.map(save_link, urls2)

if __name__ == "__main__":
    main()
