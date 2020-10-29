import scrapy


class WikiscrapeSpider(scrapy.Spider):
    name = 'wikiScrape'
    start_urls = ['https://en.wikipedia.org/wiki/Eiffel_Tower']

    def parse(self, response):
        raw_image_urls = response.css('.image img ::attr(src)').getall()
        clean_image_urls = []

        clean_image_urls = [response.urljoin(img_url) for img_url in raw_image_urls]

        yield {
            'image_urls': clean_image_urls
        }
