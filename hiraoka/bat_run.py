

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from hiraoka.spiders.hira import HiraSpider
import subprocess


def run_spider_with_parameters( b_value):
    process = CrawlerProcess(get_project_settings())

    process.crawl(HiraSpider, u=1, b=b_value)
    process.crawl(HiraSpider, u=2, b=b_value)
    process.crawl(HiraSpider, u=3, b=b_value)

    process.start()

if __name__ == "__main__":
    b_value = 0

    run_spider_with_parameters(b_value)
    subprocess.run("pkill -f 'python main_bat_run.py'")


