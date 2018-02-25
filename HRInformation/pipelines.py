# -*- coding: utf-8 -*-

# Define your item pipelines here
# @author 张函仑
# @version 1.0
# 定义pipelines

import pymysql

class HrinformationPipeline(object):

    def __init__(self):
        #数据库连接
        #阿里云的数据库
        self.db = pymysql.connect(host="47.94.205.132", user="zhanghanlun",
                                  password="123456",
                                  database="zhanghanlun",
                                  charset='utf8',
                                  cursorclass=pymysql.cursors.DictCursor)

    def process_item(self, item, spider):

        d = dict(item)

        # 获取职位详细信息，并且拼接到一起
        d_information = d['position_information']
        p_information = ""
        p_info = ''
        for x in range(len(d_information)):
            p_info = d_information[x]
            p_info.strip()
            p_information = p_information+p_info
        print(p_information)

        p_name = d['position_name']
        p_company = d['company_name']
        company_type=d['company_type']
        p_link = d['position_link']
        p_salary = d['salary']
        w_location = d['work_location']
        p_time = d['publish_time']
        p_type = d['position_type']
        p_attribute = d['position_attribute']
        p_number = d['people_number']

        # 数据库执行SQL语句

        cursor = self.db.cursor()
        sql = 'insert into zhilianHR values("'+ p_name+ '","'+p_company+'","'+company_type+ '",'+ p_number + ',"' + p_type + '","'+w_location + \
              '","' + p_salary + '","' + p_link + '","'+p_information+'","'+p_time+'","'+p_attribute+'");'
        print(sql)

        try:
            cursor.execute(sql)
            self.db.commit()
            print("成功")
        except Exception as e:
            self.db.rollback()
            print("失败")
            print(e)

        return item




    def close_spider(self,spider):
        # 关闭数据库连接
        self.db.close()

