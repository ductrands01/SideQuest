# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SongsscraperItem(scrapy.Item):
    category_name = scrapy.Field()
    category_url = scrapy.Field()
    title = scrapy.Field()
    song_url = scrapy.Field()
    author = scrapy.Field()
    duration = scrapy.Field()
    lyrics = scrapy.Field()
    tags = scrapy.Field()
    poster = scrapy.Field()
    image = scrapy.Field()
    audio_url = scrapy.Field()

