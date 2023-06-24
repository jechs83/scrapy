import scrapy


class JunSpider(scrapy.Spider):
    name = "jun"
    allowed_domains = ["juntoz.com"]
    start_urls = ["http://juntoz.com/"]

    def parse(self, response):
        pass
