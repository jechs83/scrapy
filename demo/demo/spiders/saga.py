import scrapy
import sys
import json
from demo.items import DemoItem
from datetime import datetime, date
import pymongo
from demo.spiders.urls_db import links
from decouple import config
import time

def load_datetime():
    today = date.today()
    now = datetime.now()
    date_now = today.strftime("%d/%m/%Y")  
    time_now = now.strftime("%H:%M:%S")
    return date_now, time_now, today

current_day = load_datetime()[0]

class SagaSpider(scrapy.Spider):
    name = "saga"
    allowed_domains = ["falabella.com.pe"]
    handle_httpstatus_list = [200, 206]

    def __init__(self, *args, **kwargs):
        u = int(getattr(self, 'u', '0'))
        b = int(getattr(self, 'b', '0'))
        super(SagaSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(config("MONGODB"))
        self.db = self.client["brand_allowed"]
        self.lista = self.brand_allowed()  # Initialize self.lista based on self.b
        self.urls = links()[int(int(self.u)-1)]
    
    def brand_allowed(self):
        collection1 = self.db["todo"]
        shoes = collection1.find({})
        shoes_list = [doc["brand"] for doc in shoes]
        collection1 = self.db["nada"]
        nada = collection1.find({})
        return shoes_list, nada

    def start_requests(self):
        for i, v in enumerate(self.urls):
            url = v[0]
            yield scrapy.Request(url, self.parse, meta={'base_url': url, 'subdomain': self.get_subdomain(url), 'page': 1})

    def get_subdomain(self, url):
        if "tottus" in url:
            return "tottus"
        elif "sodimac" in url:
            return "sodimac"
        return ""

    def parse(self, response):
        if response.status != 200:
            self.logger.warning(f"Skipping URL {response.url} due to non-200 status code: {response.status}")
            return

        if "/noResult" in response.url:
            self.logger.info("Skipping this URL and moving to the next one.")
            return

        base_url = response.meta['base_url']
        subdomain = response.meta['subdomain']
        current_page = response.meta['page']

        item = DemoItem()
        script_tag = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()

        if script_tag:
            json_content = json.loads(script_tag)
            page_props = json_content.get('props', {}).get('pageProps', {}).get("results",{})
        else:
            page_props = {}

        productos = page_props
        
        for i in productos:
            item["brand"] = i["brand"]
            producto = item["brand"].lower()

            if self.lista[0] == []:
                pass
            else:
                if producto not in self.lista[0]:
                    continue

            item["product"] = i["displayName"]
            item["sku"] = i["skuId"]
            item["_id"] = i["skuId"]

            prices = i["prices"]
            if len(prices) == 1:
                item["best_price"] = 0
                item["card_price"] = 0
                item["list_price"] = float(prices[0]["price"][0].replace(",", ""))
            elif len(prices) == 2:
                item["best_price"] = float(prices[0]["price"][0].replace(",", ""))
                item["card_price"] = 0
                item["list_price"] = float(prices[1]["price"][0].replace(",", ""))
            elif len(prices) == 3:
                item["best_price"] = float(prices[1]["price"][0].replace(",", ""))
                item["card_price"] = float(prices[0]["price"][0].replace(",", ""))
                item["list_price"] = float(prices[2]["price"][0].replace(",", ""))

            item["link"] = i["url"]
            item["image"] = i.get("mediaUrls", [None])[0]
            item["web_dsct"] = float(i.get("discountBadge", {}).get("label", "0").replace("-", "").replace("%", ""))
            item["dsct_app"] = 1 if i.get("multipurposeBadges", [{}])[0].get("label") == "Dscto extra por app" else 0

            if not (item["list_price"] or item["card_price"] or item["best_price"]):
                continue

            item["market"] = "saga"
            item["date"] = load_datetime()[0]
            item["time"] = load_datetime()[1]
            item["home_list"] = response.url
            item["card_dsct"] = 0

            yield item

        # Detectar el número máximo de páginas si no está ya en los meta datos
        if 'max_pages' not in response.meta:
            max_pages = self.get_max_pages(response)
            if max_pages:
                response.meta['max_pages'] = max_pages
            else:
                return

        # Obtener el número máximo de páginas desde los meta datos
        max_pages = response.meta['max_pages']

        # Continuar a la siguiente página si no se ha alcanzado el número máximo de páginas
        if current_page < max_pages:
            next_page = current_page + 1
            next_page_url = f"{base_url}?subdomain={subdomain}&page={next_page}&store={subdomain}" if subdomain else f"{base_url}?page={next_page}"
            yield scrapy.Request(next_page_url, self.parse, meta={'base_url': base_url, 'subdomain': subdomain, 'page': next_page, 'max_pages': max_pages})

    def get_max_pages(self, response):
        pagination = response.xpath('//ul[@class="pagination"]/li/a/text()').extract()
        if pagination:
            try:
                max_page = max(int(num) for num in pagination if num.isdigit())
                return max_page
            except ValueError:
                return None
        return None

# Para ejecutar el spider, guarda este código en un archivo llamado `saga_spider.py` y usa el comando:
# scrapy runspider saga_spider.py
