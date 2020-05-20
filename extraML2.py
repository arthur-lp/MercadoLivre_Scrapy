# -*- coding: utf-8 -*-
import scrapy
import time
#from celular.items import celularItem

class MercadoLivre(scrapy.Spider):
    name = 'ML2'
    start_urls = ['https://celulares.mercadolivre.com.br/_Desde_51']

    def parse(self, response):
        for div in response.css("div.item__info-container.highlighted "):
            link = div.css("h2 a::attr(href)").extract_first()
            #time.sleep(2)
            yield response.follow(link, self.parse_desciption)

        next_page = response.css("a.andes-pagination__link.prefetch::attr(href)").extract_first()
        if next_page is not None:
            #time.sleep(5)
            yield scrapy.Request(next_page, self.parse)

    def parse_desciption(self, response):
        #quarta - 14:30 - 15:00
        description  = []
        for li in response.css("li.specs-item.specs-item-primary"):
            primary_label = li.css("strong::text").extract_first()
            primary_desc  = li.css("span::text").extract_first()
            primary_text = primary_label + ":" + primary_desc
            description.append(primary_text)
        for li in response.css("li.specs-item.specs-item-secondary"):
            secondary_label = li.css("strong::text").extract_first()
            secondary_desc  = li.css("span::text").extract_first()
            secondary_text = secondary_label + ": " + secondary_desc
            description.append(secondary_text)
        #title = response.css("header.item-title h1::text").extract_first()
        yield {'desc': description}
