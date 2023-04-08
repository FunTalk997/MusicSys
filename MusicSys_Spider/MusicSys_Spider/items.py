# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MusicSysSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    songName = scrapy.Field()
    singer = scrapy.Field()
    album = scrapy.Field()
    songTime = scrapy.Field()
    lyric = scrapy.Field()
    lyricist = scrapy.Field()
    picUrl = scrapy.Field()
    musicUrl = scrapy.Field()
    table_name = scrapy.Field()
    table_fields = scrapy.Field()
