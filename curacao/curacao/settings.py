# Scrapy settings for demo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from decouple import config

BOT_NAME = "curacao"

SPIDER_MODULES = ["curacao.spiders"]
NEWSPIDER_MODULE = "curacao.spiders"

ITEM_PIPELINES = {
    'curacao.pipelines.MongoPipeline': 300,
}

RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408, 429]

# Set the maximum number of retries for each request
RETRY_TIMES = 3  # Adjust this value as needed
MONGO_URI = config("MONGODB")
# MONGO_DATABASE = config("db_curacao")
# COLLECTION_NAME = config("collection")
MONGO_DATABASE = "curacao"
COLLECTION_NAME = "scrap"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "demo (+http://www.yourdomain.com)"

# Obey robots.txt rules
#ROBOTSTXT_OBEY = True
#USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'

USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'



# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32
# LOG_ENABLED = True
# LOG_LEVEL = 'DEBUG'
# LOG_FILE = 'scrapy.log'

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "demo.middlewares.DemoSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "demo.middlewares.DemoDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "demo.pipelines.DemoPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value




# ROTATING_PROXY_LIST = [
# "45.190.170.254:999",
# "177.53.154.5:999",
# "190.43.232.122:999",
# "45.189.118.232:999",
# "38.252.209.96:999",
# "200.60.4.238:999",
# "181.65.196.153:999",
# "190.119.211.74:8080",
# "179.43.93.198:8080",
# "200.106.124.10:999",
# "190.12.95.170:47029",
# "179.43.96.178:8080",
# "179.49.156.26:999",
# "181.65.200.53:80",
# "209.45.40.34:999",
# "170.79.36.60:8081",
# "168.194.171.241:999",
# "190.102.149.74:999",
# "161.132.172.24:999",
# "190.102.139.150:999",
# "190.119.68.142:999",
# "161.132.48.32:8080",
# "45.236.44.94:8080",
# "200.37.107.197:999",
# "190.239.220.6:999",
# "161.132.125.244:8080",
# "181.65.180.188:999",
# "200.106.116.26:999",
# "190.239.205.91:999",
# "190.239.205.91:999",
# "190.239.205.91:999",
# "190.239.205.91:999",

# ]
