import scrapy
import json
import datetime
import urllib
import re
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector

class SoldHouses(scrapy.Spider):

    name = 'rightmove'
    page_index = 0

    #Parameters
    params = {
        'country':'england',
        'searchLocation': '',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    }

    #Custom Download Setting
    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN":2,
        "DOWNLOAD_DELAY":1
    }

    def __init__(self):
        #Init PostCodes
        postcodes = ''

        with open('postcodes.json', 'r') as json_file:
            for line in json_file.read():
                postcodes += line

            self.postcodes = json.loads(postcodes)

    #Crawlet Entry Point
    def start_requests(self):

        filename = f'./output/Sold_Houses_.json'
        count = 0

        for item in self.postcodes:

            self.page_index = 0
            self.params['searchLocation'] = item['postcode']
            html_file = item['postcode'].lower()
            url = f'https://www.rightmove.co.uk/house-prices/{html_file}?{urllib.parse.urlencode(self.params)}'
            yield scrapy.Request(url=url, headers=self.headers, meta={'postcode':item['postcode'], 'filename':filename, 'count':count}, callback=self.parse_links)
            count += 1
            
            break
    
    def parse_links(self, response):

        #print(f'response: {response.status}')

        #Init FileName
        postcode = response.meta.get('postcode')
        filename = response.meta.get('filename')
        count = response.meta.get('count')

        '''
        #Debug Selectors
        content = ''
        with open('res1.html', 'r') as f:
            for line in f.read():
                content += line

        response = Selector(text=content)
        '''

        #Extract Basic Features
        properties = ''.join([script for script in response.css('script::text').getall() if 'window.__PRELOADED_STATE__ = {"results":' in script])
        properties = json.loads(properties.split('window.__PRELOADED_STATE__ =')[-1])
        properties = properties['results']['properties']
        
        for prop in properties:

            if prop['detailUrl']:
                prop_id = prop['detailUrl'].split('?prop=')[-1].split('&')[0]
                link = f'https://www.rightmove.co.uk/property-for-sale/property-{prop_id}.html'
                yield response.follow(url=link, headers=self.headers, meta={'property': prop,'filename':filename, 'postcode': postcode, 'count': count}, callback=self.parse_listing)
                break
        
        #print(json.dumps(basic_features , indent=2))
        #Crawl NextPage

    def parse_listing(self,response):

        
        features = {
            'id': ''.join(re.findall('\d+', response.url.split('/')[-1])),
            'url': response.url,
            'postcode':response.meta.get('postcode'),
            'title': response.css('div.left').css('h1.fs-22::text').get(),
            'address': response.css('div.cell').css('address').css('meta::attr(content)').get().split(' - ')[-1],
            'price': response.css('div.cell').css('p.property-header-price').get().replace('\t', '').replace('\n','').replace('\r', ''),
            'agent_link':response.css('div.agent-details-display').css('a::attr(href)').get(),
            'agent_name':response.css('div.agent-details-display').css('strong::text').get(),
            'agent_address':response.css('div.agent-details-display').css('address::text').get().replace('\n', ' '),
            'agent_phone':response.css('div.request-property-details').css('strong::text').get(),
            'image_urls':response.css('div.no-js-hidden').css('img::attr(src)').getall(),
            'floor_area':response.css('div.sect').css('ul.list-style-square').css('li::text').get(),
            'key_features':response.css('div.key-features').css('ul.list-style-square').css('li::text').getall(),
            'full_description':' '.join([feature.replace('\r', '').replace('\n','').strip() for feature in response.css('p[itemprop="description"]::text').getall() if feature != ''])
        }
        
        #Extract price Description
        price_descr = response.css('div.cell').css('p.property-header-price').css('small::text').get()

        #Add text value to price if available
        if price_descr is not None:
            features['price'] = price_descr
        
        #Handle missing coordinate
        try:

            #parse coordinates
            coord_link = urllib.parse.parse_qsl(response.css('div.right').css('a.block').css('img::attr(src)'))


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(SoldHouses)
    process.start()

    #SoldHouses.parse_listing(SoldHouses, '')