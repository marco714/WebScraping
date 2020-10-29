import scrapy

base = 'http://quotes.toscrape.com/api/quotes?page='
class ScrollSpider(scrapy.Spider):
    name = 'scroll'
    start_urls = [f"{base}{1}"]

    def parse(self, response):
        
        data = response.json()
        for quote in data["quotes"]:
            yield {
                'Author': quote["author"]["name"],
                'Quote': quote["text"]
            }
        
        current_page = data["page"]
        if data["has_next"]:
            next_page_url = f"{base}{current_page+1}"
            yield scrapy.Request(url=next_page_url)