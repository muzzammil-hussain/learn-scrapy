import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class BBCNewsSpider(CrawlSpider):
    name = "bbcnews"
    root = "http://www.bbc.com"
    allowed_domains = ["www.bbc.com"]
    start_urls = [
        "http://www.bbc.com/news",
    ]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=("//div[contains(@class, 'nw-o-news-wide-navigation')]",)),
             callback="parse_category", follow=True),
    )

    def parse_category(self, response):
        # category title
        print(response.xpath("//title/text()").extract_first())

        # extract the page headline -- few pages will not have headlines
        print(response.xpath("//div[contains(@class, 'buzzard-item') or contains(@class, 'albatross-item') or contains(@class, 'kestrel-item')]/a/@href").extract_first())
