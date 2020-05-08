# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import JianshuCrawlItem as Jitem


class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    start_urls = ['http://jianshu.com/']
    rules = (
        Rule(LinkExtractor(allow=r'.+/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        # 使用xpath获取数据
        title = response.xpath("//h1[@class='_2zeTMs']/text()").get()
        author = response.xpath("//a[@class='_1OhGeD']/text()").get()
        avatar = response.xpath("//img[@class='_13D2Eh']/@src").get()
        pub_time = response.xpath("//div[@class='s-dsoj']/time/text()").get()
        content = response.xpath("//article[@class='_2rhmJa']").get()
        origin_url = response.url
        article_id = origin_url.split("?")[0].split("/")[-1]
        print(title)  # 提示爬取的文章
        item = Jitem(
            title=title,
            author=author,
            avatar=avatar,
            pub_time=pub_time,
            origin_url=origin_url,
            article_id=article_id,
            content=content,
        )
        yield item
