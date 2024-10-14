# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class NhaccuatuiScraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class NhaccuatuiScraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


from urllib.parse import urlencode
from random import randint
import requests


class ScrapeOpsFakeUserAgentMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT',
                                               'http://headers.scrapeops.io/v1/user-agents')
        self.scrapeops_fake_user_agents_active = settings.get('SCRAPEOPS_FAKE_USER_AGENT_ENABLED', False)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')
        self.headers_list = []
        self._get_user_agents_list()
        self._scrapeops_fake_user_agents_enabled()

    def _get_user_agents_list(self):
        payload = {'api_key': self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.user_agents_list = json_response.get('result', [])

    def _get_random_user_agent(self):
        random_index = randint(0, len(self.user_agents_list) - 1)
        return self.user_agents_list[random_index]

    def _scrapeops_fake_user_agents_enabled(self):
        if self.scrapeops_api_key is None or self.scrapeops_api_key == '' or self.scrapeops_fake_user_agents_active == False:
            self.scrapeops_fake_user_agents_active = False
        else:
            self.scrapeops_fake_user_agents_active = True

    def process_request(self, request, spider):
        random_user_agent = self._get_random_user_agent()
        request.headers['User-Agent'] = random_user_agent

        print("************ NEW HEADER ATTACHED *******")
        print(request.headers['User-Agent'])


class ScrapeOpsFakeBrowserHeaderAgentMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT',
                                               'http://headers.scrapeops.io/v1/browser-headers')
        self.scrapeops_fake_browser_headers_active = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED', True)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')
        self.headers_list = []
        self._get_headers_list()
        self._scrapeops_fake_browser_headers_enabled()

    def _get_headers_list(self):
        payload = {'api_key': self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.headers_list = json_response.get('result', [])

    def _get_random_browser_header(self):
        random_index = randint(0, len(self.headers_list) - 1)
        return self.headers_list[random_index]

    def _scrapeops_fake_browser_headers_enabled(self):
        if self.scrapeops_api_key is None or self.scrapeops_api_key == '' or self.scrapeops_fake_browser_headers_active == False:
            self.scrapeops_fake_browser_headers_active = False
        else:
            self.scrapeops_fake_browser_headers_active = True

def process_request(self, request, spider):
    random_browser_header = self._get_random_browser_header()

    request.headers['accept-language'] = random_browser_header.get('accept-language', 'en-US,en;q=0.9')
    request.headers['sec-fetch-user'] = random_browser_header.get('sec-fetch-user', '?1')
    request.headers['sec-fetch-mod'] = random_browser_header.get('sec-fetch-mod', 'navigate')
    request.headers['sec-fetch-site'] = random_browser_header.get('sec-fetch-site', 'same-origin')
    request.headers['sec-ch-ua-platform'] = random_browser_header.get('sec-ch-ua-platform', '"Windows"')
    request.headers['sec-ch-ua-mobile'] = random_browser_header.get('sec-ch-ua-mobile', '?0')
    request.headers['sec-ch-ua'] = random_browser_header.get('sec-ch-ua', '"Chromium";v="99", "Google Chrome";v="99", "Not A;Brand";v="99"')
    request.headers['accept'] = random_browser_header.get('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    request.headers['user-agent'] = random_browser_header.get('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36')
    request.headers['upgrade-insecure-requests'] = random_browser_header.get('upgrade-insecure-requests', '1')

    print("************ NEW HEADER ATTACHED *******")
    print(request.headers)


import base64

class ScrapeOpsProxyMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.user = settings.get('PROXY_USER')
        self.password = settings.get('PROXY_PASSWORD')
        self.endpoint = settings.get('PROXY_ENDPOINT')
        self.port = settings.get('PROXY_PORT')

    def process_request(self, request, spider):
        """
        Adds ScrapeOps proxy authentication to the request.
        """
        user_credentials = f'{self.user}:{self.password}'
        basic_authentication = 'Basic ' + base64.b64encode(user_credentials.encode()).decode()
        proxy_url = f'http://{self.endpoint}:{self.port}'
        request.meta['proxy'] = proxy_url
        request.headers['Proxy-Authorization'] = basic_authentication


from scrapy import signals
from google.oauth2 import service_account
from googleapiclient.discovery import build, MediaFileUpload

class GoogleDriveUploadMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.credentials_path = settings.get('GOOGLE_API_CREDENTIALS_FILE')
        self.credentials = service_account.Credentials.from_service_account_file(self.credentials_path)
        self.output_file_path = settings.get('OUTPUT_FILE_PATH')
        self.upload_file_name = settings.get('UPLOAD_FILE_NAME')

    def spider_closed(self, spider):
        spider.logger.info("Uploading results to Google Drive...")

        # Google Drive service setup
        service = build('drive', 'v3', credentials=self.credentials)
        file_metadata = {'name': self.upload_file_name, 'mimeType': 'application/json' if self.output_file_path.endswith('.json') else 'text/csv'}
        media = MediaFileUpload(self.output_file_path, mimetype=file_metadata['mimeType'])

        try:
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            spider.logger.info(f"File uploaded to Google Drive with ID: {file.get('id')}")
        except Exception as e:
            spider.logger.error(f"Failed to upload file to Google Drive: {e}")