import scrapy
from scrapy.spiders import CrawlSpider, Rule

class SoKamalSpider(CrawlSpider):
    name = "sokamal"
    allowed_domains = ["sokamal.com"]
    rotate_user_agent = True
    start_urls = [
        "https://sokamal.com/collections/grand-sale-stitched",
        "https://sokamal.com/collections/grand-sale-unstitched",
        "https://sokamal.com/collections/pret-summer18",
        "https://sokamal.com/collections/unstitched-summer18",
        "https://sokamal.com/collections/silk-range-18",
        "https://sokamal.com/collections/pret-bottoms",
        "https://sokamal.com/collections/unstitched-bottoms",
        "https://sokamal.com/collections/dupatta",
        "https://sokamal.com/collections/scarves",
    ]

    def parse(self, response):
        print("*****************************")
        print(response.request.headers)
        print(response.xpath(".//title/text()").extract_first())