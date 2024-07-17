import requests
import json
import re
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor
import subprocess

# Función para extraer los productId de una página
def extract_product_ids(url):
    response = requests.get(url)
    html_content = response.text

    # Encontrar el bloque de datos JSON
    pattern = r'<template data-type="json" data-varname="__STATE__">\s*<script>({.*?})<\/script>\s*<\/template>'
    match = re.search(pattern, html_content, re.DOTALL)

    product_ids = []

    if match:
        json_data = json.loads(match.group(1))

        # Extraer los productId
        product_ids = [data["productId"] for key, data in json_data.items() if "productId" in data]

    return product_ids

# Función para construir el enlace con los productId
def build_product_link(product_ids):
    base_url = "https://shopstar.pe/api/catalog_system/pub/products/search"
    parameters = "&".join([f"fq=productId:{product_id}" for product_id in product_ids])
    return f"{base_url}?{parameters}"

# Lista de URL base
base_urls = [
    "https://www.shopstar.pe/tecnologia/televisores/4k-ultra-hd?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/televisores/nanocell-tv?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/televisores/oled-tv?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/televisores/qled-tv?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/televisores/smart-tv?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/televisores/proyectores?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/tecnologia/computo/all-in-one-y-desktops?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/computo/impresoras?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/computo/laptops?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/computo/laptops/laptops-gamer?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/computo/monitores?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/computo/tablets?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/computo/laptops/macbooks?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/computo/tablets/ipads?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/tecnologia/telefonia/celulares?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/telefonia/smartwatch?order=OrderByReleaseDateDESC&page={}",
    "https://shopstar.pe/tecnologia/telefonia/celulares/samsumg/samsung?initialMap=c,c,c&initialQuery=tecnologia/telefonia/celulares&map=category-1,category-2,category-3,brand,brand&order=OrderByReleaseDateDESC&page={}",
    "https://shopstar.pe/tecnologia/telefonia/celulares/xiaomi?initialMap=c,c,c&initialQuery=tecnologia/telefonia/celulares&map=category-1,category-2,category-3,brand&order=OrderByReleaseDateDESC&page={}",
    "https://shopstar.pe/tecnologia/telefonia/celulares/apple?initialMap=c,c,c&initialQuery=tecnologia/telefonia/celulares&map=category-1,category-2,category-3,brand&order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/tecnologia/videojuegos/consolas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/videojuegos/nintendo?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/videojuegos/juegos-ps4?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/videojuegos/juegos-ps5?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/tecnologia/camaras/camaras-de-seguridad?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/camaras/camaras-deportivas-y-acuaticas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/camaras/camaras-digitales?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/camaras/drones?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/camaras/camaras-instantaneas?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/tecnologia/audio/audifonos?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/audio/audio-y-video?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/audio/parlantes?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/audio/soundbar-y-home-theater?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/audio/equipos-y-torres-de-sonido?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/audio/audio-profesional?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/audio/radios---radioreloj---autoradios?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/audio/instrumentos-musicales?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/tecnologia/smart-home/asistente-de-voz?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/tecnologia/smart-home/seguridad-inteligente?order=OrderByReleaseDateDESC&page={}",

    "https://shopstar.pe/tecnologia/apple?initialMap=c&initialQuery=tecnologia&map=category-1,marca&order=OrderByReleaseDateDESC&page={}",
    "https://shopstar.pe/tecnologia/asus?initialMap=c&initialQuery=tecnologia&map=category-1,marca&order=OrderByReleaseDateDESC&page={}",
    "https://shopstar.pe/tecnologia/hisense?initialMap=c&initialQuery=tecnologia&map=category-1,brand&order=OrderByReleaseDateDESC&page={}",
    "https://shopstar.pe/tecnologia/hp?initialMap=c&initialQuery=tecnologia&map=category-1,marca&order=OrderByReleaseDateDESC&page={}",
    "https://shopstar.pe/tecnologia/lg?initialMap=c&initialQuery=tecnologia&map=category-1,marca&order=OrderByReleaseDateDESC&page={}",
    "https://shopstar.pe/tecnologia/samsung?initialMap=c&initialQuery=tecnologia&map=category-1,brand&order=OrderByReleaseDateDESC&page={}",
    "https://shopstar.pe/pesonyb2c?map=seller&order=OrderByReleaseDateDESC&page={}",
    "https://shopstar.pe/tecnologia/xiaomi?initialMap=c&initialQuery=tecnologia&map=category-1,marca&order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/electrohogar/electrodomesticos/batidoras?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/electrodomesticos/cafeteras?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/electrodomesticos/combos?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/electrodomesticos/extractor-y-exprimidor?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/electrodomesticos/freidoras?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/electrodomesticos/hervidores?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/electrodomesticos/hornos-electricos?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/hornos-microondas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/electrodomesticos/licuadoras?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/electrodomesticos/ollas-arroceras-y-multiusos?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/electrodomesticos/tostadoras-wafleras-sandwicheras-y-parrillas-electricas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/aspirado?order=OrderByReleaseDateDESC&page={}",
    
    "https://www.shopstar.pe/electrohogar/lavado/lavadoras?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/lavado/lavasecas-y-centros-de-lavado?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/lavado/lavavajillas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/lavado/secadoras?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/electrohogar/cocina/campanas-extractoras?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/cocina/cocinas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/cocina/hornos-empotrables?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/cocina/cocinas-empotrables-y-encimeras?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/cocina/combos?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/electrohogar/refrigeracion/congeladoras?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/refrigeracion/frigobares?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/refrigeracion/refrigeradoras?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/refrigeracion/dispensadores-de-agua?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/refrigeracion/visicoolers?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/electrohogar/climatizacion/aire-acondicionado?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/climatizacion/calefaccion?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/climatizacion/deshumedecedores?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/climatizacion/ventiladores-y-extractores?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/climatizacion/termas-y-rapiduchas?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/electrohogar/electrodomesticos/aspirado/aspiradoras?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/electrodomesticos/aspirado/aspiradoras-inalambricas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/electrodomesticos/aspirado/aspiradoras-robot?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/electrodomesticos/aspirado/hidrolavadoras?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/electrohogar/electrodomesticos/aspirado/lustradoras-y-limpiadores-a-vapor?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/belleza-y-cuidado-personal/perfumeria/colonias?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/belleza-y-cuidado-personal/perfumeria/perfumes-de-hombre?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/belleza-y-cuidado-personal/perfumeria/perfumes-de-mujer?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/belleza-y-cuidado-personal/perfumeria/sets-de-perfumes?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/muebles/sala/centro-de-entretenimiento?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/muebles/sala/sofas-y-seccionales?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/muebles/sala/sofa-cama?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/muebles/sala/reclinables?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/muebles/sala/juegos-de-living?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/muebles/sala/mesas-de-centro?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/muebles/sala/bares?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/muebles/comedor/juego-de-comedor?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/muebles/oficina/sillas-de-oficina?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/muebles/oficina/escritorios?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/muebles/oficina/sillas-gamer?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/muebles/oficina/escritorios-gamer?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/muebles/oficina/libreros-y-estantes?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/muebles/dormitorio/roperos?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/muebles/dormitorio/zapateras?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/muebles/dormitorio/cabeceras?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/muebles/dormitorio/comodas-y-mesas-de-noche?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/muebles-de-dormitorio/tocadores?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/muebles/dormitorio/combos-de-dormitorio?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/muebles/terrazas/sets-de-terrazas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/muebles/terrazas/sillas-y-mesas-para-terrazas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/muebles/terrazas/accesorios-de-terraza?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/calzado/calzado-hombre/botines?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/calzado/calzado-hombre/mocasines?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/calzado/calzado-hombre/sandalias?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/calzado/calzado-hombre/zapatos?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/calzado/calzado-hombre/zapatos-casuales?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/calzado/calzado-hombre/zapatos-formales?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/calzado/zapatillas-hombre/zapatillas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/calzado/zapatillas-hombre/zapatillas-futbol?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/calzado/zapatillas-hombre/zapatillas-outdoor?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/calzado/zapatillas-hombre/zapatillas-training?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/calzado/zapatillas-hombre/zapatillas-urbanas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/calzado/zapatillas-hombre/zapatillas-running?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/calzado/calzado-mujer/zapatos?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/calzado/calzado-mujer/zapatos-casuales?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/calzado/calzado-mujer/zapatos-planos-y-ballerinas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/calzado/zapatillas-mujer/zapatillas?order=OrderByReleaseDateDES&page={}",
    "https://www.shopstar.pe/calzado/zapatillas-mujer/zapatillas-outdoor?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/calzado/zapatillas-mujer/zapatillas-training?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/calzado/zapatillas-mujer/zapatillas-urbanas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/calzado/zapatillas-mujer/zapatillas-running?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/dormitorio/colchones/1-plaza?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/colchones/1-5-plazas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/colchones/2-plazas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/colchones/queen?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/colchones/king?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/colchones/cuna?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/dormitorio/camas-box-tarima/1-plaza?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/camas-box-tarima/1-5-plazas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/camas-box-tarima/2-plazas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/camas-box-tarima/queen?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/camas-box-tarima/king?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/dormitorio/juegos-de-dormitorio/1-5-plazas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/juegos-de-dormitorio/2-plazas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/juegos-de-dormitorio/queen?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/juegos-de-dormitorio/king?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/dormitorio/ropa-de-cama/sabanas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/ropa-de-cama/edredones?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/ropa-de-cama/cubrecamas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/ropa-de-cama/mantas-y-frazadas?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/dormitorio/camas-funcionales/bases?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/camas-funcionales/box-espacio?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/camas-funcionales/divanes?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/muebles/dormitorio/roperos?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/muebles-de-dormitorio/tocadores?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/muebles/dormitorio/comodas-y-mesas-de-noche?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/muebles/dormitorio/combos-de-dormitorio?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/dormitorio/cama-americana/1-5-plazas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/cama-americana/2-plazas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/cama-americana/queen?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/cama-americana/king?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/dormitorios-paraiso?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorios-drimer?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorios-forli?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorios-rosen?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorios-el-cisne?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorios-serta?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/dormitorio/infantil/cunas-y-camas-para-ninos?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/infantil/muebles-infantiles?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/infantil/ropa-de-cama-infantil?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/dormitorio/cama-estandar/1-plaza?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/cama-estandar/2-plazas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/cama-estandar/queen?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/dormitorio/cama-estandar/king?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/hogar/menaje-cocina/accesorios-de-cocina?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/menaje-cocina/cuchillos-de-cocina?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/menaje-cocina/juego-de-ollas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/menaje-cocina/ollas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/menaje-cocina/organizadores-y-contenedores?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/menaje-cocina/sartenes-y-woks?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/menaje-cocina/termos?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/menaje-cocina/tuppers?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/menaje-cocina/utensilios-de-cocina?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/menaje-cocina/multiollas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/menaje-cocina/teteras-y-cafeteras?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/hogar/maletas-y-viajes/maletas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/maletas-y-viajes/bolsos-mochilas-y-maletines-de-viaje?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/maletas-y-viajes/accesorios-de-viaje?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/maletas-y-viajes/mochilas-outdoors?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/hogar/Parrillas-cilindros-y-cajas-chinas/cajas-chinas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/Parrillas-cilindros-y-cajas-chinas/cilindros?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/Parrillas-cilindros-y-cajas-chinas/parrillas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/Parrillas-cilindros-y-cajas-chinas?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/hogar/bano/accesorios-de-bano?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/bano/duchas-electricas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/bano/inodoros-y-asientos?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/bano/lavatorios?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/bano/muebles-para-bano?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/bano/puertas-y-cabinas-de-ducha?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/bano/tinas-e-hidromasajes?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/bano/griferia-para-bano?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/hogar/menaje-comedor/cuchilleria?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/menaje-comedor/platos-y-vajillas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/menaje-comedor/postre-te-y-cafe?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/hogar/decoracion/velas-y-portavelas?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/hogar/cocina/lavaderos-de-cocina?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/cocina/muebles-de-cocina?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/hogar/cocina/griferia-para-cocina?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/accesorios-de-moda/relojes/relojes-mujer?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/accesorios-de-moda/relojes/relojes-deportivos?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/accesorios-de-moda/relojes/relojes-hombre?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/accesorios-de-moda/carteras-y-accesorios/bolsos-y-carteras?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/accesorios-de-moda/billeteras-y-monederos/hombre?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/accesorios-de-moda/billeteras-y-monederos/mujer?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/deportes-y-aire-libre/bicicletas-y-electricos/bicicletas-hombre?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/deportes-y-aire-libre/bicicletas-y-electricos/bicicletas-mujer?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/deportes-y-aire-libre/bicicletas-y-electricos/bicicletas-ninos?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/deportes-y-aire-libre/bicicletas-y-electricos/scooters-electricos?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/deportes-y-aire-libre/mundo-fitness/elipticas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/deportes-y-aire-libre/mundo-fitness/mini-gimnasios?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/deportes-y-aire-libre/mundo-fitness/spinning?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/deportes-y-aire-libre/mundo-fitness/trotadoras?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/moda/hombre/jeans-y-pantalones?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/moda/hombre/polerones?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/moda/hombre/polos?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/moda/hombre/ropa-de-bano?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/moda/hombre/shorts-y-bermudas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/moda/hombre/chompas?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/moda/mujer/blusas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/moda/mujer/chompas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/moda/mujer/jeans-y-pantalones?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/moda/mujer/polos?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/moda/mujer/lenceria-y-pijamas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/moda/mujer/ropas-de-bano?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/moda/mujer/vestidos?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/moda/mujer/enterizos?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/moda/mujer/ropa-deporte-mujer?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/moda/hombre/ropa-deporte-hombre/buzos?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/moda/hombre/ropa-deporte-hombre/camisetas-de-futbol?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/moda/hombre/ropa-deporte-hombre/pantalones-deportivos?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/moda/hombre/ropa-deporte-hombre/polos-deportivos?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/moda/hombre/ropa-deporte-hombre/shorts?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/moda/mujer/ropa-deporte-mujer/buzos?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/moda/mujer/ropa-deporte-mujer/polos-deportivos?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/construccion-y-herramientas/gasfiteria/bombas-de-agua-y-motobombas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/construccion-y-herramientas/gasfiteria/filtros-y-purificadores-de-agua?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/construccion-y-herramientas/gasfiteria/tanques-de-agua-y-accesorios?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/construccion-y-herramientas/herramientas/accesorios-para-herramientas-electricas?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/construccion-y-herramientas/herramientas/equipos-para-soldar?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/construccion-y-herramientas/herramientas/herramientas-electricas-estacionarias?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/construccion-y-herramientas/herramientas/herramientas-electricas-portatiles?order=OrderByReleaseDateDESC&page={}",
    "https://www.shopstar.pe/construccion-y-herramientas/herramientas/maquinaria-de-construccion?order=OrderByReleaseDateDESC&page={}",

    "https://www.shopstar.pe/construccion-y-herramientas/pisos-y-ceramicos/cortadoras-y-accesorios?order=OrderByReleaseDateDESC&page={}",



]

# Conexión a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['shopstar']
collection = db['links']
collection.delete_many({})

# Función para procesar una URL base
def process_base_url(base_url):
    page_number = 1
    has_next_page = True

    while has_next_page:
        url = base_url.format(page_number)
        product_ids = extract_product_ids(url)

        if not product_ids:
            has_next_page = False
        else:
            product_link = build_product_link(product_ids)
            print(f"Enlace de productos de la página {page_number} para la URL {base_url}:")
            print(product_link)
            collection.insert_one({'url': product_link})
            page_number += 1

# Procesamiento paralelo de URLs base
with ThreadPoolExecutor() as executor:
    executor.map(process_base_url, base_urls)

# Lanzar otro script Python
subprocess.Popen(["start", "cmd", "/k", "python", "shops8.py"], shell=True)
