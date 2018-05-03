import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class SoKamalSpider(CrawlSpider):
    name = "sokamal"
    allowed_domains = ["https://sokamal.com"]
    #rotate_user_agent = True
    start_urls = [
        "https://sokamal.com",
    ]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=("",)),
             callback="parse_list", follow=True),
    )

    def parse(self, response):
        pass