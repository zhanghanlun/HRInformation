# -*- coding: utf-8 -*-

# Define here the models for your scraped items
# @author 张函仑
# @version 1.0
# 定义item
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HrinformationItem(scrapy.Item):
    # 职位名称
    position_name = scrapy.Field()
    # 公司名称
    company_name = scrapy.Field()
    # 公司类型
    company_type = scrapy.Field()
    # 招聘人数
    people_number = scrapy.Field()
    # 职位类型
    position_type = scrapy.Field()
    # 工作地点
    work_location = scrapy.Field()
    # 薪酬
    salary = scrapy.Field()
    # 职位详细信息链接
    position_link = scrapy.Field()
    # 职位详细信息
    position_information = scrapy.Field()
    # 发布时间
    publish_time = scrapy.Field()
    # 职位属性 社会招聘还是校园招聘
    position_attribute = scrapy.Field()



