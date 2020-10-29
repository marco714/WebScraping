import scrapy
import time

class OscarsspiderSpider(scrapy.Spider):
    name = 'oscars'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture']

    def parse(self, response):

        for href in response.css("tr[style='background:#FAEB86'] a[href*=film]::attr(href)").extract():
            url = response.urljoin(href)
            print(url)
            req = scrapy.Request(url, callback=self.parse_titles)
            time.sleep(4)
            yield req

    def parse_titles(self, response):

        for sel in response.css('html').extract():
            data = {}
            data['title'] = response.css("h1[id='firstHeading'] i::text").extract()
            data['director'] = response.css("tr:contains('Directed by') a[href*='/wiki/']::text").extract()
            data['starring'] = response.css("tr:contains('Starring') a[href*='/wiki/']::text").extract()
            data['releasedate'] = response.css("tr:contains('Release date') li::text").extract()
            data['runtime'] = response.css("tr:contains('Running time') td::text").extract()
        
        yield data
