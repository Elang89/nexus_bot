
import scrapy

from scrapy.utils.response import open_in_browser
from scrapy_splash import SplashRequest, SplashFormRequest
from scrapy import FormRequest


class ModSpider(scrapy.Spider):
    name = 'mod_spider'

    def start_requests(self):
        url = 'https://www.nexusmods.com/newvegas/'

        yield SplashRequest(url, self.make_search,
                            endpoint='render.html',
                            args={'wait': 0.5},
                            )

    def make_search(self, response):
        XPATH_SEARCH_FORM = '//*[@id="nav-search"]/form'
        search_term = 'FOOK New Vegas'
        category = 'Mods'

        form = response.xpath(XPATH_SEARCH_FORM)
        form_method = response.xpath('@method').extract_first()
        form_url = form.xpath('@action').extract_first()
        form_data = {'gsearch': search_term, 'gsearchtype': category}

        yield SplashFormRequest(url=form_url, callback=self.search_results,
                                method=form_method, formdata=form_data)

    def search_results(self, response):
        file = open('output.html', 'w')
        file.write(response.text)
        file.close()
