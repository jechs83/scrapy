

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from wong.wong.spiders.wong import WongSpider
import subprocess


def run_spider_with_parameters( b_value):
    process = CrawlerProcess(get_project_settings())

    process.crawl(WongSpider, u=1, b=b_value)
    process.crawl(WongSpider, u=2, b=b_value)
    process.crawl(WongSpider, u=3, b=b_value)
    process.crawl(WongSpider, u=4, b=b_value)
    process.crawl(WongSpider, u=5, b=b_value)
    process.crawl(WongSpider, u=6, b=b_value)
    process.crawl(WongSpider, u=7, b=b_value)
    process.crawl(WongSpider, u=8, b=b_value)
    process.crawl(WongSpider, u=9, b=b_value)
   
    process.start()

if __name__ == "__main__":
    b_value = 4

    run_spider_with_parameters(b_value)
    subprocess.run("pkill -f 'python shop_s.py'")


