# -*- coding: utf-8 -*-
# 抓取腾信招聘网站的招聘信息
# @author 张函仑
# @version 1.0
import scrapy
from HRInformation.items import HrinformationItem

class TencenthrSpider(scrapy.Spider):
    # 项目名称
    name = 'TencentHR'
    allowed_domains = ['tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?keywords=&lid=0&tid=87']

    def parse(self, response):
        node_list=response.xpath("//tr[@class='even']|//tr[@class='odd']")

        for node in node_list:
            item = HrinformationItem()

            item['position_name'] = node.xpath("./td[1]/a/text()").extract()[0]

            second_url = node.xpath("./td[1]/a/@href").extract()[0]
            second_url = "https://hr.tencent.com/" + second_url

            item['position_link'] =  second_url

            if len(node.xpath("./td[2]/text()").extract()):
                item['position_type'] = node.xpath("./td[2]/text()").extract()[0]
            else:
                item['position_type'] = ""

            item['people_number'] = node.xpath("./td[3]/text()").extract()[0]

            item['work_location'] = node.xpath("./td[4]/text()").extract()[0]

            item['publish_time'] = node.xpath("./td[5]/text()").extract()[0]

            item['salary'] = ''

            item['company_name'] = '腾讯'

            item['position_attribute'] = '社会招聘'

            item['company_type'] = 'BAT互联网公司'

            yield scrapy.Request(second_url, meta={'item': item}, callback=self.parse_second)

        # 循环抓取页面
        if len(response.xpath("//a[@id='next' and @class='nocative']"))==0:
            # 获取下一个页面的URL地址
            url=response.xpath("//a[@id='next']/@href").extract()[0]
            print(url)
            yield scrapy.Request("https://hr.tencent.com/"+url,callback=self.parse)

    def parse_second(self, response):
        item = response.meta['item']
        item['position_information'] = response.xpath("//ul[@class='squareli']/li/text()").extract()[0]

        yield item
