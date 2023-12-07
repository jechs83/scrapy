

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from tailoy.spiders.tai import TaiSpider



def run_spider_with_parameters( b_value):
    process = CrawlerProcess(get_project_settings())

    process.crawl(TaiSpider, u=1, b=b_value)
    process.crawl(TaiSpider, u=2, b=b_value)
    process.crawl(TaiSpider, u=3, b=b_value)


   

    process.start()

if __name__ == "__main__":
    b_value = 0
   
    run_spider_with_parameters(b_value)
    

