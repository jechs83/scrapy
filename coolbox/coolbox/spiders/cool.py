import scrapy
from coolbox.items import CoolboxItem
from datetime import datetime
from datetime import date
from coolbox.spiders import url_list 
import time
import logging



class CoolboxSpider(scrapy.Spider):
    name = 'cool'
    allowed_domains = ['coolbox.pe']
    start_urls = ['https://www.coolbox.pe/audio?page=27']

    def parse(self, response):
        products = response.xpath("//div[@class='col-md-3 col-sm-4 col-xs-6 product-grid-item']")
        for product in products:
            print(product)
            yield {
                'name': product.xpath(".//h4/a/text()").get(),
                'price': product.xpath(".//div[@class='price']/span/text()").get(),
                'link': product.xpath(".//h4/a/@href").get()
            
            }



