# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time

from selenium import webdriver
from scrapy.http.response.html import HtmlResponse

class SeleniumDownloadMiddleware(object):

    def __init__(self):
        # 加载测试浏览器
        self.driver = webdriver.Chrome(executable_path=r"D:\xsy的秘密小屋\Google\Google\Chrome\Application\chromedriver.exe")

    # request: 则scrapy框架会去服务器加载资源
    # reponse: 则跳过资源下载直接交给解析器方法
    def process_request(self, request, spider):
        self.driver.get(request.url)
        time.sleep(2)
        try:
            while True:
                showMore = self.driver.find_element_by_class_name('show-more')  # 获取标签
                showMore.click()
                time.sleep(0.5)
                if not showMore:
                    break
        except:
            pass
        source = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=source, request=request, encoding='utf-8')
        return response
