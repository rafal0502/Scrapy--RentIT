# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
# from geopy.geocoders import Nominatim


class RentitSpider(scrapy.Spider):
    name = 'rentit'
    allowed_domains = ['otodom.pl']
    start_urls = ['http://otodom.pl/sprzedaz/mieszkanie/warszawa/']

    def parse(self, response):
        mieszkania = response.xpath('//h3/a/@href').extract()
        for mieszkanie in mieszkania:
            yield Request(mieszkanie, callback=self.parse_flat)

        next_page_url = response.xpath('//a[text()="Następna"]/@href').extract_first()
        yield Request(next_page_url)


    def parse_flat(self, response):
        tytul = response.xpath('//*[@class="col-md-offer-content"]//h1//text()').extract_first()
        cena = response.xpath('//*[@class="param_price"]//strong/text()').extract_first()
        cena_za_metr = response.xpath('//*[@class="param_price"]/text()')[1].extract()
        powierzchnia = response.xpath('//*[@class="param_m"]//strong/text()').extract_first()
        pokoje = response.xpath('//strong/text()')[7].extract()
        pietro =  response.xpath('//*[@class="param_floor_no"]//text()')[1].extract()

        sublista = response.xpath('//*[@class="sub-list"]//li//text()').extract()
        sublista_dict = {sublista[i] : sublista[i+1] for i in range(0, len(sublista), 2)}

        zdjecia = response.xpath('//*[@class="col-md-offer-content"]//img/@src')[:5].extract()
        wspolrzedne_lat = response.xpath('//*[@class="ad-map-element"]//@data-lat').extract_first()
        wspolrzedne_lon = response.xpath('//*[@class="ad-map-element"]//@data-lon').extract_first()
        

        informacje = response.xpath('//*[@class="dotted-list"]//li//text()').extract()
        informacje_dodatkowe = ''.join(informacje)
        opis = response.xpath('//*[@itemprop="description"]//p//text()').extract()
        opis_finalny = ''.join(opis)



        yield {
            'tytul': tytul,
            'cena': cena,
            'cena_za_metr': cena_za_metr,
            'powierzchnia': powierzchnia,
            'pokoje': pokoje,
            'pietro': pietro,
            'cechy' : sublista_dict,
            'zdjecia': zdjecia,
            'informacje_dodatkowe': informacje_dodatkowe,
            'opis_finalny': opis_finalny,
            'wspolrzedne_lat': wspolrzedne_lat,
            'wspolrzedne_lon': wspolrzedne_lon,
        }
