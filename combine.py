import scrapy
from scrapy.http import Request


class CombineSpider(scrapy.Spider):
    handle_httpstatus_list = [404]
    name = 'combine'
    allowed_domains = ['nflcombineresults.com']
    start_urls = ['https://nflcombineresults.com/nflcombinedata.php?year={}&pos=&college='
                  .format([str(x) for x in range(1987, 2021)][i]) for i in range(33)]

    def parse(self, response):
        hrefs = response.xpath('//*[contains(@href,"playerpage")]/@href').re('(?<=https://nflcombineresults.com/).+')
        for player in hrefs:
            players = 'https://nflcombineresults.com/' + player
            yield Request(players, callback=self.parse_player)

    def parse_player(self, response):
        first_name = response.xpath('//tr[contains(.,"First Name")]/td[2]/text()').re(r'\w+')
        last_name = response.xpath('//tr[contains(.,"Last Name")]/td[2]/text()').re(r'\w+')
        draft_year = response.xpath('//tr[contains(.,"Draft Class")]/td[2]/text()')[0].re(r'\d+')
        college = response.xpath('//tr[contains(.,"College")]/td[2]/text()').re(r'\w+')
        position = response.xpath('//tr[contains(.,"Position")]/td[2]/text()')[0].re(r'\w+')
        height = response.xpath('//tr[contains(.,"Height")]/td[2]/text()')[0].re(r'\d+')
        weight = response.xpath('//tr[contains(.,"Weight")]/td[2]/text()')[0].re(r'\d+')
        bmi = response.xpath('//tr[contains(.,"BMI")]/td[2]/text()')[0].re(r'\d+.\d+')
        arm_length = response.xpath('//tr[contains(.,"Arm Length")]/td[2]/text()')[0].re(r'\d+.\d+')
        hand_size = response.xpath('//tr[contains(.,"Hand Size")]/td[2]/text()')[0].re(r'\d+.\d+')
        wing_span = response.xpath('//tr[contains(.,"Wingspan")]/td[2]/text()')[0].re(r'\d+.\d+')
        forty_yard_dash = response.xpath('//tr[contains(.,"40 Yard Dash")]/td[2]/text()')[0].re(r'\d+.\d+')
        forty_yard_mph = response.xpath('//tr[contains(.,"40 Yard (MPH)")]/td[2]/text()')[0].re(r'\d+.\d+')
        twenty_yard_split = response.xpath('//tr[contains(.,"20 Yard Split")]/td[2]/text()')[0].re(r'\d+.\d+')
        bench = response.xpath('//tr[contains(.,"Bench Press")]/td[2]/text()')[0].extract()
        qb_ball_velocity = response.xpath('//tr[contains(.,"QB Ball Velocity")]/td[2]/text()')[0].extract()
        vertical_leap = response.xpath('//tr[contains(.,"Vertical Leap")]/td[2]/text()')[0].re(r'\d+.\d+')
        broad_jump = response.xpath('//tr[contains(.,"Broad Jump")]/td[2]/text()')[0].re(r'\d+.\d+')
        twenty_yrd_shuttle = response.xpath('//tr[contains(.,"20 Yd Shuttle")]/td[2]/text()')[0].re(r'\d+.\d+')
        three_cone = response.xpath('//tr[contains(.,"Three Cone")]/td[2]/text()')[0].re(r'\d+.\d+')

        yield {'First Name': first_name,
               'Last Name': last_name,
               'Draft Year': draft_year,
               'College': college,
               'Position': position,
               'Height (inch)': height,
               'Weight (lbs)': weight,
               'BMI': bmi,
               'ArmLength (inch)': arm_length,
               'Hand Size (inch)': hand_size,
               'Wing Span (inch)': wing_span,
               '40 Yard Dash (s)': forty_yard_dash,
               '40 Yard (MPH)': forty_yard_mph,
               '20 Yard Split (s)': twenty_yard_split,
               'Bench Press': bench,
               'QB Ball Velocity': qb_ball_velocity,
               'Vertical Leap (inch)': vertical_leap,
               'Broad Jump (inch)': broad_jump,
               '20 Yd Shuttle (s)': twenty_yrd_shuttle,
               'Three Cone': three_cone

               }
