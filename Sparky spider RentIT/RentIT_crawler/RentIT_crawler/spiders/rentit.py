# -*- coding: utf-8 -*-
import scrapy


class RentitSpider(scrapy.Spider):
    name = 'rentit'
    allowed_domains = ['otodom.pl']
    start_urls = ['http://otodom.pl/']

    def parse(self, response):
        pass