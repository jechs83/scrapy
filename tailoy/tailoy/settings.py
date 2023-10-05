# Scrapy settings for demo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from decouple import config 
BOT_NAME = "tailoy"

SPIDER_MODULES = ["tailoy.spiders"]
NEWSPIDER_MODULE = "tailoy.spiders"

ITEM_PIPELINES = {
    'tailoy.pipelines.MongoPipeline': 300,
}
#MONGO_URI = 'mongodb://superuser:Viper.2013@192.168.9.66:27017/?authMechanism=DEFAULT&tls=false'
MONGO_URI = config("MONGODB")
MONGO_DATABASE = config("DATABASE")
COLLECTION_NAME = config("COLLECTION")


#DOWNLOAD_DELAY = 1 # 2 seconds of delay
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "demo (+http://www.yourdomain.com)"

# Obey robots.txt rules
#ROBOTSTXT_OBEY = True
#USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

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



# DOWNLOADER_MIDDLEWARES = {
#     # ...
#     'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
#     'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
#     # ...
# }

'''
ROTATING_PROXY_LIST = [

"206.81.0.206:3128",
"204.137.250.6:3129",
"3.88.188.120:3128",
"138.197.153.166:8080",
"185.63.34.151:3128",
"139.144.187.220:3128",
"192.254.106.90:999",
"38.83.74.2:3128",
"64.225.4.85:9996",
"5.78.44.46:8080",
"143.42.138.51:8080",
"5.78.85.7:8080",
"47.254.31.179:80",
"168.119.174.184:8080",
"178.128.43.162:3128",
"35.177.2.69:8001",
"3.9.10.163:3128",
"18.130.164.122:8001",
"209.182.225.141:2019",
"192.254.106.89:999",
"194.102.180.147:3128",
"185.135.157.89:8080",
"194.102.180.144:3128",
"31.220.73.234:3128",
"31.186.239.246:8080",
"194.102.180.145:3128",
"104.223.135.178:10000",
"23.88.61.91:8080",
"194.102.180.148:3128",
"157.90.164.254:8080",
"91.107.194.30:8080",
"167.235.138.163:8080",
"142.93.108.171:3128",
"178.128.197.199:8080",
"91.107.235.93:8080",

]
'''

# ROTATING_PROXY_LIST = [
# "200.123.29.41:3128",
# "190.12.95.170:37209",
# "190.108.81.140:59311",
# "190.119.235.210:4153",
# "181.224.253.220:5678",
# "131.255.137.49:32650",
# "190.119.102.251:999",
# "181.65.169.35:999",
# "190.119.102.250:999",
# "190.239.24.76:5678",
# "170.81.240.237:999",
# "200.60.124.11:999",
# "200.123.27.162:999",
# "190.237.116.25:999",
# "190.239.220.231:999",
# "200.123.29.39:3128",
# "200.123.29.35:3128",
# "190.119.84.34:999",
# "161.132.125.244:8080",
# "190.119.102.252:999",
# "191.97.60.198:999",
# "181.65.128.140:999",
# "200.123.29.37:3128",
# "200.123.29.45:3128",
# "200.37.107.106:8888",
# "131.255.138.163:80",
# "170.81.240.232:999",
# "190.43.92.109:999",
# "181.176.211.168:8080",
# "200.37.140.35:10101",
# "200.123.29.38:3128",
# "200.60.119.131:9991",
# "170.81.242.232:999",
# "200.60.71.10:46934",
# "200.106.116.149:999"]



ROTATING_PROXY_LIST = [
"161.132.125.244:8080",
"170.81.240.232:999"]