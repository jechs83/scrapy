import pymongo
import requests
from concurrent.futures import ProcessPoolExecutor
import subprocess

mongo_client = pymongo.MongoClient("mongodb://192.168.9.66:27017/")
db = mongo_client["shopstar"]
collection = db["productos"]
collection.delete_many({})
collection = db["links"]

def process_link(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        data = response.json()

        for product_data in data:
            sku = product_data.get('productId')
            marca = product_data.get('brand')
            product = product_data.get('productName')
            precio2 = product_data.get('items', [])[0].get('sellers', [])[0].get('commertialOffer', {}).get('ListPrice')
            precio1 = product_data.get('items', [])[0].get('sellers', [])[0].get('commertialOffer', {}).get('Price')
            link = product_data.get('link')
            image = product_data.get('items', [])[0].get('images', [])[0].get('imageUrl', '')
            try:
                descuento = round((100 - ((precio1 / precio2) * 100)), 0)
            except ZeroDivisionError:
                descuento = 0.00

            teasers = product_data.get('items', [])[0].get('sellers', [])[0].get('commertialOffer', {}).get('PromotionTeasers', [])
            if teasers:
                for teaser in teasers:
                    effects = teaser.get('Effects', {}).get('Parameters', [])
                    for effect in effects:
                        if effect.get('Name', '') == 'PercentualDiscount':
                            discount_value = float(effect.get('Value', '0'))
                            precio3 = round(precio1 - (precio1 * (discount_value/100)), 2)
            else:
                precio3 = 0.00
                            
            print()
            print("productId:", sku)
            print("brand:", marca)
            print("productName:", product)
            print("Price:", precio1)
            print("ListPrice:", precio2)
            print("PriceOh:", precio3)
            print(descuento)
            print("link:", link)
            print("imageUrl:", image) if image else print("No hay imagen ps")
            print("----------------------")

            # Crear el documento a insertar en la colección "products"
            product_data = {
                "id": sku,
                "brand": marca,
                "product": product,
                "precio_desct": precio1,
                "precio_normal": precio2,
                "precio_card": precio3,
                "descuento": descuento,
                "link": link,
                "imagen": image
            }
            # Insertar el documento en la colección "products"
            products_collection = db["productos"]
            products_collection.insert_one(product_data)

    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud a {link}: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == '__main__':
    # Obtener todos los documentos (en este caso, url) de la colección
    links = collection.distinct("url")
    # Ejecutar la extracción en paralelo con procesos
    with ProcessPoolExecutor() as executor:
        executor.map(process_link, links)

    subprocess.Popen(["start", "cmd", "/k", "python", "shops7.py"], shell=True)