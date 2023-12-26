import requests
from bs4 import BeautifulSoup
import json
import time

# Replace 'your_url' with the actual URL of the page containing the JSON data
#url = 'https://shopstar.pe/tecnologia/televisores?order=OrderByReleaseDateDESC&page=2'



def productId_extract(url):

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        #oops = soup.find_all("script")

        # for i in oops:
        #     if "No se ha encontrado ningún producto" in i.text:

        #         return False
        
        

        template_element = soup.find('template', {'data-type': 'json', 'data-varname': '__STATE__'})
        script_element = template_element.find('script')


  

        json_content = script_element.get_text(strip=True)
        # with open("text.txt", "+w") as l:
        #     l.write(json_content)
    
        json_data = json.loads(json_content)

        productId_web = []
        for product_key, product_info in json_data.items():
            try:
                product_id = product_info['productId']
                #print(f"Product ID for {product_id}")
                productId_web.append("fq=productId:"+product_id+"&")
                

            except: 
                continue
        productId_web = "".join(productId_web)

        web = "https://shopstar.pe/api/catalog_system/pub/products/search?"+productId_web
        return web
        



url = "https://shopstar.pe/calzado/zapatillas-hombre/zapatillas?order=OrderByReleaseDateDESC&page=1"
productId_extract(url)