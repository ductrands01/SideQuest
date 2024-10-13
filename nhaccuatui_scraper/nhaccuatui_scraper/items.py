# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NhaccuatuiItem(scrapy.Item):
    category_name = scrapy.Field()
    category_url = scrapy.Field()
    song_url = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    duration = scrapy.Field()
    lyrics = scrapy.Field()

