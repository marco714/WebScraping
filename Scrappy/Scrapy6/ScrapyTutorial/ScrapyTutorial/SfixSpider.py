import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from items import ScrapytutorialItem

class SfixspiderSpider(scrapy.Spider):
    name = 'SfixSpider'
    allowed_domains = ['screwfix.com']
    custom_settings = {
        'FEED_FORMAT':'json',
        'FEED_URI':'drills.json'
    }

    def start_requests(self):
        url = 'https://www.screwfix.com/c/tools/drills/cat830704#category=cat830704'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        
        for sf_product in response.selector.xpath("//*[@class='lg-12 md-24 sm-24 cols']"):
            loader = ItemLoader(item=ScrapytutorialItem(), selector=sf_product, response=response)
            loader.add_xpath('link', "//h3[@class='lii__title']/a/@href")
            loader.add_xpath('price', "//div[@class='lii_price']/h4/text()")
            loader.add_xpath('description', "//*[@class='lii__title']/a/text()")
            yield loader.load_item()
            
        next_page = response.selector.xpath("//a[@id='next_page_link']/@href").get()

        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse)

process = CrawlerProcess()
process.crawl(SfixspiderSpider)
process.start()