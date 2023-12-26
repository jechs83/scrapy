

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from shopstar.spiders.shop import ShopSpider

import subprocess


def run_spider_with_parameters( b_value):
    process = CrawlerProcess(get_project_settings())

   
    process.crawl(ShopSpider, u=1, b=b_value)
    process.crawl(ShopSpider, u=2, b=b_value)
 

   
 
    process.start()

if __name__ == "__main__":
    b_value = 4

    run_spider_with_parameters(b_value)
    subprocess.run("pkill -f 'python test_s.py'")


