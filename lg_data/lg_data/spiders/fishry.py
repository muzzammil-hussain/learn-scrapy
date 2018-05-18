import json
import datetime
from lg_data.items import Product
from lg_data.fishry_configs import stores
from scrapy import FormRequest, Request
from scrapy.spiders import CrawlSpider


class FishrySpider(CrawlSpider):
    name = "fishry"
    api_endpoint = "https://fishry-api-live.azurewebsites.net/collection_request"
    collections_endpoint = "https://fishry.azure-mobile.net/tables/collection?$filter=((collectionVisibility eq true) and (storeID eq '{}'))&$top=1000"
    links_endpoint = "https://fishry.azure-mobile.net/tables/link_list?$filter=(storeID eq '{}')&$top=1000"
    zumo_id = "egepBriQNqIKWucZFzqpQOMwdDmzfs16"
    rotate_user_agent = True

    def start_requests(self):
        for store in stores.keys():
            if stores.get(store)["active"]:
                yield Request(
                    self.links_endpoint.format(store),
                    headers={
                        "X-ZUMO-APPLICATION": self.zumo_id
                    },
                    meta={
                        "store_uuid": store
                    }
                )

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        ignore_links = stores.get(response.meta["store_uuid"])

        current_menu = []
        for item in json_response:
            if item["link_handle"] == "main-menu":
                links = json.loads(item["link_list"])
                for link in links:
                    for sub_link in link["list"]:
                        if sub_link.get("linkCollection") and sub_link.get("linkCollection") not in ignore_links:
                            current_menu.append(sub_link["linkCollection"])

        yield Request(
            self.collections_endpoint.format(response.meta["store_uuid"]),
            headers = {
                "X-ZUMO-APPLICATION": self.zumo_id
            },
            meta={
                "store_uuid": response.meta["store_uuid"],
                "current_menu": current_menu
            },
            callback=self.parse_collections
        )

    def parse_collections(self, response):
        json_response = json.loads(response.body_as_unicode())
        current_menu = response.meta["current_menu"]

        for item in json_response:
            if item["collectionUrl"] in current_menu:
                yield FormRequest(
                    self.api_endpoint,
                    formdata={
                        "storeID": response.meta["store_uuid"],
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
                    meta={
                        "store_id": stores.get(response.meta["store_uuid"])["id"],
                        "store_name": stores.get(response.meta["store_uuid"])["name"]
                    },
                    callback=self.parse_category,
                    errback=self.parse_errors
                )

    def parse_category(self, response):
        json_response = json.loads(response.body_as_unicode())
        for item in json_response:
            if item["inventoryQuantity"] >= 1:
                product = Product()

                images = []
                raw_images = json.loads(item["productImage"])
                for raw_image in raw_images.values():
                    images.append({
                        "name": raw_image["Image"],
                        "featured": raw_image["Featured"]
                    })

                collections = []
                raw_collections = json.loads(item["productCollections"])
                for raw_collection in raw_collections.values():
                    collections.append(raw_collection["name"])

                attribs = {}
                if item["productMultiOptions"]:
                    raw_options = json.loads(item["productMultiOptionsList"])
                    for raw_option in raw_options:

                        if raw_option["custom"]:
                            values = []
                            for raw_value in raw_option["value"]:
                                values.append(raw_value["value"])
                            attribs[raw_option["custom"]] = values
                            continue

                        if raw_option["optionSelected"]:
                            values = []
                            for raw_value in raw_option["value"]:
                                values.append(raw_value["value"])
                            attribs[raw_option["optionSelected"]] = values
                            continue

                product["store_id"] = response.meta["store_id"]
                product["store_name"] = response.meta["store_name"]
                product["vendor_product_id"] = item["id"]
                product["scraped_at"] = datetime.datetime.utcnow()
                product["created_at"] = item["__createdAt"]
                product["updated_at"] = item["__updatedAt"]
                product["name"] = item["productName"]
                product["images"] = images
                product["sku"] = item["productSKU"]
                product["url"] = "https://sokamal.com/product/{}".format(item["productUrl"])
                product["variants"] = ""
                product["price"] = item["productPrice"]
                product["quantity"] = item["inventoryQuantity"]
                product["description"] = item["productDescription"]
                product["collections"] = collections
                product["attribs"] = attribs

                yield product

    def parse_errors(self, response):
        pass
