import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, date
import uuid
import pymongo
import time
from decouple import config

client = pymongo.MongoClient(config("MONGODB"))
db = client["brand_allowed"]

def load_datetime():
    today = date.today()
    now = datetime.now()
    date_now = today.strftime("%d/%m/%Y")
    time_now = now.strftime("%H:%M:%S")
    return date_now, time_now, today
def saga_spider():
    allowed_domains = ["falabella.com.pe"]
    
    # Define a function to get the list of allowed brands
    def brand_allowed():
        collection1 = db["shoes"]
        collection2 = db["electro"]
        # ... Define other collections for TV, cellphone, laptop, etc.
        
        shoes = collection1.find({})
        electro = collection2.find({})
        # ... Retrieve data from other collections
        
        shoes_list = [doc["brand"] for doc in shoes]
        electro_list = [doc["brand"] for doc in electro]
        # ... Create lists for other categories
        
        return shoes_list, electro_list, # ... Return lists for other categories

    # Start scraping here
    u = 0  # Set the value of 'u' as needed
    b = 0  # Set the value of 'b' as needed

    # Define the URL mapping
    url_mapping = {
        1: url_list.list1, 2: url_list.list2, 3: url_list.list3, 4: url_list.list4, 5: url_list.list5, 6: url_list.list6,
        # ... Define URL lists for other values of 'u'
    }

    # Retrieve the appropriate list based on the value of 'u'
    urls = url_mapping.get(u, [])

    for url_data in urls:
        url, page_count = url_data

        if "tottus" in url:
            for e in range(page_count + 10):
                url = f"{url}?subdomain=tottus&page={e + 1}&store=tottus"
                scrape_page(url)

        if "sodimac" in url:
            for e in range(page_count + 10):
                url = f"{url}?subdomain=sodimac&page={e + 1}&store=sodimac"
                scrape_page(url)
        else:
            for e in range(page_count + 10):
                url = f"{url}?page={e + 1}"
                scrape_page(url)

def scrape_page(url):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Skipping URL {url} due to non-200 status code: {response.status_code}")
        return

    if "/noResult" in response.url:
        print("Skipping this URL and moving to the next one.")
        return

    page_props = None
    script_tag = None

    try:
        script_tag = json.loads(
            BeautifulSoup(response.content, "html.parser").find("script", id="__NEXT_DATA__").text
        )
        page_props = script_tag.get('props', {}).get('pageProps', {}).get("results", {})
    except Exception as e:
        print(f"Failed to parse JSON data from {url}: {str(e)}")

    if page_props:
        for product_data in page_props:
            brand = product_data.get("brand", None)
            if brand:
                # Check if the brand should be skipped

                product = product_data.get("displayName", None)
                sku = product_data.get("skuId", None)
                _id = str(uuid.uuid4())

                best_price = 0
                list_price = 0
                card_price = 0

                try:
                    best_price = float(product_data["prices"][1]["price"][0].replace(",", ""))
                except:
                    pass

                try:
                    list_price = float(product_data["prices"][2]["price"][0].replace(",", ""))
                except:
                    pass

                try:
                    card_price = float(product_data["prices"][0]["price"][0].replace(",", ""))
                except:
                    pass

                link = product_data.get("url", None)
                image = product_data.get("mediaUrls", None)

                web_dsct = 0

                try:
                    web_dsct = float(product_data["discountBadge"]["label"].replace("-", "").replace("%", ""))
                except:
                    pass

                market = "saga"
                date = load_datetime()[0]
                time = load_datetime()[1]
                home_list = url
                card_dsct = 0

                # Print or store the data as needed
                print(f"Brand: {brand}")
                print(f"Product: {product}")
                print(f"SKU: {sku}")
                print(f"Best Price: {best_price}")
                print(f"List Price: {list_price}")
                print(f"Card Price: {card_price}")
                print(f"Link: {link}")
                print(f"Image: {image}")
                print(f"Web Discount: {web_dsct}")
                print(f"Market: {market}")
                print(f"Date: {date}")
                print(f"Time: {time}")
                print(f"Home List: {home_list}")
                print(f"Card Discount: {card_dsct}")
                print("\n")

saga_spider()



https://www.metro.pe/
_v/segment/graphql/v1?workspace=master&maxAge=short&appsEtag=remove&domain=store&locale=es-PE&operationName=
productSearchV3&variables=
%7B%7D&extensions=%7B"persistedQuery"%3A%7B"version"%3A1%2C"sha256Hash"%3A"40b843ca1f7934d20d05d334916220a0c2cae3833d9f17bcb79cdd2185adceac"
%2C"sender"%3A"vtex.store-resources%400.x"%2C"provider"%3A"vtex.search-graphql%400.x"%7D%2C
"variables"%3A"eyJoaWRlVW5hdmFpbGFibGVJdGVtcyI6dHJ1ZSwic2t1c0ZpbHRlciI6IkFMTCIsInNpbXVsYXRpb25CZWhhdmlvciI6ImRlZmF1bHQiLCJpbnN0YWxsbWVudENyaXRlcmlhIjoiTUFYX1dJVEhPVVRfSU5URVJFU1QiLCJwcm9kdWN0T3JpZ2luVnRleCI6ZmFsc2UsIm1hcCI6ImMiLCJxdWVyeSI6ImVsZWN0cm9ob2dhciIsIm9yZGVyQnkiOiJPcmRlckJ5U2NvcmVERVNDIiwiZnJvbSI6NjAsInRvIjoxMTksInNlbGVjdGVkRmFjZXRzIjpbeyJrZXkiOiJjIiwidmFsdWUiOiJlbGVjdHJvaG9nYXIifV0sIm9wZXJhdG9yIjoiYW5kIiwiZnV6enkiOiIwIiwic2VhcmNoU3RhdGUiOm51bGwsImZhY2V0c0JlaGF2aW9yIjoiU3RhdGljIiwiY2F0ZWdvcnlUcmVlQmVoYXZpb3IiOiJkZWZhdWx0Iiwid2l0aEZhY2V0cyI6ZmFsc2UsInZhcmlhbnQiOiIifQ%3D%3D"%7D

"eyJoaWRlVW5hdmFpbGFibGVJdGVtcyI6dHJ1ZSwic2t1c0ZpbHRlciI6IkFMTCIsInNpbXVsYXRpb25CZWhhdmlvciI6ImRlZmF1bHQiLCJpbnN0YWxsbWVudENyaXRlcmlhIjoiTUFYX1dJVEhPVVRfSU5URVJFU1QiLCJwcm9kdWN0T3JpZ2luVnRleCI6ZmFsc2UsIm1hcCI6ImMiLCJxdWVyeSI6ImVsZWN0cm9ob2dhciIsIm9yZGVyQnkiOiJPcmRlckJ5U2NvcmVERVNDIiwiZnJvbSI6NjAsInRvIjoxMTksInNlbGVjdGVkRmFjZXRzIjpbeyJrZXkiOiJjIiwidmFsdWUiOiJlbGVjdHJvaG9nYXIifV0sIm9wZXJhdG9yIjoiYW5kIiwiZnV6enkiOiIwIiwic2VhcmNoU3RhdGUiOm51bGwsImZhY2V0c0JlaGF2aW9yIjoiU3RhdGljIiwiY2F0ZWdvcnlUcmVlQmVoYXZpb3IiOiJkZWZhdWx0Iiwid2l0aEZhY2V0cyI6ZmFsc2UsInZhcmlhbnQiOiIifQ%3D%3D"