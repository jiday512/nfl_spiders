import scrapy
from scrapy.http import Request
import re


class QbsSpider(scrapy.Spider):
    name = 'rushing_stats'
    allowed_domains = ['www.nfl.com']
    start_urls = ['https://nfl.com/stats/player-stats/category/rushing/{}/REG/all/rushingyards/desc'.format([str(x) for x in range(1970,2021)][i]) for i in range(len([str(x) for x in range(1970,2021)]))]

    def parse(self, response):
        
        try:
            next_page = response.xpath('//a[@title="Next Page"]/@href').extract_first()
            next_page_url = 'https://www.nfl.com' + next_page
            absolute_url = Request(url=next_page_url)
            yield absolute_url
            
        except:
            pass
       
        table = response.xpath('//table')
        trs = table.xpath('.//tr')[1:]
        for tr in trs:
            Name = tr.xpath('.//*[@class="d3-o-player-fullname nfl-o-cta--link"]/text()').re(r'\w+\s\w+')
            Year = response.xpath('//option[@selected="selected"]/text()').re(r'\d+')
            RushingYards = tr.xpath('.//td[2]/text()').re(r'\d+')
            Att = tr.xpath('.//td[3]/text()').re(r'\d+')
            TD = tr.xpath('.//td[4]/text()').re(r'\d+')
            TwentyPlus = tr.xpath('.//td[5]/text()').re(r'\d+')
            FourtyPlus = tr.xpath('.//td[6]/text()').re(r'\d+')
            Lng = tr.xpath('.//td[7]/text()').re(r'\d+')
            RushingFirst = tr.xpath('.//td[8]/text()').re(r'\d+')
            RushingFirstPerc = tr.xpath('.//td[9]/text()').re(r'\d+.\d+')
            RushingFum = tr.xpath('.//td[10]/text()').re(r'\d+')
        
            yield {
            'Name' : Name,
            'Year' : Year,
            'RushingYards' : RushingYards, 
            'Att' : Att,
            'TD' : TD, 
            'TwentyPlus' : TwentyPlus,
            'FourtyPlus' : FourtyPlus,
            'Lng' : Lng,
            'RushingFirst' : RushingFirst,
            'RushingFirstPerc' : RushingFirstPerc,
            'RushingFum' : RushingFum,
            }
            
    
    