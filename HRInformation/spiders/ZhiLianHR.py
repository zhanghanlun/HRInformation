# -*- coding: utf-8 -*-
import scrapy
from HRInformation.items import HrinformationItem

class ZhilianhrSpider(scrapy.Spider):

    name = 'ZhiLianHR'
    allowed_domains = ['zhaopin.com']
    start_urls = ['https://xiaoyuan.zhaopin.com/full/0/0_0_160400_0_0_-1_0_1_0']
    offset=1

    def parse(self, response):

        node_list = response.xpath("//ul[@class='searchResultListUl']/li")

        for node in node_list:
            item = HrinformationItem()
            item['position_name'] = node.xpath("./div[1]/div[2]/p[1]/a/text()").extract()[0]
            item['position_attribute'] = node.xpath("./div[1]/div[2]/p[1]/span/text()").extract()[0]
            item['position_link'] = node.xpath("./div[1]/div[2]/p[1]/a/@href").extract()[0]
            item['work_location'] = node.xpath("./div[1]/div[2]/p[2]/span[1]/span/em/text()").extract()[0]
            item['company_name'] = node.xpath("./div[1]/div[1]/p[1]/span/text()").extract()[0]

            item['position_link'] = 'http:' + item['position_link']

            second_url = item['position_link']

            item['salary'] = " "

            yield scrapy.Request(second_url, meta={'item': item}, callback=self.second_parse)

        if self.offset <= 1294:
            self.offset = self.offset + 1
            url = "https://xiaoyuan.zhaopin.com/full/0/0_0_160400_0_0_-1_0_" + str(self.offset) + '_0'
            yield scrapy.Request(url, callback=self.parse)

    def second_parse(self, response):

        item = response.meta['item']

        item['publish_time'] = response.xpath('//*[@id="liJobPublishDate"]//text()').extract()[0]
        if len(response.xpath('//*[@id="divMain"]/div/div/div[1]/div[1]/ul[1]/li[8]/text()'))==0:
            item['company_type']=" "
        else:
            item['company_type'] = response.xpath('//*[@id="divMain"]/div/div/div[1]/div[1]/ul[1]/li[8]/text()').extract()[
            0]

        item['position_information'] = response.xpath(
            '//*[@id="divMain"]/div/div/div[1]/div[2]/div[2]/div/div/p/text()').extract()

        item['position_type'] = response.xpath('//*[@id="divMain"]/div/div/div[1]/div[1]/ul[2]/li[4]/text()').extract()[
            0]

        item['people_number']= response.xpath('//*[@id="divMain"]/div/div/div[1]/div[1]/ul[2]/li[6]/text()').extract()[0]
        # item['']
        people_number=item['people_number'][0]+item['people_number'][1]
        if( item['people_number'][1] == '人'):
            item['people_number'] = item['people_number'][0]
        elif people_number=='若干':
            item['people_number'] = '10'
        else:
            item['people_number'] = people_number
        yield item
