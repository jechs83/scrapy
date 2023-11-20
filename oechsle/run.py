

# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# from oechsle.spiders.oh import OhSpider
# from decouple import config

# def run_spider_with_parameters( b_value):
#     process = CrawlerProcess(get_project_settings())

#     process.crawl(OhSpider, u=1, b=b_value)
#     process.crawl(OhSpider, u=2, b=b_value)
#     process.crawl(OhSpider, u=3, b=b_value)
#     process.crawl(OhSpider, u=4, b=b_value)
#     process.crawl(OhSpider, u=5, b=b_value)
#     process.crawl(OhSpider, u=6, b=b_value)
#     process.crawl(OhSpider, u=7, b=b_value)
#     process.crawl(OhSpider, u=8, b=b_value)
#     process.crawl(OhSpider, u=9, b=b_value)
#     process.crawl(OhSpider, u=10, b=b_value)
#     process.crawl(OhSpider, u=11, b=b_value)
#     process.crawl(OhSpider, u=12, b=b_value)
    
#     process.start()

# if __name__ == "__main__":
    
#     b_value = 0
   
#     run_spider_with_parameters( b_value)
    

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from oechsle.spiders.oh import OhSpider

def run_spider_with_parameters(b_value):
    process = CrawlerProcess(get_project_settings())

    process.crawl(OhSpider, u=1, b=b_value)
    process.crawl(OhSpider, u=2, b=b_value)
    process.crawl(OhSpider, u=3, b=b_value)
    process.crawl(OhSpider, u=4, b=b_value)
    process.crawl(OhSpider, u=5, b=b_value)
    process.crawl(OhSpider, u=6, b=b_value)
    process.crawl(OhSpider, u=7, b=b_value)
    process.crawl(OhSpider, u=8, b=b_value)
    process.crawl(OhSpider, u=9, b=b_value)
    process.crawl(OhSpider, u=10, b=b_value)
    process.crawl(OhSpider, u=11, b=b_value)
    process.crawl(OhSpider, u=12, b=b_value)
    
    process.start()

if __name__ == "__main__":
    b_value = 0
    while True:  # Infinite loop
        try:
            run_spider_with_parameters(b_value)
        except:
            run_spider_with_parameters(b_value)



    