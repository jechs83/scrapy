import requests
from concurrent.futures import ThreadPoolExecutor

def scrape_product(product_id):
     base_url = "https://shopstar.pe/api/catalog_system/pub/products/search"
     url = f"{base_url}?fq=productId:{product_id}"

    
     response = requests.get(url)
     response.raise_for_status()
     data = response.json()

     if data and data[0].get("items"):
          product_info = data[0]
          if not product_info:
              pass
          item_info = product_info.get("items", [{}])[0]
          product_name = product_info.get("productName")
          link = product_info.get("link") or f"https://shopstar.pe/{product_info.get('linkText', '')}/p"
          image_url = item_info.get("images", [{"imageUrl": None}])[0].get("imageUrl")
          price_info = item_info.get("sellers", [{}])[0].get("commertialOffer", {})
          price, list_price = price_info.get("Price"), price_info.get("ListPrice")
          product_reference = product_info.get("productReference")

          print(f"Product Reference: {product_reference}")
          print(f"Product Name: {product_name}")
          print(f"Link: {link}")
          print(f"Image URL: {image_url}")
          print(f"Price: {price}")
          print(f"List Price: {list_price}")
          print("\n---\n")
   
def scrape_shopstar_parallel():
    max_product_id = 10000000  #SE PUEDE CAMBIAR
    with ThreadPoolExecutor() as executor:
        executor.map(scrape_product, range(1, max_product_id + 1))

if __name__ == "__main__":
    scrape_shopstar_parallel()
