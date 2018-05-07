import json
from scrapy import FormRequest
from scrapy.spiders import CrawlSpider


class SoKamalSpider(CrawlSpider):
    name = "sokamal"
    endpoint = "https://fishry-api-live.azurewebsites.net/collection_request"
    store_id = "480EFD74-078D-4CF2-AC68-270940ED408F"
    rotate_user_agent = True

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
                    "collection_id[]": item,
                    "varients": "[]"
                })

    # def start_requests(self):
    #     for item in self.collections:
    #         yield FormRequest(
    #             self.endpoint,
    #             formdata={
    #                 "storeID": self.store_id,
    #                 "take": "999",
    #                 "skip": "0",
    #                 "collection_inclusion": "true",
    #                 "order_by": "__createdat",
    #                 "order_by_seq": "desc",
    #                 "varients_inclusion": "true",
    #                 "status": "true",
    #                 "collection_id[]": item,
    #                 "varients": "[]"
    #             })

    def parse(self, response):
        print("**********************")
        json_response = json.loads(response.body_as_unicode())
        for item in json_response:
            print(item["id"])
