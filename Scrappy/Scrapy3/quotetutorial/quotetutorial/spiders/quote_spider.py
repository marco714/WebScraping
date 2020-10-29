import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from ..items import QuotetutorialItem

class QuoteSpider(scrapy.Spider):

    name = 'quotes'
    page_num = 2
    start_urls = [
        'http://quotes.toscrape.com/login'
    ]

    def parse(self, response):

        token = response.css("form input::attr(value)").extract_first()
        return FormRequest.from_response(response, formdata={
            'csrf_tokem':token,
            'username':'marconarca@gmail.com',
            'password':'helloworld'
        }, callback=self.start_scraping)
    
    def start_scraping(self, response):
        open_in_browser(response)
        
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
            yield response.follow(next_page, callback=self.start_scraping)
        else:
            pass