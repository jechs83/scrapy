from bs4 import BeautifulSoup
import json
import requests
import time
import re



def base_link(base):
   
    # def json_extract():
        response = requests.get(base)
        if response.status_code == 200:

            soup = BeautifulSoup(response.text, 'html.parser')
            category = soup.find_all("script" )

            for i in category:
                 
                 if "/buscapagina?" in i.text:

                    pattern = re.compile(r'/buscapagina.*?PageNumber=')
                    match = pattern.search(i.text)
                    web = match.group()

                    base_url = "https://www.oechsle.pe"+web
        print()           
        print(base_url)
        return base_url
                                             

def json_link(link):
   
        response = requests.get(link)
       
        if response.status_code == 200:

            productos = []

            soup = BeautifulSoup(response.text, 'html.parser')
        

            product_id = soup.find_all('div', {'data-id': True})

            for i in product_id:

                productos.append("&fq=productId:"+str(i["data-id"]))


            web1= "https://www.oechsle.pe/api/catalog_system/pub/products/search?"
            web2 = "".join(productos)

            json_link = web1+web2

            return json_link
     



# def parse(web):
   
#     response = requests.get(web)
   
#     data = json.loads(response.text)
  

#     count = 0
        
#         # extracted_data = []
#     for i in data:
#             count = count+1
#             item = {}
        
#             item["product"]=  i["productName"]
  
#             item["image"]=  i["items"][0]["images"][0]["imageUrl"]
#             item["brand"]=  i["brand"]

#             # product = item["brand"].lower()
#             # marca_not_allowed = []
#             # if self.lista == []:
#             #     pass
#             # else:
#             #     if product not in self.lista:

#             #         continue

#             item["link"]=  i["link"]
#             item["sku"] = i["productReference"]


#             item["list_price"] =   float(i["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"])

#             try:
#                 item["best_price"] =   float(i["items"][0]["sellers"][0]["commertialOffer"]["Price"])
#             except:item["best_price"] = 0

#             if item["best_price"] == item["list_price"]:
#                 item["web_dsct"] = 0

#             elif item["best_price"] != 0:
#                 item["web_dsct"]  = round(100-(item["best_price"]*100/item["list_price"]))
#             else:
#                 item["web_dsct"] = 0

#             try:
#                 dcst_tarjeta =   float(i["items"][0]["sellers"][0]["commertialOffer"]["PromotionTeasers"][0]["Effects"]["Parameters"][1]["Value"])
        
#             except: dcst_tarjeta = None
#             if dcst_tarjeta != None:
#                 item["card_price"] =item["list_price"] - dcst_tarjeta
#                 item["card_dsct"] = round(100-(item["card_price"] *100/item["list_price"]))
#             else:
#                 item["card_price"]= 0
#                 item["card_dsct"] =0 

#             item["home_list"] = "home" 
#             item["_id"]=   item["sku"]
#             # item["date"] = current_day
#             # item["time"] = current_time
#             item["market"] = "oechsle"


#             print("###########")
#             print(count)
#             print("##############")
#             print(item["brand"])
#             print(item["product"])
#             print(item["link"])
#             print(item["image"])
#             print(item["best_price"])
#             print(item["list_price"])
#             print(item["card_price"])

#             print(item)
        




# #         #return extracted_data
# # dd = "https://www.oechsle.pe/api/catalog_system/pub/products/search?&fq=productId:1000598699&fq=productId:1000598698&fq=productId:1000598697&fq=productId:1000597350&fq=productId:1000597349&fq=productId:1000593180&fq=productId:1000593179&fq=productId:1000592980&fq=productId:1000592979&fq=productId:1000588977&fq=productId:1000588857&fq=productId:1000580148&fq=productId:1000580147&fq=productId:1000580146&fq=productId:1000580144&fq=productId:1000577947&fq=productId:1000576516&fq=productId:1000566240&fq=productId:1000560629&fq=productId:1000559419&fq=productId:1000548270&fq=productId:1000547673&fq=productId:1000547672&fq=productId:1000547667&fq=productId:1000547003&fq=productId:1000547001&fq=productId:1000547000&fq=productId:1000546999&fq=productId:1000546997&fq=productId:1000546996&fq=productId:1000546987&fq=productId:1000546985&fq=productId:1000546293&fq=productId:1000545976&fq=productId:1000503551&fq=productId:1000546984"

# # parse(dd)
# # # for i in range (50):

# # #     url = base_link(oh_link)+str(i+1)
# # #     print(json_link(url))
# # #     parse(json_link(url))
# # #     print("paso "+str(i))     
# # #     print(url)

      
    





# # oh_link = "https://www.oechsle.pe/tecnologia/televisores&page=3"
# # #   https://www.oechsle.pe/tecnologia/televisores?&optionOrderBy=OrderByScoreDESC&O=OrderByScoreDESC&page=2
# # oh_link = "https://www.oechsle.pe/tecnologia/televisores?&optionOrderBy=OrderByScoreDESC&optionOrderBy=OrderByScoreDESC&O=OrderByScoreDESC&optionOrderBy=OrderByScoreDESC&page=3"
# #link2 = "https://www.oechsle.pe/tecnologia/televisores?&optionOrderBy=OrderByScoreDESC&optionOrderBy=OrderByScoreDESC&O=OrderByScoreDESC&optionOrderBy=OrderByScoreDESC&page=4"
# link2 = "https://www.oechsle.pe/tecnologia/televisores"
# base_link(link2)