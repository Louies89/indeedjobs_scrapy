# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import json

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('output.json', 'w')
        self.file.write('[\n') # Before writting Json Info add '[' to denote list starting

    def close_spider(self, spider):
        self.file.write(']')  # Before closing the file end with ']' to denote list end
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + ",\n"
        self.file.write(line)
        return item