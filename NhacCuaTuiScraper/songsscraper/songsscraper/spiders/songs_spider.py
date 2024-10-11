import scrapy
from scrapy_splash import SplashRequest
from ...songsscraper.items import SongsscraperItem


class NhacCuaTuiSpider(scrapy.Spider):
    name = 'nhaccuatui'
    allowed_domains = ['nhaccuatui.com']
    start_urls = ['https://www.nhaccuatui.com/bai-hat/bai-hat-moi.html']

    # Lua script for Splash to render the dynamic page
    script = """
    function main(splash, args)
        splash.private_mode_enabled = false
        splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36")
        splash:go(args.url)
        splash:wait(3)
        return {html = splash:html()}
    end
    """

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse_categories, endpoint='execute', args={'lua_source': self.script})

    def parse_categories(self, response):
        # Extract main categories
        categories = response.xpath('//ul[@class="detail_menu_browsing_dashboard"]/li/a')
        for category in categories:
            category_name = category.xpath('text()').get()
            category_url = response.urljoin(category.xpath('@href').get())

            # Follow each category URL to scrape song details
            yield SplashRequest(category_url, self.parse_songs, endpoint='execute', args={'lua_source': self.script},
                                meta={'category_name': category_name, 'category_url': category_url})

    def parse_songs(self, response):
        category_name = response.meta['category_name']
        category_url = response.meta['category_url']

        # Extract songs on the category page
        songs = response.xpath('//div[@class="box-content-music-list"]//div[@class="info_song"]')
        for song in songs:
            item = SongsscraperItem()
            item['category_name'] = category_name
            item['category_url'] = category_url
            item['song_name'] = song.xpath('.//a[@class="name_song"]/@title').get()
            item['song_url'] = response.urljoin(song.xpath('.//a[@class="name_song"]/@href').get())
            item['author'] = song.xpath('.//div[@class="name_sing_under"]/a/text()').get()

            # Follow the song detail page to extract more information
            detail_url = item['song_url']
            yield SplashRequest(detail_url, self.parse_song_detail, endpoint='execute',
                                args={'lua_source': self.script}, meta={'item': item})

    def parse_song_detail(self, response):
        item = response.meta['item']

        # Extract additional information from the song detail page
        item['lyrics'] = response.xpath('//div[@class="lyrics"]/text()').get()
        item['tags'] = response.xpath('//div[@class="tags"]/a/text()').getall()
        item['poster'] = response.xpath('//div[@class="poster"]//img/@src').get()
        item['audio_url'] = response.xpath('//audio[@class="audio_source"]/@src').get()
        item['image'] = response.xpath('//div[@class="thumbnail"]//img/@src').get()

        yield item
