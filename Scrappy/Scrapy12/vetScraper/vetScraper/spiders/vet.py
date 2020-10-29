import scrapy


class VetSpider(scrapy.Spider):
    name = 'vet'
    start_urls = ['http://www.findalocalvet.com/Find-a-Veterinarian.aspx']

    def parse(self, response):

        for link in response.css('#SideByCity .itemresult a::attr(href)').getall():
            link = response.urljoin(link)
            yield scrapy.Request(url=link, callback=self.parse_city)

    def parse_city(self, response):

        for link in response.css('.org::attr(href)').getall():
            link = response.urljoin(link)
            yield scrapy.Request(url=link, callback=self.parse_clinic)

        next_link = response.css('a.dataheader:contains("Next")::attr(href)').get()
        if next_link:
            next_link = response.urljoin(next_link)
            yield scrapy.Request(url=next_link, callback=self.parse_city)

    def parse_clinic(self, response):
        yield {
            'Name': response.css('.Results-Header h1::text').get(),
            'City': response.css('.locality::text').get(),
            'State': response.css('.region::text').get(),
            'StreetAddress': response.css('.street-address::text').get(),
            'Link': response.url,
        }