# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from douban5.items import *

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        #self.db[DoubanuserItem.collection].create_index([('id', pymongo.ASCENDING)])

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        if isinstance(item,DoubandetailmoviereviewItem):
            self.db[item.collection].update(
                {'id': item.get('movie_reviewer_id')},
                {'$addToSet':
                    {
                        'movie_review_info': {'$each':item['movie_review_info']}
                    }
                }, True)

        if isinstance(item, DoubandetailmusicreviewItem):
            self.db[item.collection].update(
                {'id': item.get('music_reviewer_id')},
                {'$addToSet':
                    {
                        'music_review_info': {'$each': item['music_review_info']}
                    }
                }, True)

        if isinstance(item,DoubandetailbookreviewItem):
            self.db[item.collection].update(
                {'id': item.get('book_reviewer_id')},
                {'$addToSet':
                    {
                    'book_review_info': {'$each':item['book_review_info']}
                    }
                }, True)

        return item

