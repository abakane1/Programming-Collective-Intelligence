# -*- coding: utf-8 -*-
# 定义编码格式
import urllib2
from BeautifulSoup import *
from urlparse import urljoin
from pysqlite2 import dbapi2 as sqlite

# 忽略单词表
ignoreWords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])


class crawler:
    # inited the database name
    def __init__(self, dbanme):
        self.con = sqlite.connect(dbanme)

    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()

    # 获取条目的ID,如果不存在，添加db中
    def getEntryID(self, table, field, value, createnew=True):
        return None

    # 为网页建立索引
    def addtoIndex(self, url, soup):
        print 'Indexing %s' % url

    # 提取文字（no html）
    def getTextOnly(self, soup):
        return None

    # 根据空白分词
    def sparatewords(self, text):
        return None

    # 判断是否索引
    def isIndexd(self, url):
        return False

    # 添加链接
    def addLinkRef(self, urlFrom, urlTo, linkText):
        pass

    # 对一组网页进行广度有限搜索，直到一定深度
    # 同时建立索引
    def crawl(self, pages, depth=2):
        for i in range(depth):
            newpages = set()
            for page in pages:
                try:
                    c = urllib2.urlopen(page)
                except:
                    print "Could not open %s" % page
                    continue
                soup = BeautifulSoup(c.read())
                self.addtoIndex(page, soup)

                links = soup('a')
                for link in links:
                    if 'href' in dict(link.attrs):
                        url = urljoin(page, link['href'])
                        if url.find("'") != -1: continue
                        url = url.split('#')[0]  # 去掉位置部分
                        if url[0:4] == 'http' and not self.isIndexd(url):
                            newpages.add(url)
                        linkText = self.getTextOnly(link)
                        self.addLinkRef(page, url, linkText)

                self.dbcommit()
            pages = newpages

    # 创建数据库表
    def createIndexTables(self):
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid, wordid, location)')
        self.con.execute('create table link(fromid integer, toid integer)')
        self.con.execute('create table linkwords(wordid, linkid)')
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')
        self.dbcommit()
