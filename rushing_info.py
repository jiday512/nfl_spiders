import scrapy
from scrapy.http import Request
import re


class QbsSpider(scrapy.Spider):
    name = 'rushing_info'
    allowed_domains = ['www.nfl.com']
    start_urls = ['https://nfl.com/stats/player-stats/category/rushing/{}/REG/all/rushingyards/desc'.format([str(x) for x in range(1970,2020)][i]) for i in range(len([str(x) for x in range(1970,2020)]))]

    def parse(self, response):
        players = response.xpath('//td/div/div/a/@href').extract()
        for player in players:
            qbs = 'https://www.nfl.com' + player
            yield Request(qbs, callback = self.player_data)
            
        try:
            next_page = response.xpath('//a[@title="Next Page"]/@href').extract_first()
            next_page_url = 'https://www.nfl.com' + next_page
            absolute_url = Request(url=next_page_url)
            yield absolute_url
        except:
            pass
       
    
    def player_data(self, response):
        name = response.xpath('//h1/text()').extract()
        team = response.xpath('//*[@class="nfl-c-player-header__team nfl-u-hide-empty"]/text()').extract()
        college = response.xpath('//li[contains(.,"college")]/div[2]/text()').extract()
        height = response.xpath('//li[contains(.,"height")]/div[2]/text()').extract()
        weight = response.xpath('//li[contains(.,"weight")]/div[2]/text()').extract()
        arms =  response.xpath('//li[contains(.,"arms")]/div[2]/text()').extract()
        hands = response.xpath('//li[contains(.,"hands")]/div[2]/text()').extract()
        age = response.xpath('//li[contains(.,"age")]/div[2]/text()').extract()
        position = response.xpath('//*[@class="nfl-c-player-header__position"]/text()').re('\w+')
        
        yield  {
            'name':name,
            'position':position,
            'team':team,
            'college':college,
            'height': height,
            'weight': weight,
            'arms': arms,
            'hands': hands,
            'age': age
        }
        