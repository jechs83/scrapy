import scrapy
from scrapy_playwright.page import PageMethod


class ShopSpider(scrapy.Spider):
    name = "shop"
   
    def start_requests(self):
        url = "https://shopstar.pe/tecnologia/televisores?page=1"

        yield scrapy.Request(url,
                meta=dict (
                    playwright= True,
                    playwright_include_page = True,

    

                   playwright_page_coroutines = [
                       PageMethod("wait_for_selector", "div.vtex-stack-layout-0-x-stackItem.vtex-stack-layout-0-x-stackItem--summary-header.absolute.top-0.left-0.w-auto.h-auto"),
                     PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),

                        PageMethod('wait_for_selector', 'div.pr3.items-stretch.vtex-flex-layout-0-x-stretchChildrenWidth.flex')
                    ]

        ))

    async def parse(self, response): 
        yield{
            'text':response.text
        }
        pass
