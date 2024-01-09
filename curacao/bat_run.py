

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from curacao.spiders.cura import CuraSpider
import subprocess

def run_spider_with_parameters(b_value):
    process = CrawlerProcess(get_project_settings())

    process.crawl(CuraSpider, u=1, b=b_value)
    process.crawl(CuraSpider, u=2, b=b_value)
    process.crawl(CuraSpider, u=3, b=b_value)
    process.crawl(CuraSpider, u=4, b=b_value)
    process.crawl(CuraSpider, u=5, b=b_value)
    process.crawl(CuraSpider, u=6, b=b_value)
    process.crawl(CuraSpider, u=7, b=b_value)
    process.crawl(CuraSpider, u=8, b=b_value)
    process.crawl(CuraSpider, u=9, b=b_value)
    process.crawl(CuraSpider, u=10, b=b_value)


    # Add more process.crawl() calls for other values of 'u' if needed
    
    process.start()

if __name__ == "__main__":
    b_value = 0

    run_spider_with_parameters(b_value)

