# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import open_in_browser

class PubMedSpider(scrapy.Spider):
    name = 'PubMed'
    # allowed_domains = ['https://www.ncbi.nlm.nih.gov/pubmed/']
    start_urls = ['https://www.ncbi.nlm.nih.gov/pubmed/']

    def __init__(self, term=None, *args, **kwargs):
        super(PubMedSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.ncbi.nlm.nih.gov/pubmed/?term=' + term]

    def parse(self, response):
        # open_in_browser(response)
        for article in response.css('div.rprt'):
            yield {
                'num': article.css('div.rprtnum > span ::text').extract_first()[:-1],
                'title': article.css('a ::text').extract_first(),
                'url': 'https://www.ncbi.nlm.nih.gov' + article.css('a ::attr(href)').extract_first(),
                'authors': article.css('p.desc ::text').extract_first().split(','),
                'details': article.css('p.details ::text').extract_first(),
                'PMID': article.css('dd::text').extract_first(),
                'similar': 'https://www.ncbi.nlm.nih.gov' + article.css('p.links > a ::attr(href)').extract_first(),
                'type': article.css('a.status_icon ::text').extract_first(),
                }
        for next_page in response.css('a.next'):
            yield response.follow(next_page, self.parse)