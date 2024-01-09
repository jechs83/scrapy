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



# part = []
# for i in range (9999999):

#         web2 = "&fq=productId:"+str(i)+"&"
#         part.append("".join(web2))

     
# web1 = "https://shopstar.pe/api/catalog_system/pub/products/search?"
# web2 = "".join(part)

# url = web1+web2
        



# with open('urls_listacompleta.py', 'w') as archivo:
#     archivo.write('list_url = ' + str(url))


iterations_per_file =10
for file_number in range(30):  # Create 10 files, each with 1000 URLs (10 * 100)

    part = []
    start_index = file_number * iterations_per_file * 100  # Calculate the starting index for each file

    for i in range(start_index, start_index + (iterations_per_file * 10)):
        web2 = "fq=productId:" + str(i) + "&"
        part.append("".join(web2))

    web1 = "https://shopstar.pe/api/catalog_system/pub/products/search?"
    web2 = "".join(part)

    url = web1 + web2

    # Create separate files for each set of URLs
    file_name = f'a{file_number}.py'
    with open(file_name, 'w') as archivo:
        archivo.write('list_url = ' + '"'+str(url)+'"')