# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 父类标题
    parentTitel = scrapy.Field()
    # 父类链接
    parentUrls = scrapy.Field()
    # 父类文件名
    parentFilename = scrapy.Field

    # 子类标题
    subTitel = scrapy.Field()
    # 子类urls
    subUrls = scrapy.Field()
    # 子类文件名
    subFilename = scrapy.Field()

    # 子类中的 每个小连接
    sonUrls = scrapy.Field()

    # 之类中的所有帖子的标题
    title = scrapy.Field()
    # 子类中的所有帖子的内容
    content = scrapy.Field()
