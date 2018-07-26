# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NexusBotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ModFile(scrapy.Item):
    mod_id = scrapy.Field()
    mod_name = scrapy.Field()
    files = scrapy.Field()
    total_MBs = scrapy.Field()
