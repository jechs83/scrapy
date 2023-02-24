# Scrapy settings for demo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "metro"
COLLECTION_NAME = "scrap"
SPIDER_MODULES = ["metro.spiders"]
NEWSPIDER_MODULE = "metro.spiders"

ITEM_PIPELINES = {
    'metro.pipelines.MongoPipeline': 300,
}
MONGO_URI = 'mongodb://superuser:Viper.2013@192.168.9.66:27017/?authMechanism=DEFAULT&tls=false'

MONGO_DATABASE = 'scrap'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "demo (+http://www.yourdomain.com)"

# Obey robots.txt rules
#ROBOTSTXT_OBEY = True
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
#DOWNLOAD_DELAY = 1

#USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'


# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

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
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


DOWNLOADER_MIDDLEWARES = {
    # ...
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    # ...
}
ROTATING_PROXY_LIST = [
"108.61.191.222:1994",
"204.137.250.6:3129",
"3.208.13.0:9999",
"54.226.196.225:9999",
"5.161.48.72:8080",
"145.40.103.113:3128",
"20.241.236.196:3128",
"172.245.242.5:3128",
"159.223.206.101:3128",
"172.245.248.46:3128",
"104.223.135.178:10000",
"198.148.104.93:1994",
"173.82.12.238:1994",
"198.211.55.167:1994",
"173.82.12.10:1994",
"108.166.203.110:1994",
"104.194.232.179:1994",
"135.84.142.94:3128",
"173.82.20.178:1994",
"35.85.253.80:80",
"179.49.113.230:999",
"216.127.188.18:1994",
"102.165.51.172:3128",
"190.121.146.233:3129",
"45.63.119.70:80",
"217.138.226.139:9090",
"35.180.92.53:8001",
"130.61.186.129:8000",
"217.138.226.138:9090",
"88.99.171.92:8080",
"81.4.102.223:8081",
"170.78.210.17:999",
"195.201.16.74:8080",
"46.151.31.27:3128",
"167.235.62.101:8080",

]

