# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NhaccuatuiSong(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    authors = scrapy.Field()
    lyrics = scrapy.Field()
    poster = scrapy.Field()
    poster_url = scrapy.Field()

class NhaccuatuiCategory(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
