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

        # next_page_url = response.xpath('//a[text()="Następna"]/@href').extract_first()
        # yield Request(next_page_url)

    def parse_flat(self, response):
        tytul = response.xpath('//*[@class="col-md-offer-content"]//h1//text()').extract_first()
        cena = response.xpath('//*[@class="param_price"]//strong/text()').extract_first()
        cena_za_metr = response.xpath('//*[@class="param_price"]/text()')[1].extract()
        powierzchnia = response.xpath('//*[@class="param_m"]//strong/text()').extract_first()
        pokoje = response.xpath('//strong/text()')[7].extract()
        pietro =  response.xpath('//*[@class="param_floor_no"]//text()')[1].extract()
        rynek =  response.xpath('//*[@class="sub-list"]//li//text()')[1].extract()
        rodzaj_zabudowy = response.xpath('//*[@class="sub-list"]//li//text()')[3].extract()
        material_budynku = response.xpath('//*[@class="sub-list"]//li//text()')[5].extract()
        okna = response.xpath('//*[@class="sub-list"]//li//text()')[7].extract()
        ogrzewanie = response.xpath('//*[@class="sub-list"]//li//text()')[9].extract()
        rok_budowy = response.xpath('//*[@class="sub-list"]//li//text()')[11].extract()
        stan_wykonczenia = response.xpath('//*[@class="sub-list"]//li//text()')[13].extract()
        czynsz = response.xpath('//*[@class="sub-list"]//li//text()')[15].extract()
        forma_wlasnosci = response.xpath('//*[@class="sub-list"]//li//text()')[17].extract()
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
            'rynek': rynek,
            'rodzaj_zabudowy': rodzaj_zabudowy,
            'material_budynku': material_budynku,
            'okna': okna,
            'ogrzewanie': ogrzewanie,
            'rok_budowy': rok_budowy,
            'stan_wykonczenia':  stan_wykonczenia,
            'czynsz': czynsz,
            'forma_wlasnosci': forma_wlasnosci,
            'zdjecia': zdjecia,
            'informacje_dodatkowe': informacje_dodatkowe,
            'opis_finalny': opis_finalny,
            'wspolrzedne_lat': wspolrzedne_lat,
            'wspolrzedne_lon': wspolrzedne_lon,
        }
