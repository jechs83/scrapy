

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from hiraoka.spiders.hira import HiraSpider
import subprocess


def run_spider_with_parameters( b_value):
    process = CrawlerProcess(get_project_settings())

    process.crawl(HiraSpider, u=1, b=b_value)
    process.crawl(HiraSpider, u=2, b=b_value)
    process.crawl(HiraSpider, u=3, b=b_value)
    # process.crawl(HiraokaItem, u=4, b=b_value)
    # process.crawl(HiraokaItem, u=5, b=b_value)
    # process.crawl(HiraokaItem, u=6, b=b_value)
    # process.crawl(HiraokaItem, u=7, b=b_value)
    # process.crawl(HiraokaItem, u=8, b=b_value)
    # process.crawl(HiraokaItem, u=9, b=b_value)
    # process.crawl(HiraokaItem, u=10, b=b_value)
    # process.crawl(HiraokaItem, u=11, b=b_value)
    # process.crawl(HiraokaItem, u=12, b=b_value)
    # process.crawl(HiraokaItem, u=13, b=b_value)
    # process.crawl(HiraokaItem, u=14, b=b_value)
    # process.crawl(HiraokaItem, u=15, b=b_value)
    # process.crawl(HiraokaItem, u=16, b=b_value)
    # process.crawl(HiraokaItem, u=17, b=b_value)
    # process.crawl(HiraokaItem, u=18, b=b_value)
    # process.crawl(HiraokaItem, u=19, b=b_value)
    # process.crawl(HiraokaItem, u=20, b=b_value)

    process.start()

if __name__ == "__main__":
    b_value = 0

    run_spider_with_parameters(b_value)
    subprocess.run("pkill -f 'python saga_s.py'")

