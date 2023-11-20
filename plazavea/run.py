

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from plazavea.spiders.vea import VeaSpider

def run_spider_with_parameters( b_value):
    process = CrawlerProcess(get_project_settings())

    process.crawl(VeaSpider, u=1, b=b_value)
    process.crawl(VeaSpider, u=2, b=b_value)
    process.crawl(VeaSpider, u=3, b=b_value)
    process.crawl(VeaSpider, u=4, b=b_value)
    process.crawl(VeaSpider, u=5, b=b_value)
    process.crawl(VeaSpider, u=6, b=b_value)
    process.crawl(VeaSpider, u=7, b=b_value)
    process.crawl(VeaSpider, u=8, b=b_value)

   

    process.start()

if __name__ == "__main__":
    b_value = 0
   
    run_spider_with_parameters(b_value)
    

