# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CraiglistscrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    date = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    hood = scrapy.Field()
    link = scrapy.Field()
    misc = scrapy.Field()
    lon = scrapy.Field()
    lat = scrapy.Field()
    
