

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from coolbox.spiders.cool import CoolboxSpider
import subprocess


def run_spider_with_parameters( b_value):
    process = CrawlerProcess(get_project_settings())

    process.crawl(CoolboxSpider, u=1, b=b_value)

    process.start()

if __name__ == "__main__":
    b_value = 0

    run_spider_with_parameters(b_value)
    subprocess.run("pkill -f 'python main_bat_run.py'")


