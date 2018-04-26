import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class BBCNewsSpider(scrapy.Spider):
    name = "bbcnews"
    root = "http://www.bbc.com"
    allowed_domains = ["www.bbc.com"]
    start_urls = [
        "http://www.bbc.com/news",
    ]

    def parse(self, response):
        nav_links = response.xpath("//div[contains(@class, 'nw-o-news-wide-navigation')]//a//@href").extract()
        for link in nav_links:
            yield scrapy.Request("{}{}".format(self.root, link), callback=self.parse_category)

    def parse_category(self, response):
        # category title
        print(response.xpath("//title/text()").extract_first())
