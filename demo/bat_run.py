

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from demo.spiders.saga import SagaSpider
import subprocess


def run_spider_with_parameters( b_value):
    process = CrawlerProcess(get_project_settings())

    process.crawl(SagaSpider, u=1, b=b_value)
    process.crawl(SagaSpider, u=2, b=b_value)
    process.crawl(SagaSpider, u=3, b=b_value)
    process.crawl(SagaSpider, u=4, b=b_value)
    process.crawl(SagaSpider, u=5, b=b_value)
    process.crawl(SagaSpider, u=6, b=b_value)
    process.crawl(SagaSpider, u=7, b=b_value)
    process.crawl(SagaSpider, u=8, b=b_value)
  
    process.start()

if __name__ == "__main__":
    b_value = 0

    run_spider_with_parameters(b_value)
    subprocess.run("pkill -f 'python main_bat_run.py'")


