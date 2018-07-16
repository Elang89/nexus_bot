from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from nexus_bot.spiders.mod_spider import ModSpider


def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(ModSpider())
    process.start()


if __name__ == '__main__':
    main()
