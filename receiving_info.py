import scrapy
from scrapy.http import Request
import re


class QbsSpider(scrapy.Spider):
    name = 'receiving_info'
    allowed_domains = ['www.nfl.com']
    start_urls = ['https://www.nfl.com/stats/player-stats/category/receiving/{}/REG/all/receivingreceptions/desc/'.format([str(x) for x in range(1970,2021)][i]) for i in range(len([str(x) for x in range(1970,2021)]))]

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
        Name = response.xpath('//h1/text()').extract()
        Team = response.xpath('//*[@class="nfl-o-cta--link"]/text()').extract()
        College = response.xpath('//li[contains(.,"College")]/div[2]/text()').extract()
        Height = response.xpath('//li[contains(.,"Height")]/div[2]/text()').extract()
        Weight = response.xpath('//li[contains(.,"Weight")]/div[2]/text()').extract()
        Arms =  response.xpath('//li[contains(.,"Arms")]/div[2]/text()').extract()
        Hands = response.xpath('//li[contains(.,"Hands")]/div[2]/text()').extract()
        Age = response.xpath('//li[contains(.,"Age")]/div[2]/text()').extract()
        Position = response.xpath('//*[@class="nfl-c-player-header__position"]/text()').re('\w+')

        yield  {
            'Name':Name,
            'Position':Position,
            'Team':Team,
            'College':College,
            'Height': Height,
            'Weight': Weight,
            'Arms': Arms,
            'Hands': Hands,
            'Age': Age
        }
