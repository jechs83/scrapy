import aiohttp
import asyncio
import json
import random
from pymongo import MongoClient
from fake_useragent import UserAgent

# Database connection
client = MongoClient("mongodb://192.168.1.66:27017")
db = client['ripley']
collection = db['productos']

# Base URLs
base_urls = [
    "https://simple.ripley.com.pe/tecnologia/tv-y-cine-en-casa/televisores?source=menu&page={}&s=mdco",
    # Add other URLs as required...
]

# Random user agent
user_agent = UserAgent()

async def fetch(session, url):
    headers = {'User-Agent': user_agent.random, 'Referer': 'https://simple.ripley.com.pe/', 'Accept-Encoding': 'gzip, deflate, br'}
    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            return await response.text()
    except aiohttp.ClientResponseError as e:
        print(f"HTTP Error for {url}: {e.status}")
    except aiohttp.ClientError as e:
        print(f"Client Error for {url}: {str(e)}")
    return None

async def process_page(url, session, retry_delay=10, max_retries=5):
    try:
        response = await fetch(session, url)
        if response.status == 429:
            retry_after = response.headers.get('Retry-After', retry_delay)
            print(f"Rate limit reached, retrying after {retry_after} seconds...")
            await asyncio.sleep(int(retry_after))
            if max_retries > 0:
                print(f"Retrying {url}...")
                return await process_page(url, session, retry_delay * 2, max_retries - 1)
            else:
                print("Max retries exceeded.")
                return None
        json_match = re.search(r'window\.__PRELOADED_STATE__\s*=\s*({.*?})\s*;\s*<\/script>', await response.text())
        # Process the data...
        # Your existing data processing logic here.
    except aiohttp.ClientError as e:
        print(f"HTTP error while processing {url}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Update your asyncio.gather or task creation to handle retries properly.


async def crawl_base_url(base_url):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(process_page(base_url.format(page), session)) for page in range(1, 50)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                print(f"Error encountered: {result}")

async def main():
    # Process each base URL concurrently
    await asyncio.gather(*(crawl_base_url(url) for url in base_urls))

if __name__ == "__main__":
    asyncio.run(main())
