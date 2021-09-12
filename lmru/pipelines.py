import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class LmruPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroymerlin.ru

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item.data)
        return item


class LmruPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['images']:
            for img in item['images']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)



