# Scrapy settings for nhaccuatui_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "nhaccuatui_scraper"

SPIDER_MODULES = ["nhaccuatui_scraper.spiders"]
NEWSPIDER_MODULE = "nhaccuatui_scraper.spiders"


# File output settings
OUTPUT_FILE_FORMAT = "csv"
OUTPUT_FILE_PATH = f'data/songs.{OUTPUT_FILE_FORMAT}'  # Local output file path based on format

# Scrapy feed export settings
FEED_FORMAT = OUTPUT_FILE_FORMAT
FEED_URI = OUTPUT_FILE_PATH

import os
from dotenv import load_dotenv
load_dotenv()

# CLOSESPIDER_ITEMCOUNT = 5

# MYSQL_SERVER
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')


# SCRAPEOPS
SCRAPEOPS_API_KEY = os.getenv('SCRAPEOPS_API_KEY')
SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = 'http://headers.scrapeops.io/v1/user-agents'
SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT = 'http://headers.scrapeops.io/v1/browser-headers'
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = False
SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED = False
SCRAPEOPS_NUM_RESULTS = 5

PROXY_USER = os.getenv('PROXY_USER')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD')
PROXY_ENDPOINT = os.getenv('PROXY_ENDPOINT', 'proxy.scrapeops.io')
PROXY_PORT = os.getenv('PROXY_PORT', '8000')


# GOOGLE_DRIVE
# GOOGLE_API_CREDENTIALS_FILE = os.getenv('GOOGLE_API_CREDENTIALS_FILE')

# LOG_LEVEL = 'INFO'
# LOG_FILE = './logs/system.log'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "nhaccuatui_scraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 30

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5
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
#     "nhaccuatui_scraper.middlewares.GoogleDriveUploadMiddleware": 600,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # "nhaccuatui_scraper.middlewares.NhaccuatuiScraperDownloaderMiddleware": 543,
    "nhaccuatui_scraper.middlewares.ScrapeOpsFakeUserAgentMiddleware": 100,
    "nhaccuatui_scraper.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware": 200,
    "nhaccuatui_scraper.middlewares.ScrapeOpsProxyMiddleware":300

}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    'scrapy_deltafetch.DeltaFetch': 100,
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
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3000
HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
