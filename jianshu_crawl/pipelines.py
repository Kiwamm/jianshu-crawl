# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi


class JinshuAsyncPipeline(object):
    '''
    异步储存爬取的数据
    '''

    def __init__(self):
        # 连接本地mysql
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'debian-sys-maint',
            'password': 'lD3wteQ2BEPs5i2u',
            'database': 'jianshu',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql = None

    @property
    def sql(self):
        # 初始化sql语句
        if not self._sql:
            self._sql = '''
                  insert into article(id,title,content,author,avatar,pub_time,origin_url,article_id)\
                  values(null,%s,%s,%s,%s,%s,%s,%s)'''
        return self._sql

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item, item)  # 提交数据
        defer.addErrback(self.handle_error, item, spider)  # 错误处理

    def insert_item(self, cursor, item):
        # 执行SQL语句
        cursor.execute(self.sql, (item['title'], item['content'], item['author'],
                                  item['avatar'],
                                  item['pub_time'],
                                  item['origin_url'], item['article_id']))

    def handle_error(self, item, error, spider):
        print('Error!')


class JianshuCrawlPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'debian-sys-maint',
            'password': 'lD3wteQ2BEPs5i2u',
            'database': 'jianshu',
            'charset': 'utf8mb4',
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (item['title'], item['content'], item['author'],
                                       item['avatar'], item['pub_time'],
                                       item['origin_url'], item['article_id']))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = '''
            insert into article(id,title,content,author,avatar,pub_time,origin_url,article_id)\
            values(null,%s,%s,%s,%s,%s,%s,%s)'''
        return self._sql
