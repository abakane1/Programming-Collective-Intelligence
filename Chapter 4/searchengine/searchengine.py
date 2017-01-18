# -*- coding: utf-8 -*-
# 定义编码格式
import urllib2
from BeautifulSoup import *
from urlparse import  urljoin

# 忽略单词表
ignoreWords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])
class crawler:
    # inited the database name
    def __init__(self,dbanme):
        pass
    def __del__(self):
        pass
    def dbcommit(self):
        pass

    # 获取条目的ID,如果不存在，添加db中
    def getEntryID(self,table, field, value, createnew=True):
        return None

    # 为网页建立索引
    def addtoIndex(self, url, soup):
        print 'Indexing %s' % url

    # 提取文字（no html）
    def getTextOnly(self, soup):
        return None

    # 根据空白分词
    def sparatewords(self,text):
        return None

    # 判断是否索引
    def isIndexd(self,url):
        return False

    # 添加链接
    def addLinkRef(self,urlFrom,urlTo, linkText):
        pass

    # 对一组网页进行广度有限搜索，直到一定深度
    # 同时建立索引
    def crawl(self, pages, depth=2):
        pass

    # 创建数据库表
    def createIndexTables(self):
        pass

