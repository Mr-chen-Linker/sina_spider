# -*- coding: utf-8 -*-
import scrapy
import os
from ..items import SinaItem


class SinaguiderSpider(scrapy.Spider):
    name = 'sinaguider'
    allowed_domains = ['news.sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        # 用于暂时保存item的列表
        items = []

        # 父类的标题列表
        parentTitel = response.xpath("//div[@id='tab01']//h3/a/text()").extract()
        # 父类的每个链接
        parentUrls = response.xpath("//div[@id='tab01']//h3/a/@href").extract()

        # 子类标题
        subTitel = response.xpath("//div[@id='tab01']//ul/li/a/text()").extract()
        # 子类url
        subUrls = response.xpath("//div[@id='tab01']//ul/li/a/@href").extract()

        # 遍历每个父类，处理url和标题，主要是为了按标题名当做文件夹保存帖子
        for i in range(0, len(parentTitel)):
            # 指定父类的目录及名称
            parentfilename = r"D:/DATA/python/Scrapy_Spiser/douban/douban/data/" + parentTitel[i]

            print(parentfilename)
            # 如果文件不存在就创建该目录

            if (not os.path.exists(parentfilename)):
                os.makedirs(parentfilename)

            # 遍历每个子类
            for j in range(len(subTitel)):

                item = SinaItem()
                # 保存父类的标题和 url
                item["parentTitel"] = parentTitel[i]
                item["parentUrls"] = parentUrls[i]

                # 首先判断子类是否属于父类，判断方法：子类的Url是不是以父类的url开头的
                if_belong = subUrls[j].startswith(item["parentUrls"])
                # 如果子类属于父类的
                if if_belong:
                    subFilename = parentfilename + "/" + subTitel[j]

                    if (not os.path.exists(subFilename)):
                        os.makedirs(subFilename)

                    # 保存子类标题、url、文件路径及名称
                    item["subTitel"] = subTitel[j]
                    item["subUrls"] = subUrls[j]
                    item["subFilename"] = subFilename

                    items.append(item)

                    # 为了使父类的数据可以传递下去，所以在外面遍历items 发请求  # yield scrapy.Request(subUrls[j], callback=self.second_parse)
        # 发送每个小类url的Request请求，得到Response连同包含meta数据 一同交给回调函数 second_parse 方法处理
        for item in items:
            yield scrapy.Request(item["subUrls"], meta={"meta_1": item}, callback=self.second_parse)

    def second_parse(self, response):
        '''处理请求子类链接所的到请求的'''

        # 保存当初发送请求时传过来的item数据
        meta_1 = response.meta["meta_1"]

        # 得到子类中的 所有的文章链接
        sonUrls = response.xpath('//a/@href').extract()

        items = []
        for i in range(0, len(sonUrls)):
            # 去除无效链接，即开头须是父类的连接，结尾须是.shtml
            if_belong = sonUrls[i].endswith(".shtml") and sonUrls[i].startswith(meta_1["parentUrls"])

            if if_belong:
                item = SinaItem()

                item["parentTitel"] = meta_1["parentTitel"]
                item["parentUrls"] = meta_1["parentUrls"]
                item["subTitel"] = meta_1["subTitel"]
                item["subUrls"] = meta_1["subUrls"]
                item["subFilename"] = meta_1["subFilename"]
                item["sonUrls"] = sonUrls[i]

                items.append(item)
        # 遍历，发送每个子类下面的每个链接的请求，并传递以上的item数据，交给content_parse函数处理响应
        for item in items:
            yield scrapy.Request(item["sonUrls"], meta={"meta_2": item}, callback=self.content_parse)

    def content_parse(self, response):
        '''获取每个帖子的标题和内容的方法'''
        # 保存传递过来的元数据
        item = response.meta["meta_2"]

        # 文章的标题
        title = response.xpath("//h1[@class='main-title']/text()")
        content_list = response.xpath("//div[@class='article']/p/text()").extract()
        content = ""
        # 合并内容列表为一个字符串
        for content_one in content_list:
            content += content_one

        item["title"] = title
        item["content"] = content

        yield item
