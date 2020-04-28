# -*- coding: utf-8 -*-
from pymongo import MongoClient
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

''' 
from pymongo import MongoClient

client = MongoClient(host='localhost', port=27017)

db=client['db1']['test']

db.insert_one({'name':'aaa'})

'''# mongo
class ZolUltraPipeline(object):


    def process_item(self, item, spider):
        if (item.get("index" )== 1):
            self.InsertToMongo('cpu',item)
        if (item.get("index") == 2):
            self.InsertToMongo('vga',item)
        if (item.get("index") == 3):
            self.InsertToMongo('board', item)
        if (item.get("index") == 4):
            self.InsertToMongo('disk',item)
        if (item.get("index") == 5):
            self.InsertToMongo('memory', item)
        if (item.get("index") == 6):
            self.InsertToMongo('power', item)
        if (item.get("index") == 7):
            self.InsertToMongo('heat', item)
        if (item.get("index") == 8):
            self.InsertToMongo('box', item)

    def InsertToMongo(self,collection,dict):
        client = MongoClient(host='localhost', port=27017)

        db = client['db1'][collection]

        db.insert_one(dict)