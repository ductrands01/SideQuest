import scrapy
from ..items import NhaccuatuiItem

class NhaccuatuiSpider(scrapy.Spider):
    name = 'nhaccuatui'
    start_urls = ['https://www.nhaccuatui.com/bai-hat/bai-hat-moi.html']

    def parse(self, response):
        category_urls = response.xpath('//ul[@class="detail_menu_browsing_dashboard"]/li/a/@href').getall()
        for category_url in category_urls:
            yield scrapy.Request(category_url, callback=self.parse_category, errback=self.handle_error)

    def parse_category(self, response):
        song_urls = response.xpath('//div[@class="box-content-music-list"]//div[@class="info_song"]//a[@class="name_song"]/@href').getall()
        for song_url in song_urls:
            yield scrapy.Request(song_url, callback=self.parse_song, meta={
                'category_name': response.xpath('//title/text()').get(),
                'category_url': response.url
            }, errback=self.handle_error)

        next_page = response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse_category, errback=self.handle_error)

    def parse_song(self, response):
        songitem = NhaccuatuiItem()
        songitem['category_name'] = response.meta['category_name']
        songitem['category_url'] = response.meta['category_url']
        songitem['song_url'] = response.url
        songitem['title'] = response.css('div.name_title h1[itemprop="name"]::text').get()
        songitem['authors'] = response.xpath('//*[@id="box_playing_id"]/div/div/h2/a/text()').getall()
        songitem['lyrics'] = response.xpath('//*[@id="divLyric"]/text() | //*[contains(@id, "divLyric")]/br').getall()
        songitem['poster'] = response.xpath('//p[@class="name_post"]/a/text()').get()
        songitem['poster_url'] = response.xpath('//p[@class="name_post"]/a/@href').get()
        yield songitem

    def handle_error(self, failure):
        self.logger.error(repr(failure))
