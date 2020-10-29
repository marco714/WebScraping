# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst
from datetime import datetime

def remove_quotes(text):

    text = text.strip(u'\u201c'u'\201d')
    return text

def convert_date(text):

    return datetime.strptime(text, "%B %d, %Y")

def parse_location(text):

    return text[3:]

class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    quote_content = Field(
        input_processor = MapCompose(remove_quotes),
        output_processor = TakeFirst()
    )

    author_name = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    
    tags = Field()
    author_birthday =Field(
        input_processor = MapCompose(convert_date),
        output_processor = TakeFirst()
    )
    author_bornlocation = Field(
        input_processor = MapCompose(parse_location),
        output_processor = TakeFirst()
    )
    author_bio = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )