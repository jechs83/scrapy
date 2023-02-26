import scrapy
import requests
from bs4 import BeautifulSoup


response = requests.get('https://www.example.com')
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    data = soup.find("script")

    for i in data:
        print(i.text)

        
    # Extract the text from the HTML
    text = soup.get_text()
    print(text)



class OhSpider(scrapy.Spider):
    name = "oh"
    allowed_domains = ["oechsle.pe"]
    start_urls = ["http://oechsle.pe/"]

    def parse(self, response):
        pass
