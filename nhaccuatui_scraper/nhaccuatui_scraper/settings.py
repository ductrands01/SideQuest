# Scrapy settings for nhaccuatui_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy.settings.default_settings import DOWNLOAD_TIMEOUT

BOT_NAME = "nhaccuatui_scraper"

SPIDER_MODULES = ["nhaccuatui_scraper.spiders"]
NEWSPIDER_MODULE = "nhaccuatui_scraper.spiders"

FEEDS = {
    'data/songs.csv': {
        'format': 'csv',
        'encoding': 'utf8',
        'store_empty': False,
        'fields': None,
        'overwrite': False,
        'item_export_kwargs': {
            'export_empty_fields': False,
        },
    }
}

# CATEGORY_URL = 'https://www.nhaccuatui.com/bai-hat/nhac-tre-moi.7.html'
NEXT_PAGE_LIMIT = 100000000000000000000000

import os
from dotenv import load_dotenv
load_dotenv()


# MYSQL_SERVER
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

# SCRAPEOPS
SCRAPEOPS_API_KEY = os.getenv('SCRAPEOPS_API_KEY')
SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = 'http://headers.scrapeops.io/v1/user-agents'
SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT = 'http://headers.scrapeops.io/v1/browser-headers'
SCRAPEOPS_PROXY_ENDPOINT = 'https://proxy.scrapeops.io/v1/?'
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = False
SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED = False
SCRAPEOPS_PROXY_ENABLED = False
SCRAPEOPS_NUM_RESULTS = 5

# CLOSESPIDER_ITEMCOUNT = 100


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "nhaccuatui_scraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 26
# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 0.55
DOWNLOAD_TIMEOUT = 30000



# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    # "nhaccuatui_scraper.middlewares.NhaccuatuiScraperSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # "nhaccuatui_scraper.middlewares.NhaccuatuiScraperDownloaderMiddleware": 543,
   #  "nhaccuatui_scraper.middlewares.ScrapeOpsFakeUserAgentMiddleware": 100,
   #  "nhaccuatui_scraper.middlewares.ScrapeOpsFakeBrowserHeaderMiddleware": 200,
   #  "nhaccuatui_scraper.middlewares.ScrapeOpsProxyMiddleware":300,
   #  'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
   #  'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
   #  'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    'scrapy_deltafetch.DeltaFetch': 100,
    # 'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500,
    # "scrapy.extensions.telnet.TelnetConsole": None,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "nhaccuatui_scraper.pipelines.NhaccuatuiScraperPipeline": 300,
    'nhaccuatui_scraper.pipelines.MySQLPipeline': 400
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 3
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 30
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 3000
HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
