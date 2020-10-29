import scrapy
from ..items import AmazontutorialItem

class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon'
    page_number = 2
    start_urls = [
        'https://www.amazon.com/s?k=the+threat+how+the+fbi+protects+america+in+the+age&crid=335KJ5XZYB5WX&sprefix=The+threat+how+the%2Caps%2C351&ref=nb_sb_ss_i_2_18'
    ]

    def parse(self, response):
        items = AmazontutorialItem()

        product_name = response.css('.a-color-base.a-text-normal').css('::text').extract()
        product_author = response.css('.sg-col-12-of-28 .a-size-base+ .a-size-base').css('::text').extract()
        product_price = response.css('.sg-col-24-of-28:nth-child(9) .a-price-whole , .sg-col-24-of-28:nth-child(9) .a-price-fraction , .sg-col-24-of-28:nth-child(8) .a-price-whole , .a-spacing-top-small .a-price-fraction , .a-spacing-top-small .a-price-whole').css('::text').extract()
        product_imagelink = response.css('.s-image::attr(src)').extract()

        items['product_name'] = product_name
        items['product_author'] = product_author
        items['product_price'] = product_price
        items['product_imagelink'] = product_imagelink

        yield items

        next_page = f'https://www.amazon.com/s?k=the+threat+how+the+fbi+protects+america+in+the+age&page={AmazonSpiderSpider.page_number}'

        if AmazonSpiderSpider.page_number <=15:
            AmazonSpiderSpider.page_number +=1
            yield response.follow(next_page, callback=self.parse)






