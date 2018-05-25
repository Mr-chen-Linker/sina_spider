# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs


class SinaPipeline(object):

    def process_item(self, item, spider):
        sonUrls = item['sonUrls']

        # 文件名为子链接url中间部分，并将 / 替换为 _，保存为 .txt格式
        filename = sonUrls[7:-6].replace('/', '_')
        filename += ".txt"
        print("开始写入——"*5)
        print(item['subFilename'])
        fp = open(item['subFilename'] + '/' + filename, 'w')
        print(item["content"])
        fp.write(item['content'])
        print("结束写入——" * 5)
        fp.close()


