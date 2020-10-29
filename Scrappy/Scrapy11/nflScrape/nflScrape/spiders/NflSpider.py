import scrapy


class NflspiderSpider(scrapy.Spider):
    name = 'NflSpider'
    start_urls = ['https://www.nfl.com/players/active/a']

    def parse(self, response):
        player = response.css('.nfl-o-cta--link::attr(href)').get()
        link = response.urljoin(player)
        yield scrapy.Request(url=link, callback=self.parse_profile)

        '''
        all_players = response.css('.nfl-o-cta--link::attr(href)').getall()

        for player in all_players:
            #Using Urljoin it will get the relative link

            link = response.urljoin(player)
            yield scrapy.Request(url=link, callback=self.parse_profile)
        '''

    def parse_profile(self, response):
        link = response.css('.active+ li a::attr(href)').get()
        stats_link = response.urljoin(link)
        yield scrapy.Request(url=stats_link, callback=self.parse_log)
    
    def parse_log(self, response):
        link = response.css('li:nth-child(3) .nfl-o-cta--secondary::attr(href)').get()
        log_link = response.urljoin(link)
        yield scrapy.Request(url=log_link, callback=self.parse_player_profile)
    
    def parse_player_profile(self, response):
        player_name = response.css('.nfl-c-player-header__title::text').get()
        player_team = response.css('.nfl-c-player-header__team::text').get()
        table = response.xpath("//div[@class='nfl-o-roster']/div[2]/table")

        for header in response.xpath("//div[@class='nfl-o-roster']/div[1]/h3/text()").getall():
            season = header.replace('\n', '').strip()
            print(season)

        for t in table:
            for week in t.css('tbody > tr'):
                wk = week.css('td:nth-child(1)::text').get().replace('\n', '').strip()
                date_played = week.css('td:nth-child(2)::text').get().replace('\n', '').strip()
                opponent = week.css('td:nth-child(3)::text').get().replace('\n', '').strip()
                result = week.css('td:nth-child(4)::text').get().replace('\n', '').strip()
        
                item = {
                    'Player_name': player_name,
                    'Player_team': player_team,
                    'Week': wk,
                    'Date_played': date_played,
                    'Opponent': opponent,
                    'Result': result
                }

                yield item
