import scrapy
from bs4 import BeautifulSoup
import time
import requests
import re
#from shopstar.spiders.gteurls import get_json
import json
import pymongo
from decouple import config
from datetime import datetime
from datetime import date

cliente = pymongo.MongoClient(config("MONGODB"))
base_de_datos = cliente["shopstar"]
coleccion = base_de_datos["links"]



lista1=[];lista2=[];lista3=[];lista4=[];lista5=[];lista6=[];lista7=[];lista8=[];lista9=[];lista10=[];lista11=[];lista12=[];lista13=[];lista14=[];lista15=[];lista16=[];lista17=[];lista18=[];lista19=[]; lista20 =[]


# Obtener los documentos de la colección

# Iterar sobre los documentos y clasificar según el valor de "lista"
def links():
    documentos = coleccion.find()
    for documento in documentos:
        lista = documento["lista"]
        url = documento["url"]
        page = documento["page"]
    
        for i in range(1, 20):  # Start the loop from 1 instead of 0
            if lista == i:
                # Agregar a la lista correspondiente en el formato requerido
                if i == 1:
                    lista1.append((url, page))
                elif i == 2:
                    lista2.append((url, page))
                elif i == 3:
                    lista3.append((url, page))
                elif i == 4:
                    lista4.append((url, page))
                elif i == 5:
                    lista5.append((url, page))

                elif i == 6:
                    lista6.append((url, page))
                elif i == 7:
                    lista7.append((url, page))
                elif i == 8:
                    lista8.append((url, page))
                elif i == 9:
                    lista9.append((url, page))
                elif i == 10:
                    lista10.append((url, page))
                elif i == 11:
                    lista11.append((url, page))
                elif i == 12:
                    lista12.append((url, page))
                elif i == 13:
                    lista13.append((url, page))
                elif i == 14:
                    lista14.append((url, page))
                elif i == 15:
                    lista15.append((url, page))
                elif i == 16:
                    lista16.append((url, page))
                elif i == 17:
                    lista17.append((url, page))
                elif i == 18:
                    lista18.append((url, page))
                elif i == 19:
                    lista19.append((url, page))
                elif i == 20:
                    lista20.append((url, page))

    return lista1,lista2,lista3,lista4,lista5,lista6,lista7,lista8,lista9,lista10,lista11,lista12,lista13,lista14,lista15,lista16,lista17,lista18,lista19, lista20 






def get_json(url):

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
                    productos.append("fq=productId:"+pro+"&")
                    
                except: 
                    continue 
                    
            #print(productos)
       

            web1 = "https://shopstar.pe/api/catalog_system/pub/products/search?"

            web2 = ''.join(productos)

            #print(web2)

            url = web1 + web2

            return url
        


url_general = []




lista_urls = links()[0]
for i in lista_urls:
    
        for e in range(50):
            try:
             web_t = i[0]+"&page="+str(e+1)
            except:
                break

            if web_t == "h&page=1":
                break
            # print(web_t)
            # print()
            url_complete = get_json(web_t)
            #print(url_complete)

            url_general.append(url_complete)

print(url_complete)

# Guardar la lista en el archivo
with open('urls_listacompleta.py', 'w') as archivo:
    archivo.write('list_url = ' + str(url_general))