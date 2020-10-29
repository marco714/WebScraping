import scrapy
from ..items import QuotetutorialItem
class QuoteSpider(scrapy.Spider):

    name = 'quotes'
    page_num = 2
    start_urls = [
        'http://quotes.toscrape.com/login'
    ]

    def parse(self, response):

        items = QuotetutorialItem()
        all_div_quotes = response.css("div.quote")

        for quote in all_div_quotes:

            title = quote.css("span.text::text").extract()
            author = quote.css("small.author::text").extract()
            tag = quote.css(".tag::text").extract()

            items['title'] = title
            items['author'] = author
            items['tags'] = tag
            
            yield items
        
        next_page = f"http://quotes.toscrape.com/page/{QuoteSpider.page_num}/"
        print(next_page)

        if QuoteSpider.page_num < 11:
            QuoteSpider.page_num += 1
            yield response.follow(next_page, callback=self.parse)
        else:
            pass
