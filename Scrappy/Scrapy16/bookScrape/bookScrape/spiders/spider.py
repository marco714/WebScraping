from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class SpiderSpider(CrawlSpider):
    name = 'spider'
    start_urls = ['http://books.toscrape.com/']
    base_url = 'http://books.toscrape.com/'

    rules = [Rule(LinkExtractor(allow='catalogue/'), callback='parse_filter_book', follow=True)]

    def parse_filter_book(self,response):

        exists = response.xpath("//div[@id='product_gallery']").get()

        if exists:
            title = response.xpath('//div/h1/text()').get()
            relative_image = response.xpath("//div[@class='item active']/img/@src").get()
            final_image = f"{self.base_url}{relative_image.replace('../..', '')}"
            price = response.xpath("//p[@class='price_color']/text()").getall()[0]
            stocks = response.xpath("//p[@class='instock availability']/text()").getall()[1].replace('\n','').strip()

            #p[contains(@class, "star-rating")]
            rating = response.xpath("//div[@class='col-sm-6 product_main']/p[3]/@class").get()
            description = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
            UPC = response.xpath("//table[@class='table table-striped']/tr[1]/td/text()").get()
            exclusive_tax = response.xpath("//table[@class='table table-striped']/tr[3]/td/text()").get()
            inclusive_tax = response.xpath("//table[@class='table table-striped']/tr[4]/td/text()").get()
            
            yield {
                'Title': title,
                'Image_URL': final_image,
                'Price':price,
                'Stocks': stocks,
                'Rating': rating,
                'Description': description,
                'UPC': UPC,
                'Exclusive Tax': exclusive_tax,
                'Inclusive Tax': inclusive_tax
            }

        else:
            print(response.url)
            
'''
def parse(self, response):
        all_the_books = response.xpath("//article[@class='product_pod']")

        for book in all_the_books:
            book_url = book.xpath(".//h3/a/@href").get()

            if 'catalogue/' not in book_url:
                book_url = 'catalogue/' + book_url

            book_url = self.base_url + book_url

            yield scrapy.Request(url=book_url, callback=self.parse_book)


        next_page = response.xpath("//li[@class='next']/a/@href").get()

        if 'catalogue/' not in next_page:
            next_page = 'catalogue/' + next_page

        next_page_url = self.base_url + next_page
        yield scrapy.Request(url=next_page_url, callback=self.parse)

'''