import scrapy
from scrapy.loader import ItemLoader
from tutorial.items import TutorialItem

class QuoteSpider(scrapy.Spider):

    name = "quotes"

    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        self.logger.info('Hello this is my first project')
        quotes = response.css('div.quote')
        for quote in quotes:

            loader = ItemLoader(item=TutorialItem(), selector=quote)
            loader.add_css('quote_content', '.text::text')
            loader.add_css('tags', '.tag::text')
            quote_item = loader.load_item()
            author_url = quote.css('small.author + a::attr(href)').get()
            yield response.follow(author_url, callback=self.parse_author, meta={'quote-item':quote_item})
        
        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)
    
    def parse_author(self, response):

        quote_item = response.meta['quote-item']
        loader = ItemLoader(item=quote_item, response=response)
        
        loader.add_css('author_name', '.author-title::text')
        loader.add_css('author_birthday', '.author-born-date::text')
        loader.add_css('author_bornlocation', 'author-born-location::text')
        loader.add_css('author_bio', 'author-description::text')
        yield loader.load_item()