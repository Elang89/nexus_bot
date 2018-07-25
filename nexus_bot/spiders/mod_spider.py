
import scrapy

from scrapy.utils.response import open_in_browser
from scrapy import Request, FormRequest


class ModSpider(scrapy.Spider):
    name = 'mod_spider'

    def start_requests(self):
        url = 'https://www.nexusmods.com/newvegas/'
        yield Request(url=url, callback=self.make_search)

    def make_search(self, response):
        XPATH_SEARCH_FORM = '//*[@id="nav-search"]/form'
        search_term = 'FOOK'
        category = 'Mods'

        form = response.xpath(XPATH_SEARCH_FORM)
        form_method = response.xpath('@method').extract_first()
        form_url = form.xpath('@action').extract_first()
        form_data = {'gsearch': search_term, 'gsearchtype': category}

        yield FormRequest(url=form_url, callback=self.search_results,
                          method=form_method, formdata=form_data)

    def search_results(self, response):
        XPATH_MOD_TILES = '//div[@class="tile-content"]/h3/a'
        mod = 'FOOK - New Vegas'
        mod_list = response.xpath(XPATH_MOD_TILES)

        for element in mod_list:
            name = element.xpath('text()').extract_first()
            if name == mod:
                link = element.xpath('@href').extract_first()
                yield Request(url=link, callback=self.follow_link)

    def follow_link(self, response):
        open_in_browser(response)
