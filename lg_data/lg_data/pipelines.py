# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import pymongo
from scrapy.conf import settings


class MongoPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings["MONGO_URI"]
        )
        db = connection[settings["MONGODB_DB"]]
        self.collection = db[settings["MONGODB_COLLECTION"]]

    def process_item(self, item, spider):

        self.collection.insert(dict(item))
        logging.debug("Item added to database")
        return item

class LgDataPipeline(object):
    def process_item(self, item, spider):
        return item
