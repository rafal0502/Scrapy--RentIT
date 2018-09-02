# -*- coding: utf-8 -*-
#!/usr/bin/python

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
        kategoria = response.xpath('//*[@class="p-t-5"]//*[@class="title"]/text()').extract()[0].split(" ",1)[1]
        tytul = response.xpath('//*[@class="col-md-offer-content"]//h1//text()').extract_first()

        lista = response.xpath('//*[@class="main-list"]//li//text()').extract()
        strip_lista = [x.strip() for x in lista]

        if  "Cena" in strip_lista:
            try:
                cena = strip_lista[strip_lista.index("Cena")+1]
            except IndexError:
                cena = None
            try:
                cena_za_metr = strip_lista[strip_lista.index("Cena")+2]
            except IndexError:
                cena_za_metr = None
        else:
            cena = None
        if "Powierzchnia" in strip_lista:
            powierzchnia = strip_lista[strip_lista.index("Powierzchnia")+1]
        else:
            powierzchnia = None
        if "Liczba pokoi" in strip_lista:
            pokoje = strip_lista[strip_lista.index("Liczba pokoi")+1]
        else:
            pokoje = None
        if "Piętro" in strip_lista:
            pietro = strip_lista[strip_lista.index("Piętro")+1]
        else:
            pietro = None
        try:
            liczba_pieter = response.xpath('//*[@class="param_floor_no"]//span/text()').extract()[0].strip().split()[1][:-1]
        except IndexError:
            liczba_pieter = None

        sublista = response.xpath('//*[@class="sub-list"]//li//text()').extract()
        sublista_dict = {sublista[i] : sublista[i+1] for i in range(0, len(sublista), 2)}
        zdjecia = response.xpath('//*[@class="col-md-offer-content"]//img/@src')[:5].extract()
        wspolrzedne_lat = response.xpath('//*[@class="ad-map-element"]//@data-lat').extract_first()
        wspolrzedne_lon = response.xpath('//*[@class="ad-map-element"]//@data-lon').extract_first()
        informacje = response.xpath('//*[@class="dotted-list"]//li//text()').extract()
        informacje_dodatkowe = ''.join(informacje)
        opis = response.xpath('//*[@itemprop="description"]//p//text()').extract()
        opis_finalny = ''.join(opis)
        # try:
        #    dzielnica = response.xpath('//*[@class="address-links"]//a').extract()[2].split(">",1)[1].split("<",1)[0]
        # except IndexError:
        #     dzielnica = None
        #2dzielnica = response.xpath('//*[@class="p-t-5"]//a//text()').extract()[2]
        #3dzielnica = response.xpath('//*[@class="breadcrumb"]//li//a//text()').extract()[3:][2]
        strona = "www.otodom.pl"

        lista_2 = response.xpath('//*[@class="left"]//p//text()').extract()
        strip_lista_2 = [y.strip() for y in lista_2]
        split_lista_2 = [y.split(':') for y in strip_lista_2]

        flat_list_2=list()
        for sublist in split_lista_2:
            for item in sublist:
                flat_list_2.append(item)

        if "Nr oferty w Otodom" in flat_list_2:
            nr_oferty_na_stronie = flat_list_2[flat_list_2.index("Nr oferty w Otodom")+1].strip()
        else:
            nr_oferty_na_stronie = None
        if "Nr oferty w biurze nieruchomości" in flat_list_2:
            nr_oferty_w_biurze_nieruchomosci = flat_list_2[flat_list_2.index("Nr oferty w biurze nieruchomości")+1].strip()
        else:
            nr_oferty_w_biurze_nieruchomosci = None
        if "Liczba wyświetleń strony" in flat_list_2:
            liczba_wyswietlen = flat_list_2[flat_list_2.index("Liczba wyświetleń strony")+1].strip()
        else:
            liczba_wyswietlen = None

        lista_3 = response.xpath('//*[@class="right"]//p//text()').extract()
        strip_lista_3 = [y.strip() for y in lista_3]
        split_lista_3 = [y.split(':') for y in strip_lista_3]
        flat_list_3=list()
        for sublist in split_lista_3:
            for item in sublist:
                flat_list_3.append(item)

        if "Data dodania" in flat_list_3:
            data_dodania = flat_list_3[flat_list_3.index("Data dodania")+1].strip()
        else:
            data_dodania = None
        if "Data aktualizacji" in flat_list_3:
            data_aktualizacji = flat_list_3[flat_list_3.index("Data aktualizacji")+1].strip()
        else:
            data_aktualizacji = None

        yield {
            'kategoria': kategoria,
            'tytul': tytul,
            'cena': cena,
            'cena_za_metr': cena_za_metr,
            'powierzchnia': powierzchnia,
            'pokoje': pokoje,
            'pietro': pietro,
            'liczba_pieter': liczba_pieter,
            'cechy' : sublista_dict,
            'zdjecia': zdjecia,
            'informacje_dodatkowe': informacje_dodatkowe,
            'opis_finalny': opis_finalny,
            'wspolrzedne_lat': wspolrzedne_lat,
            'wspolrzedne_lon': wspolrzedne_lon,
            #'dzielnica': dzielnica,
            'strona': strona,
            'nr_oferty_w_biurze_nieruchomosci': nr_oferty_w_biurze_nieruchomosci,
            'nr_oferty_na_stronie': nr_oferty_na_stronie,
            'liczba_wyswietlen': liczba_wyswietlen,
            'data_dodania': data_dodania,
            'data_aktualizacji': data_aktualizacji,
       }
