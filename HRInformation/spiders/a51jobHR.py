# -*- coding: utf-8 -*-
# @author 张函仑
# version 1.0
# 爬取51job关于软件开发的职位信息
import scrapy
from HRInformation.items import HrinformationItem

class A51jobhrSpider(scrapy.Spider):
    name = '51jobHR'
    allowed_domains = ['51job.com']
    start_urls = ['http://search.51job.com/jobsearch/search_result.php?fromJs=1&industrytype=32%2C01%2C40&keyword=%E5%BC%80%E5%8F%91&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9']

    def parse(self, response):

        for x in range(4,54):
            str1=str(x)
            node_xpath = '//*[@id="resultList"]/div['+str1+']'
            item = HrinformationItem()
            # 职位名称
            item['position_name'] = response.xpath(node_xpath + '/p/span/a/@title').extract()[0]
            # 职位类型
            item['position_type'] = '技术类'
            # 职位信息链接
            item['position_link'] = response.xpath(node_xpath + '/p/span/a/@href').extract()[0]
            # 公司名称
            item['company_name'] = response.xpath(node_xpath + '/span[1]/a/text()').extract()[0]
            # 工作地点
            item['work_location'] = response.xpath(node_xpath + '/span[2]/text()').extract()[0]
            # 薪资水平
            if (len(response.xpath(node_xpath + '/span[3]/text()').extract()) != 0):
                item['salary'] = response.xpath(node_xpath + '/span[3]/text()').extract()[0]
            else:
                item['salary'] = ""
            # 发布时间
            item['publish_time'] = response.xpath(node_xpath + '/span[4]/text()').extract()[0]
            item['publish_time'] = '2018-' + item['publish_time']

            item['position_attribute'] = '社会招聘'

            second_url = item['position_link']
            yield scrapy.Request(second_url, meta={'item': item}, callback=self.parse_second)

            # 循环抓取页面
        if (len(response.xpath('//*[@id="resultList"]/div[55]/div/div/div/ul/li[8]/a/@href').extract()) != 0):
            next_url = response.xpath('//*[@id="resultList"]/div[55]/div/div/div/ul/li[8]/a/@href').extract()[0]
            print(next_url)
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_second(self,response):

        item = response.meta['item']

        second_node_PNumber_Xpath = "/html/body/div[3]/div[2]/div[3]/div[1]/div/div/span[3]/text()"
        second_node_PInformation_Xpath = "/html/body/div[3]/div[2]/div[3]/div[2]/div/p/text()"
        second_node_PInformation_Xpath1 = '/html/body/div[3]/div[2]/div[3]/div[2]/div/text()'

        item['people_number'] = response.xpath(second_node_PNumber_Xpath).extract()[0]

        people_number=item['people_number'][1]+item['people_number'][2]

        if people_number == '若干':
            item['people_number'] = '10'
        elif people_number[1] == '人':
            item['people_number'] = people_number[0]
        elif people_number[1]=='-':
            item['people_number'] = people_number[0]
        else:
            item['people_number'] = people_number

        item['company_type'] = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()').extract()[0]

        CompanyType = item['company_type'][6] + item['company_type'][7]

        item['company_type'] = CompanyType

        item['position_information'] = response.xpath(second_node_PInformation_Xpath).extract()
        if len(item['position_information']) == 0:
            item['position_information'] = response.xpath(second_node_PInformation_Xpath1).extract()

        yield item
