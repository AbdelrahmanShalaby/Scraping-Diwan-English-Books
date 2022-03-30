# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class EnglishBooksDataSpider(CrawlSpider):
    name = 'english_books_data'
    allowed_domains = ['diwanegypt.com']
    user_agent = "Mozilla/5.0 (Windows; U; Windows NT 6.1) AppleWebKit/532.9.7 (KHTML, like Gecko) Version/5.0.1 Safari/532.9.7"
    #user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
    def start_requests(self):
        yield scrapy.Request(url= 'https://diwanegypt.com/product-category/books/english-books',headers={
            'User-Agent': self.user_agent
        })
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[@class='woocommerce-LoopProduct-link woocommerce-loop-product__link']"),\
             callback='parse_item', follow=True,process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="//a[@class='next page-numbers']"),
             process_request='set_user_agent')
    )
    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent
        return request
    def parse_item(self, response):
        instock = response.xpath("(//p[@class='stock out-of-stock'])[1]/text()").get()
        if instock == None:
            instock = "Instock"
        yield{
            "title": response.xpath("(//h1)[1]/text()").get(),
            "author": response.xpath("(//span[@class='author'])[1]/text()").get(),
            "price": response.xpath("(//bdi)[1]/text()").get(),
            "in_stock": instock,
            "book_genre": response.xpath("(//a[@class='crumb'])[3]/text()").get(),
            "book_url": response.url,
            #"user_agent": response.request.headers['User-Agent']
        }
