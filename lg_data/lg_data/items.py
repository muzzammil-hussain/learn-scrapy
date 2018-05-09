# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class Product(Item):
    vendor_product_id = Field()
    created_at = Field()
    updated_at = Field()
    name = Field()
    images = Field()
    sku = Field()
    url = Field()
    variants = Field()
    price = Field()
    quantity = Field()
    description = Field()
    collections = Field()