import scrapy


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['http://books.toscrape.com/']
    start_urls = ['http://books.toscrape.com//']

    def parse(self, response):
        
        all_the_books = response.xpath("//article")
        
        for book in all_the_books:
            title = book.xpath(".//h3/a/@title").get()
            price = book.xpath(".//div[@class='product_price']/p[@class='price_color']/text()").get()
            src = book.xpath(".//a/img/@src").get()
            img_src = response.urljoin(src)
            url = book.xpath(".//div[@class='image_container']/a/@href").get()
            book_url = response.urljoin(url)

            yield {
                'Title':title,
                'Price':price,
                'Image_Src': img_src,
                'Book_Url': book_url
            }