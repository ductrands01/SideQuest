import scrapy
from ..items import NhaccuatuiCategory


class NhaccuatuiCategoriesSpider(scrapy.Spider):
    name = 'nhaccuatui_categories'
    start_urls = [
        'https://www.nhaccuatui.com/bai-hat/bai-hat-moi.html',
    ]

    def parse(self, response):
        categories = response.xpath('//ul[@class="detail_menu_browsing_dashboard"]/li/a')
        for category in categories:
            category_url = category.xpath('@href').get()
            category_name = category.xpath('text()').get()
            if category_url and category_name:
                yield NhaccuatuiCategory(
                    url=response.urljoin(category_url),
                    name=category_name.strip()
                )

FEEDS = {
    'data/categories.csv': {
        'format': 'csv',
        'overwrite': False
    },
}