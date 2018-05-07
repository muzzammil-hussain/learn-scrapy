import json
from lg_data.items import Product
from scrapy import FormRequest, Request
from scrapy.spiders import CrawlSpider


class FishrySpider(CrawlSpider):
    name = "fishry"
    api_endpoint = "https://fishry-api-live.azurewebsites.net/collection_request"
    collections_endpoint = "https://fishry.azure-mobile.net/tables/collection?$filter=((collectionVisibility eq true) and (storeID eq '{}'))&$top=1000"
    store_id = "480EFD74-078D-4CF2-AC68-270940ED408F"
    rotate_user_agent = True

    stores = [
        {
            "id": "480EFD74-078D-4CF2-AC68-270940ED408F",
            "zumo_id": "egepBriQNqIKWucZFzqpQOMwdDmzfs16",
            "name": "sokamal",
            "active": True,
            "ignore": ["frontpage", "duvet-set", "sheet-set", "media-gallery", "summer-18-catalog" ]
        }
    ]

    def start_requests(self):
        for store in self.stores:
            yield Request(
                self.collections_endpoint.format(store["id"]),
                headers = {
                    "X-ZUMO-APPLICATION": store["zumo_id"]
                },
                meta={
                    "ignore": store["ignore"]
                }
            )

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        for item in json_response:
            if item["collectionUrl"] not in response.meta["ignore"]:
                yield FormRequest(
                    self.api_endpoint,
                    formdata={
                        "storeID": self.store_id,
                        "take": "999",
                        "skip": "0",
                        "collection_inclusion": "true",
                        "order_by": "__createdat",
                        "order_by_seq": "desc",
                        "varients_inclusion": "true",
                        "status": "true",
                        "collection_id[]": item["id"],
                        "varients": "[]"
                    },
                    callback=self.parse_category,
                    errback=self.parse_errors
                )

    def parse_category(self, response):
        json_response = json.loads(response.body_as_unicode())
        for item in json_response:
            product = Product()

            images = []
            raw_images = json.loads(item["productImage"])
            for image in raw_images:
                images.append({
                    "name": image["Image"],
                    "featured": image["Featured"]
                })



            product["id"] = item["id"]
            product["created_at"] = item["__createdAt"]
            product["updated_at"] = item["__updatedAt"]
            product["name"] = item["productName"]
            product["images"] = images
            product["sku"] = item["productSKU"]
            product["url"] = item["productUrl"]
            product["variants"] = ""
            product["price"] = item["productPrice"]
            product["quantity"] = item["inventoryQuantity"]
            product["description"] = item["productDescription"]
            product["meta"] = ""

            yield product

    def parse_errors(self, response):
        pass
