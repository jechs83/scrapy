import scrapy
from tailoy.items import TailoyItem
from datetime import datetime
from datetime import date
from tailoy.settings import ROTATING_PROXY_LIST
from tailoy.spiders import url_list
import time
import uuid
import pymongo
from decouple import config





def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

class TaiSpider(scrapy.Spider):
    name = "tai"
    allowed_domains = ["tailoy.com.pe"]

    def __init__(self, *args, **kwargs):
        super(TaiSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(config("MONGODB"))
        self.db = self.client["brand_allowed"]
        self.lista = self.brand_allowed()[int(self.b)]  # Initialize self.lista based on self.b

    def brand_allowed(self):
        collection1 = self.db["todo"]
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
        for url in self.start_urls:
            return scrapy.Request(url=url, callback=self.parse,
                       meta={"proxy": "http://"+ROTATING_PROXY_LIST})
            

        u = int(getattr(self, 'u', '0'))
        b = int(getattr(self, 'b', '0'))

        if u == 1:
            urls = url_list.list1

        elif u == 3:
                urls = url_list.list3
        else:
            urls = []

        # for i, v in enumerate(urls):
        #     for e in range (300):
        #         url = v[0]+ str(e+1) 
        #         yield scrapy.Request(url, self.parse)
                
        arrays_of_urls = []  
        for i in urls:
            temp_array = []  # Create a temporary array for each iteration
            for e in range(300):
                temp_array.append(i + str(e + 1))
            arrays_of_urls.append(temp_array)  # Append the temporary array to the main list
            

        
        for url_array in arrays_of_urls:
            for url in url_array:
                yield scrapy.Request(url, callback=self.parse, meta={'url_array': url_array})

        # for i in url:
        #     for e in i:
                
        #         yield scrapy.Request(e, self.parse)

        # for i, v in enumerate(urls):
        #     for e in range(200):
        #         url = v+str(e+1)
        #         yield scrapy.Request(url, self.parse)


    def parse(self, response):

        if response.status != None :# 200 and response.xpath('//desired_data'):
            # Process the response here
            pass
        else:
            self.log(f"Invalid response for URL: {response.url}")
            url_array = response.meta.get('url_array')
            
            # Move to the next array
            next_array_index = url_array.index(response.url) + 1
            if next_array_index < len(arrays_of_urls):
                next_url_array = arrays_of_urls[next_array_index]
                yield scrapy.Request(next_url_array[0], callback=self.parse, meta={'url_array': next_url_array})
            else:
                self.log("No more arrays of URLs.")

        web_true = response.css("li.item.product.product-item").css("div.price-box.price-final_price::attr(data-product-id)").get()
        print(web_true)

        # if web_true == None:
        # # If the response status is not 200, skip processing this link and move to the next one
        #         self.logger.warning(f"Skipping URL {response.url} due to non-200 status code: {response.status}")
        #         return
        
        if web_true == None:
                # Move to the next URL in the array (since it is a "noResult" page)
                self.logger.info("Skipping this URL and moving to the next one.")
                return False
        

        item = TailoyItem()

        productos = response.css("li.item.product.product-item")

      

        for i in productos:

            item["sku"]= i.css("div.price-box.price-final_price::attr(data-product-id)").get()
            item["_id"] =i.css("div.price-box.price-final_price::attr(data-product-id)").get()
            #item["_id"] =  item["sku"]+str(load_datetime()[0])
            item["_id"] :str(uuid.uuid4())
          


            
            item["link"] = i.css("a::attr(href)").get()
            item["brand"] = i.css("div.brand-label  span::text").get()
            
            product = item["brand"]
            if product == None:
                return False
        
            

          
            # if self.lista == []:
            #     pass
            # else:
            #     if product == None:
            #         product = "sin marca"
            #     else:
            #         if product.lower() not in self.lista:
            #                 continue
                
            item["product"] = i.css("strong.product.name.product-item-name a.product-item-link::text").get()
            item["product"] = item["product"].strip()

            try:
                item["best_price"] = i.css('span.price-container span.price-wrapper span.price::text').get()
                item["best_price"] = str(item["best_price"]).replace("S/","").replace(",","")
                item["best_price"]= float(item["best_price"])
            except: item["best_price"] = 0

   
        
            try:
                item["list_price"] = i.css('span.old-price span.price-container.price-final_price.tax.weee span.price-wrapper span.price::text').get()

                item["list_price"] = str(item["list_price"]).replace("S/","").replace(",","")
                item["list_price"] = float(item["list_price"] )
            except: item["list_price"] = None

            if item["list_price"] == None:
                try:
                    item["list_price"] = i.css("span.price-container.price-final_price.tax.weee").get()
                    item["list_price"] = str(item["list_price"]).replace("S/","") .replace(",","")
                    item["list_price"] = float(item["list_price"])
                except: item["list_price"] = 0

            item["image"] = i.css("img::attr(src)").get()

            try:
                item["web_dsct"] = i.css("span.discount-value::text").get()
                item["web_dsct"] = round(float(str(item["web_dsct"]).replace("-","").replace("%","")))
            except:
                item["web_dsct"] = 0


            item["market"]= "tailoy"
            item["date"] =load_datetime()[0]
            item["time"] = load_datetime()[1]
            item["home_list"] = response.url
            item["card_price"] = 0
            item["card_dsct"] = 0





            yield item
            