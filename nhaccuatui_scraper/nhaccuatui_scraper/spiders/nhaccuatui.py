import scrapy
from ..items import NhaccuatuiItem

class NhaccuatuiSpider(scrapy.Spider):
    name = 'nhaccuatui'
    start_urls = ['https://www.nhaccuatui.com/bai-hat/bai-hat-moi.html']

    def parse(self, response):
        category_urls = response.xpath('//ul[@class="detail_menu_browsing_dashboard"]/li/a/@href').getall()
        for category_url in category_urls:
            yield scrapy.Request(response.urljoin(category_url), callback=self.parse_category)

    def parse_category(self, response):
        song_urls = response.xpath('//div[@class="box-content-music-list"]//div[@class="info_song"]//a[@class="name_song"]/@href').getall()
        for song_url in song_urls:
            yield scrapy.Request(response.urljoin(song_url), callback=self.parse_song, meta={'category_name': response.xpath('//title/text()').get(), 'category_url': response.url})

        next_page = response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse_category)

    def parse_song(self, response):
        item = NhaccuatuiItem()
        item['category_name'] = response.meta['category_name']
        item['category_url'] = response.meta['category_url']
        item['song_url'] = response.url
        item['title'] = response.css('div.name_title h1[itemprop="name"]::text').get()
        item['authors'] = response.css('div.name_title h2.name-singer a::text').getall()
        item['duration'] = response.xpath('//*[@id="utTotalTimeflashPlayer"]/text()').get()
        item['lyrics'] = response.xpath('//*[@id="divLyric"]/text()').get()

        yield item
