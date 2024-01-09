


import requests
import re
import json
import time
from shopstar.spiders.urls_db import links


#url = 'https://shopstar.pe/tecnologia/televisores?order=OrderByReleaseDateDESC&page=3'
def get_json(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            
            # Using regular expression to find and extract JSON-like content from the HTML
            pattern = r'<template data-type="json" data-varname="__STATE__">.*?<script>(.*?)</script>.*?</template>'
            match = re.search(pattern, html_content, re.DOTALL)
            
            if match:
                json_str = match.group(1)
                #print(json_str)  # Printing the extracted JSON-like content
            else:
                print("No JSON-like content found in the HTML.")
            json_data = json.loads(json_str)

            productos = []
            for i,v in json_data.items():
                try:
                    pro = v["cacheId"].replace("sp-","")

                    print(pro)
                    productos.append("fq=productId:"+pro+"&")
                except: 
                    continue 
                    
            print(productos)

            web1 = "https://shopstar.pe/api/catalog_system/pub/products/search?"


            url = web1 + ''.join(productos)


            return url
        

        else:
            print(f"Failed to fetch the page. Status code: {response.status_code}")

    except requests.RequestException as e:
        print(f"Request error: {e}")


urls = links()[0]
lista_urls =[]
def todas_url(urls):

    for i, v in enumerate(urls):
        for e in range(50):
            url2  = v[0]+"&page="+str(e+1)

            url = get_json(url2)
            if url =="https://shopstar.pe/api/catalog_system/pub/products/search?":
                break

            print(url)


todas_url(urls)