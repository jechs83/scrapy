

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
    process.crawl(SagaSpider, u=9, b=b_value)
    process.crawl(SagaSpider, u=10, b=b_value)
    process.crawl(SagaSpider, u=11, b=b_value)
    process.crawl(SagaSpider, u=12, b=b_value)
    process.crawl(SagaSpider, u=13, b=b_value)
    process.crawl(SagaSpider, u=14, b=b_value)
    process.crawl(SagaSpider, u=15, b=b_value)
    process.crawl(SagaSpider, u=16, b=b_value)
    process.crawl(SagaSpider, u=17, b=b_value)
    process.crawl(SagaSpider, u=18, b=b_value)
    process.crawl(SagaSpider, u=19, b=b_value)
    process.crawl(SagaSpider, u=20, b=b_value)

    process.start()

if __name__ == "__main__":
    b_value = 0

    run_spider_with_parameters(b_value)
    subprocess.run("pkill -f 'python saga_s.py'")

