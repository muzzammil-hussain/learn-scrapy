import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class BBCNewsSpider(CrawlSpider):
    name = "thenumbers"
    root = "https://www.the-nuumbers.com"
    allowed_domains = ["www.the-numbers.com"]
    rotate_user_agent = True
    start_urls = [
        "https://www.the-numbers.com",
    ]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=("",)),
             callback="parse", follow=True),
    )

    def parse(self, response):
        print(response)