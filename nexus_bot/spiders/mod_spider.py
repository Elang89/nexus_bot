
import scrapy

from scrapy import Request, FormRequest
from scrapy.utils.response import open_in_browser
from nexus_bot.items import ModFile
from nexus_bot.utils.util_funcs import convert_to_mb


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
        XPATH_MOD_FILES = '//li[@id="mod-page-tab-files"]/a'
        file_tab = response.xpath(XPATH_MOD_FILES)
        file_tab_option = file_tab.xpath('@href').extract_first()
        file_tab_link = response.urljoin(file_tab_option)

        yield Request(url=file_tab_link, callback=self.extract_file_data)

    def extract_file_data(self, response):
        XPATH_FILE_DATA = '//dt[@class="clearfix accopen"]'
        XPATH_DOWNLOAD_LINKS = '//a[span[text()="Manual Download"]]'
        ORIGINAL_NAME = 'FOOK'

        names = {'FOOK v1-13 ESMs and ReadMes',
                 'FOOK v1-13 Required Files', 'FOOK v1-13 Optional Files'}

        mod_id = list(filter(str.isdigit, response.url))
        mod_id = ''.join(mod_id)
        file_data = response.xpath(XPATH_FILE_DATA)
        file_download_links = response.xpath(XPATH_DOWNLOAD_LINKS)
        mod_record = ModFile(mod_id=mod_id, mod_name=ORIGINAL_NAME)
        mod_record['files'] = {}
        total_size = 0

        for element in file_data:
            name = element.xpath(
                'span[normalize-space(text())]/text()').extract_first()
            if name in names:
                link = file_download_links.xpath('@href').extract_first()
                file_size = element.xpath(
                    '''span/div[@class="file-download-stats clearfix"]/ul/
                    li[@class="stat-filesize"]/div/div[@class="stat"]/text()''').extract_first()
                numeric_size = convert_to_mb(file_size)
                total_size += numeric_size
                mod_record['files'][name] = (numeric_size, link)
                print(name)
        mod_record['total_MBs'] = total_size
        yield mod_record
