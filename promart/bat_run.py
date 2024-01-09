

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from promart.spiders.pro import ProSpider

def run_spider_with_parameters( b_value):
    process = CrawlerProcess(get_project_settings())

    process.crawl(ProSpider, u=1, b=b_value)


   

    process.start()

if __name__ == "__main__":
    b_value = 0
   
    run_spider_with_parameters(b_value)
    

