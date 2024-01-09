

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from ripley.spiders.ripple_scrap import RippleScrapSpider
import subprocess


def run_spider_with_parameters( b_value):
    process = CrawlerProcess(get_project_settings())

    process.crawl(RippleScrapSpider, u=1, b=b_value)
    process.crawl(RippleScrapSpider, u=2, b=b_value)
    process.crawl(RippleScrapSpider, u=3, b=b_value)
    process.crawl(RippleScrapSpider, u=4, b=b_value)
    process.crawl(RippleScrapSpider, u=5, b=b_value)
    process.crawl(RippleScrapSpider, u=6, b=b_value)
    process.crawl(RippleScrapSpider, u=7, b=b_value)
    process.crawl(RippleScrapSpider, u=8, b=b_value)
    process.crawl(RippleScrapSpider, u=9, b=b_value)
    process.crawl(RippleScrapSpider, u=10, b=b_value)
    process.crawl(RippleScrapSpider, u=11, b=b_value)
    process.crawl(RippleScrapSpider, u=12, b=b_value)
    process.crawl(RippleScrapSpider, u=13, b=b_value)
    process.crawl(RippleScrapSpider, u=14, b=b_value)
    process.crawl(RippleScrapSpider, u=15, b=b_value)
    process.crawl(RippleScrapSpider, u=16, b=b_value)
    process.crawl(RippleScrapSpider, u=17, b=b_value)
    process.crawl(RippleScrapSpider, u=18, b=b_value)
    process.crawl(RippleScrapSpider, u=19, b=b_value)
    process.crawl(RippleScrapSpider, u=20, b=b_value)

    process.start()

if __name__ == "__main__":
    b_value = 0

    run_spider_with_parameters(b_value)
    subprocess.run("pkill -f 'python bat_run.py'")


