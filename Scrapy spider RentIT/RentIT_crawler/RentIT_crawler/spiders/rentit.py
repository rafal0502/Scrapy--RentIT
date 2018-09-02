# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


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
        cena = response.xpath('//*[@class="params-list"]//*[@class="main-list"]//li//strong//text()').extract()[0]
        cena_za_metr = response.xpath('//*[@class="param_price"]/text()')[1].extract()
        powierzchnia = response.xpath('//*[@class="params-list"]//*[@class="main-list"]//li//strong//text()').extract()[1]
        pokoje = response.xpath('//*[@class="params-list"]//*[@class="main-list"]//li//strong//text()').extract()[2]
        pietro = response.xpath('//*[@class="params-list"]//*[@class="main-list"]//li//strong//text()').extract()[3]
        sublista = response.xpath('//*[@class="sub-list"]//li//text()').extract()
        sublista_dict = {sublista[i] : sublista[i+1] for i in range(0, len(sublista), 2)}
        zdjecia = response.xpath('//*[@class="col-md-offer-content"]//img/@src')[:5].extract()
        wspolrzedne_lat = response.xpath('//*[@class="ad-map-element"]//@data-lat').extract_first()
        wspolrzedne_lon = response.xpath('//*[@class="ad-map-element"]//@data-lon').extract_first()
        informacje = response.xpath('//*[@class="dotted-list"]//li//text()').extract()
        informacje_dodatkowe = ''.join(informacje)
        opis = response.xpath('//*[@itemprop="description"]//p//text()').extract()
        opis_finalny = ''.join(opis)
        dzielnica = response.xpath('//*[@class="p-t-5"]//a//text()').extract()[2]
        strona = "www.otodom.pl"
        nr_oferty_w_otodom = response.xpath('//*[@class="left"]//p//text()').extract()[0][20:]
        nr_oferty_w_biurze_nieruchomosci = response.xpath('//*[@class="left"]//p//text()').extract()[1][34:]
        liczba_wyswietlen = response.xpath('//*[@class="left"]//p//text()').extract()[2].strip()[26:]
        data_dodania = response.xpath('//*[@class="right"]//p//text()').extract()[0][14:]
        data_aktualizacji = response.xpath('//*[@class="right"]//p//text()').extract()[1][19:]


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
            'dzielnica': dzielnica,
            'strona': strona,
            'nr_oferty_w_biurze_nieruchomosci': nr_oferty_w_biurze_nieruchomosci,
            'nr_oferty_w_otodom': nr_oferty_w_otodom,
            'liczba_wyswietlen': liczba_wyswietlen,
            'data_dodania': data_dodania,
            'data_aktualizacji': data_aktualizacji,
       }
