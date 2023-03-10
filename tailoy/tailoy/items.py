# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TailoyItem(scrapy.Item):
    # define the fields for your item here like:

    sku= scrapy.Field()
    _id = scrapy.Field()
    product = scrapy.Field()
    brand = scrapy.Field()
    best_price = scrapy.Field()
    list_price = scrapy.Field()
    web_dsct = scrapy.Field()
    link = scrapy.Field()
    image = scrapy.Field()
    product = scrapy.Field()
    market= scrapy.Field()
    date =scrapy.Field()
    time = scrapy.Field()
    home_list = scrapy.Field()
    card_price = scrapy.Field()
    card_dsct = scrapy.Field()
  
    pass
