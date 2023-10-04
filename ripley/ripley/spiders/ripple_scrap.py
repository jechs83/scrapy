import scrapy
import time
from ripley.spiders import url_list 
import scrapy
from ripley.items import RipleyItem
from datetime import datetime
from datetime import date
import random


def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

class RippleScrapSpider(scrapy.Spider):
    name = "ripley_scrap"

    user_agents = [

        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/80.0.361.62",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140",
        # Add more user-agent strings here
    ]
    
    links =[]
    def start_requests(self):
        u = int(getattr(self, 'u', '0'))
        if u == 1:
            urls = url_list.list1
        elif u == 2:
                urls = url_list.list2
        elif u == 3:
                urls = url_list.list3
        elif u == 4:
                urls = url_list.list4
        elif u == 0:
                urls = url_list.list0

        elif u == 100:
                urls = url_list.list100
        elif u == 200:
                urls = url_list.list200
        elif u == 300:
                urls = url_list.list300
        elif u == 400:
                urls = url_list.list400
        elif u == 500:
                urls = url_list.list500


        else:
            urls = []



        for i, v in enumerate(urls):
            for e in range((round(v[1]/48)+1)):
                url = v[0] + str(e + 1)      
                # Select a random user-agent
                user_agent = random.choice(self.user_agents)

                headers = {'User-Agent': user_agent}

                yield scrapy.Request(url, self.parse, headers=headers   )
                #yield scrapy.Request(url, self.parse)

                # proxy = random_proxy()
            
              

                # # Use the obtained proxy in the request
                # yield scrapy.Request(url, self.parse, meta={'proxy': proxy})

            
    def parse(self, response):
            item = RipleyItem()
            productos = response.css("div.catalog-product-item.catalog-product-item__container.col-xs-6.col-sm-6.col-md-4.col-lg-4")

            for i in productos:
            
                item["brand"] = i.css('div.brand-logo span::text').get()
                if item["brand"] == None:
                    item["brand"] = "Revisar codigo"
                
                try:
                    item["product"] = i.css(".catalog-product-details__name::text").get()
                except: item["product"] = None

                try:
                    item["image"] = i.css("img::attr(data-src)").get()
                except:  item["image"] = None

                image_start = item["image"][:6]
                if image_start != "https:":
                    item["image"] = "https:" + item["image"]

                item["sku"] = i.css(".catalog-product-item.catalog-product-item__container.undefined::attr(id)").get()
                item["sku"] = str( item["sku"])
                item["sku"] = item["sku"][:-1]

                item["_id"] =  item["sku"]+str(load_datetime()[0])
                
                try:
                    item["web_dsct"] = round(float(i.css(".catalog-product-details__discount-tag::text").get().replace("-", "").replace("%", "")))
                except:
                    item["web_dsct"] = 0
                
                try:
                    item["list_price"] = i.css(".catalog-prices__list-price.catalog-prices__lowest.catalog-prices__line_thru::text").get().replace("S/", "").replace(",", "")
                except:
                    item["list_price"] = 0

                try:
                    item["best_price"] = i.css(".catalog-prices__offer-price::text").get().strip().replace("S/", "").replace(",", "")
                except:
                    item["best_price"] = 0

                try:
                    item["card_price"] = i.css(".catalog-prices__card-price::text").get().replace("S/", "").replace(",", "")
                except:
                    item["card_price"] = 0

                item["list_price"]     = float(item["list_price"] )
                item["best_price"]     = float(item["best_price"] )
                item["web_dsct"]     = float(item["web_dsct"] )

                item["link"] = i.css(".catalog-product-item.catalog-product-item__container.undefined::attr(href)").get()
                item["link"] = "https://simple.ripley.com.pe" + item["link"]
                item["card_dsct"] = 0
                item["market"]= "ripley"
                item["date"]= load_datetime()[0]
                item["time"]= load_datetime()[1]
                item["home_list"] = response.url       
            
                yield item


            time.sleep(0.8)
