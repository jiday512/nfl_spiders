import scrapy
from scrapy.http import Request
import re


class QbsSpider(scrapy.Spider):
    name = 'passing_stats'
    allowed_domains = ['www.nfl.com']
    start_urls = ['https://nfl.com/stats/player-stats/category/passing/{}/REG/all/passingyards/desc'.format([str(x) for x in range(1970,2021)][i]) for i in range(len([str(x) for x in range(1970,2021)]))]

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
            PassYards = tr.xpath('.//td[2]/text()').re(r'\d+')
            YdsPerAtt = tr.xpath('.//td[3]/text()').re(r'\d+.\d+')
            Att = tr.xpath('.//td[4]/text()').re(r'\d+')
            Cmp = tr.xpath('.//td[5]/text()').re(r'\d+')
            CompPerc = tr.xpath('.//td[6]/text()').re(r'\d+.\d+')
            TD = tr.xpath('.//td[7]/text()').re(r'\d+')
            int = tr.xpath('.//td[8]/text()').re(r'\d+')
            Rate = tr.xpath('.//td[9]/text()').re(r'\d+.\d+')
            First = tr.xpath('.//td[10]/text()').re(r'\d+')
            FirstPerc = tr.xpath('.//td[11]/text()').re(r'\d+.\d+')
            TwentyPlus = tr.xpath('.//td[12]/text()').re(r'\d+')
            FortyPlus = tr.xpath('.//td[13]/text()').re(r'\d+')
            Lng = tr.xpath('.//td[14]/text()').re(r'\d+')
            Sck = tr.xpath('.//td[15]/text()').re(r'\d+')
            SckY = tr.xpath('.//td[16]/text()').re(r'\d+')
            PlayerHref = tr.xpath('.//a/@href').extract_first()
            Passing = 'https://www.nfl.com' + PlayerHref
            
            yield {
            'Name' : Name,
            'Year' : Year,
            'PassYards' : PassYards, 
            'YdsPerAtt' : YdsPerAtt,
            'Att' : Att, 
            'Cmp' : Cmp,
            'Completion %' : CompPerc,
            'TD' : TD,
            'INT': int,
            'Rate' : Rate,
            '1st' : First,
            '1st %' : FirstPerc,
            '20+' : TwentyPlus,
            '40+' : FortyPlus,
            'Lng' : Lng,
            'Sck' : Sck,
            'SckY' : SckY,
            }
            
    
    