import scrapy
from scrapy.spiders import CrawlSpider, Rule

class SoKamalSpider(CrawlSpider):
    name = "sokamal"
    allowed_domains = ["sokamal.com"]
    rotate_user_agent = True
    collections = [
        "643E9641-4E2D-49F8-A39D-B714CE336169",
        "47CF236F-CCBB-43CB-A78E-467D77064CCA",
        "71F2EFF8-1DFC-49A8-994B-E16CBC8F4A96",
        "2BAC0315-3290-4811-B0EB-577C66B7C1F9",
        "04F34B3B-ADD6-4505-B926-2BD58664E691",
        "53DEE257-82C6-4A3B-A5F8-F019AA4AE4C8",
        "5488125A-3483-4FC6-BCB6-FC2E363952BA"
        "0B068C4A-811E-46D6-B4AA-1B84D92A818C",
        "F06CE5AA-F8EA-4C54-863A-A15D8E244DAD"
    ]
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