import pandas as pd
import scrapy
from ..items import NhaccuatuiSong
from scrapy.utils.project import get_project_settings

class NhaccuatuiSongsSpider(scrapy.Spider):
    name = 'nhaccuatui_songs'

    def __init__(self, *args, **kwargs):
        super(NhaccuatuiSongsSpider, self).__init__(*args, **kwargs)
        settings = get_project_settings()
        self.limit = settings.get('NEXT_PAGE_LIMIT', 3)

    def start_requests(self):
        try:
            df = pd.read_csv('categories.csv')
        except FileNotFoundError:
            self.logger.error("File 'categories.csv' not found.")
            return
        except Exception as e:
            self.logger.error(f"Error reading 'categories.csv': {str(e)}")
            return

        for _, row in df.iterrows():
            if 'url' in row and 'name' in row:
                yield scrapy.Request(
                    url=row['url'],
                    callback=self.parse_category,
                    meta={'page_count': 1, 'category_name': row['name']},
                )
            else:
                self.logger.warning(f"Skipping category due to missing 'url' or 'name': {row}")

    def parse_category(self, response):
        song_urls = response.xpath('//div[@class="info_song"]/a[@class="name_song"]/@href').getall()
        for song_url in song_urls:
            yield scrapy.Request(
                url=response.urljoin(song_url),
                callback=self.parse_song,
                meta={'category_name': response.meta['category_name']}
            )

        page_count = response.meta['page_count']
        if page_count < self.limit:
            next_page = response.xpath('//a[@rel="next"]/@href').get()
            if next_page:
                yield scrapy.Request(
                    url=response.urljoin(next_page),
                    callback=self.parse_category,
                    meta={'page_count': page_count + 1, 'category_name': response.meta['category_name']}
                )

    def parse_song(self, response):
        song_item = NhaccuatuiSong(
            url=response.url,
            name=response.css('div.name_title h1[itemprop="name"]::text').get(),
            authors=response.xpath('//*[@id="box_playing_id"]/div/div/h2/a/text()').getall(),
            lyrics=response.xpath('//*[@id="divLyric"]/text() | //*[contains(@id, "divLyric")]/br').getall(),
            poster=response.xpath('//p[@class="name_post"]/a/text()').get(),
            poster_url=response.xpath('//p[@class="name_post"]/a/@href').get()
        )
        yield song_item

    def handle_error(self, failure):
        self.logger.error(f"Request failed: {failure.request.url}, Error: {repr(failure)}")
