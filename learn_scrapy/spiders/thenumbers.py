import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class TheNumbersSpider(CrawlSpider):
    name = "thenumbers"
    root = "https://www.the-nuumbers.com"
    allowed_domains = ["www.the-numbers.com"]
    #rotate_user_agent = True
    start_urls = [
        "https://www.the-numbers.com/daily-box-office-chart",
    ]

    # rules = (
    #     Rule(LinkExtractor(allow=(), restrict_xpaths=("",)),
    #          callback="parse_list", follow=True),
    # )

    def parse(self, response):
        movies = response.xpath(".//div[@id='page_filling_chart']//table//tr")
        for movie in movies