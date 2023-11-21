import scrapy


class RpSpider(scrapy.Spider):
    name = "rp"
    allowed_domains = ["rappi.com.pe"]
    start_urls = ["http://rappi.com.pe/"]

    def start_requests(self):
        # u = int(getattr(self, 'u', '0'))
        # b = int(getattr(self, 'b', '0'))
        # urls = links()[int(u-1)]
        url = "https://www.rappi.com.pe/tiendas/33820-darkstores-nc"
        # for i, v in enumerate(urls):
        #     for e in range (v[1]+10):
        #         url = v[0]+"?&optionOrderBy=OrderByScoreDESC&O=OrderByScoreDESC&page="+str(e+1)
        yield scrapy.Request(url, self.parse)

    def parse(self, response):

        productos = response.xpath('//div[@data-qa="product-item-2091997788"]') 

        print(productos)


        for i in productos:
            print(i)
        pass

