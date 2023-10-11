import scrapy
from promart.items import PromartItem
from datetime import datetime
from datetime import date
from promart.spiders import url_list 
import uuid
import pymongo
from decouple import config



def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now



class ProSpider(scrapy.Spider):
    name = "pro"
    allowed_domains = ["promart.pe"]
    def __init__(self, *args, **kwargs):
        super(ProSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(config("MONGODB"))
        self.db = self.client["brand_allowed"]
        self.lista = self.brand_allowed()[int(self.b)]  # Initialize self.lista based on self.b

    def brand_allowed(self):
        collection1 = self.db["shoes"]
        collection2 = self.db["electro"]
        collection3 = self.db["tv"]
        collection4 = self.db["cellphone"]
        collection5 = self.db["laptop"]
        collection6 = self.db["consola"]
        collection7 = self.db["audio"]
        collection8 = self.db["colchon"]
        collection9 = self.db["nada"]
        collection10 = self.db["sport"]
        
        shoes = collection1.find({})
        electro = collection2.find({})
        tv = collection3.find({})
        cellphone = collection4.find({})
        laptop = collection5.find({})
        consola = collection6.find({})
        audio = collection7.find({})
        colchon = collection8.find({})
        nada = collection9.find({})
        sport = collection10.find({})


        shoes_list = [doc["brand"] for doc in shoes]
        electro_list = [doc["brand"] for doc in electro]
        tv_list = [doc["brand"] for doc in tv]
        cellphone_list = [doc["brand"] for doc in cellphone]
        laptop_list = [doc["brand"] for doc in laptop]
        consola_list = [doc["brand"] for doc in consola]
        audio_list = [doc["brand"] for doc in audio]
        colchon_list = [doc["brand"] for doc in colchon]
        nada_list = [doc["brand"] for doc in nada]
        sport_list = [doc["brand"] for doc in sport]
        return shoes_list ,electro_list,tv_list,cellphone_list,laptop_list, consola_list, audio_list, colchon_list,nada_list,sport_list
    


    def start_requests(self):
        u = int(getattr(self, 'u', '0'))
        b = int(getattr(self, 'b', '0'))

        if u == 0:
            urls = url_list.list0
      
        elif u == 1:
                urls = url_list.list1
        elif u == 2:
                urls = url_list.list2
        elif u == 3:
                urls = url_list.list3
        elif u == 4:
                urls = url_list.list4
        elif u == 10:
                urls = url_list.list10
        else:
            urls = []

        for i, v in enumerate(urls):
     
            for e in range(50):

                
        
                url = v[0]+str(e)+v[1]
                print(url)

    
                yield scrapy.Request(url, self.parse)




    def parse(self, response):
        item = PromartItem()
        productos = response.css("div.item-product.product-listado")  

        for i in productos:

            item["sku"] = i.css("div::attr(data-id)").get()
            if  item["sku"] == None:
                 continue
            #item["_id"] =  item["sku"]+str(load_datetime()[0])
            item["_id"] :str(uuid.uuid4())

            item["brand"]= i.css("div.brand.js-brand p::text").get()
            product = item["brand"]
            if self.b !=8:
                        if product.lower() not in self.lista:
                            continue
            item["product"] =i.css("input.insert-sku-quantity::attr(title)").get()
            item["link"] =i.css("a.prod-det-enlace::attr(href)").get()
            item["image"]= i.css("img::attr(src)").get()
        
            try:
                item["best_price"] = i.css("div.bestPrice div.vcenter.bestPrice.js-bestPrice span.sin-fto::text").get()
                item["best_price"] =round(float(str(item["best_price"]). strip().replace(",","").replace(" ","").replace("S/","")))

            except: item["best_price"] = 0
        
            if item["best_price"] == None:
                 item["best_price"] = 0


            # if  item["best_price"] != 0 or None:
            #     try: 
            #         item["best_price"] = str(item["best_price"]).replace(",","").replace("S/.","")
            
            #         item["best_price"] = round(float(str(item["best_price"])))
            #     except: item["best_price"] = 0
          
  


            item["list_price"]  =i.css("div.vcenter.listPrice.js-listPrice span.sin-fto::text").get()
            if item["list_price"] != None:
                item["list_price"] = round(float(str(item["list_price"]).replace(",","").replace("S/ ","")))
            else:
                   item["list_price"] =0
        

            # if item["list_price"] == None:
            #      item["list_price"] = 0



            # except: item["list_price"] = 0
            # if item["list_price"] == None:
            #      item["list_price"] = 0


            if item["best_price"] == 0:
                    item["best_price"] = i.css("span.text.fz-lg-15.fw-bold.BestPrice::text").get()
                    try:
                        item["best_price"] = round(float(str(item["best_price"]).replace(",","").replace("S/.","")))
                    except:  item["best_price"] = 0

           

          
            if item["best_price"]  and item["list_price"] !=0:
                item["web_dsct"] = 100-(float(item["best_price"])*100/float(item["list_price"]))
                item["web_dsct"] = round(float( item["web_dsct"]))
            else:
                 item["web_dsct"] = 0
                

          
            

           
            item["home_list"]=response.url
            item["card_dsct"] = 0
            item["card_price"] = 0 
            item["market"]= "promart"  # COLECCION
            item["date"] = load_datetime()[0]
            item["time"]= load_datetime()[1]


            # element = item["brand"]
            # if item["web_dsct"]>= 70 and   any(item.lower() == element.lower() for item in brand()):
                
            #         if  item["card_price"] == 0:
            #              card_price = ""
            #         else:
            #             card_price = '\n👉Precio Tarjeta :'+str(item["card_price"])

            #         if item["list_price"] == 0:
            #                 list_price = ""
            #         else:
            #             list_price = '\n\n➡️Precio Lista :'+str(item["list_price"])

            #         if item["web_dsct"] <= 50:
            #             dsct = "🟡"
            #         if item["web_dsct"] > 50 and item["web_dsct"]  <=69:
            #             dsct = "🟢"
            #         if item["web_dsct"] >=70:
            #             dsct = "🔥🔥🔥🔥🔥"

            #         message =  "✅Marca: "+str(item["brand"])+"\n✅"+str(item["product"])+list_price+"\n👉Precio web :"+str(item["best_price"])+card_price+"\n"+dsct+"Descuento: "+"% "+str(item["web_dsct"])+"\n"+"\n\n⌛"+item["date"]+" "+ item["time"]+"\n🔗Link :"+str(item["link"])+"\n🏠home web:"+item["home_list"]+"\n\n◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"
            #         foto = item["image"]

            #         send_telegram(message,foto, bot_token, chat_id)


            yield item
