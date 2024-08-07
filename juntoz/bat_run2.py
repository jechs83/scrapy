

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from juntoz.spiders.jun import JunSpider
import subprocess


def run_spider_with_parameters( b_value):
    process = CrawlerProcess(get_project_settings())

    process.crawl(JunSpider, u=30, b=b_value)

  
    process.start()

if __name__ == "__main__":
    b_value = 1

    run_spider_with_parameters(b_value)
    subprocess.run("pkill -f 'python main_bat_run.py'")


