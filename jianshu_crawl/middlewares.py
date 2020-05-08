# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from selenium import webdriver
from scrapy.http.response.html import HtmlResponse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


class SeleniumDownloadMiddleware(object):
    def __init__(self):
        self.driver = webdriver.Chrome()

    def process_request(self, request, spider):
        while True:
            # 超时重新请求
            try:
                self.driver.set_page_load_timeout(1)
                self.driver.get(request.url)
            except:
                pass
            finally:
                try:
                    # 等待ajax加载，超时了就重来
                    WebDriverWait(self.driver, 1).until(
                        expected_conditions((By.CLASS_NAME, 'rEsl9f'))
                    )
                except:
                    continue
                finally:
                    break
        url = self.driver.current_url
        source = self.driver.page_source
        response = HtmlResponse(url=url, body=source, request=request, encoding='utf-8')
        return response
