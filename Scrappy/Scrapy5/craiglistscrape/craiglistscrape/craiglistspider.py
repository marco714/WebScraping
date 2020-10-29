import scrapy
import os
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
from items import CraiglistscrapeItem

class RealestateSpider(scrapy.Spider):
    num = 1
    name = 'realestate_loader'
    start_urls= [
        'https://newyork.craigslist.org/d/real-estate/search/rea'
    ]

    try:
        os.remove('result.json')
    except OSError:
        pass

    def __init__(self):
        self.lat = ""
        self.lon = ""
    
    def start_requests(self):
        yield scrapy.Request('https://newyork.craigslist.org/d/real-estate/search/rea', callback=self.parse)
    
    def parse(self, response):
        
        all_ads = response.xpath("//p[@class='result-info']")

        for ads in all_ads:
            
            #Get the details Link
            details_link = ads.xpath(".//a[@class='result-title hdrlnk']/@href").get()
            
            #Get The Geo Data
            yield response.follow(url=details_link, callback=self.parse_detail)

            #Loader
            loader = ItemLoader(item=CraiglistscrapeItem(),selector=ads,response=response)

            loader.add_xpath("price", ".//span[@class='result-price']/text()")
            loader.add_xpath("date", ".//time[@class='result-date']/text()")
            loader.add_xpath("title", ".//a[@class='result-title hdrlnk']/text()")
            loader.add_xpath("hood", ".//span[@class='result-hood']/text()")
            loader.add_xpath("link", ".//a[@class='result-title hdrlnk']/@href")
            loader.add_value("lon", self.lon)
            loader.add_value("lat", self.lat)

            yield loader.load_item()

        
        if RealestateSpider.num <=20:

            #Nav next page    
            next_page = response.xpath("//a[@class='button next']/@href").get()
            RealestateSpider.num +=1
            if next_page:
                yield response.follow(url=next_page, callback=self.parse)

    def parse_detail(self, response):
        #Set Variable to response from lon and latest
        self.lon = response.xpath("//meta[@name='geo.position']/@content").get().split(";")[0]
        self.lat = response.xpath("//meta[@name='geo.position']/@content").get().split(";")[1]


if __name__ == "__main__":
    cl = CrawlerProcess(settings={
        "FEEDS":{
            "result.json":{"format":"json"},
        }
    })

    cl.crawl(RealestateSpider)
    cl.start()