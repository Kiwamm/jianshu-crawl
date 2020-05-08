# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from time import sleep
from selenium import webdriver
from scrapy.http.response.html import HtmlResponse


class SeleniumDownloadMiddleware(object):
    def __init__(self):
        self.driver = webdriver.Chrome()

    def process_request(self, request, spider):
        self.driver.get(request.url)
        sleep(1)  # 防止数据未加载
        url = self.driver.current_url
        source = self.driver.page_source
        response = HtmlResponse(url=url, body=source, request=request, encoding='utf-8')
        return response
