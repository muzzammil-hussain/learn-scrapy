from scrapy import FormRequest, Request
from scrapy.spiders import CrawlSpider, Rule

class SoKamalSpider(CrawlSpider):
    name = "sokamal"
    endpoint = "https://fishry-api-live.azurewebsites.net/collection_request"
    store_id = "480EFD74-078D-4CF2-AC68-270940ED408F"
    #allowed_domains = ["sokamal.com"]
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

    def start_requests(self):
        for item in self.collections:
            yield FormRequest(
                self.endpoint,
                formdata={
                    "storeID": self.store_id,
                    "take": "999",
                    "skip": "0",
                    "collection_inclusion": "true",
                    "order_by": "__createdat",
                    "order_by_seq": "desc",
                    "varients_inclusion": "true",
                    "status": "true",
                    "collection_id[]": item
                })

    def parse(self, response):
        print(response)
