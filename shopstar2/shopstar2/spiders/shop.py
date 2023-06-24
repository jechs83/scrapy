import scrapy
from scrapy_playwright.page import PageMethod
import time

class ShopSpider(scrapy.Spider):
    name = "shop"
   
    def start_requests(self):
        url = "https://shopstar.pe/tecnologia/televisores?page=1"

        yield scrapy.Request(url,
                meta=dict (
                    playwright= True,
                    playwright_include_page = True,
                    playwright_page_methods= [
                        PageMethod("wait_for_timeout", 5000),  # Wait for 2 seconds after navigation
                        PageMethod("wait_for_selector", "div.vtex-button__label.flex.items-center.justify-center.h-100.ph5"),
                        

                        PageMethod("evaluate", "window.scrollTo(0, document.body.scrollHeight)"),

                        # PageMethod("wait_for_selector", "//div[24]/section[1]/a[1]/article[1]")

                    ],
                  

        ))

    


    async def parse(self, response): 
        yield{
            'text':response.text
        }
        pass

