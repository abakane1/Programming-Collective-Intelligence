# -*- coding: utf-8 -*-
# 定义编码格式
import searchengine

#pagelist =['https://en.wikipedia.org/wiki/Bathsheba']
#crawler = searchengine.crawler('')
#crawler.crawl(pagelist)

crawler = searchengine.crawler('searchindex.db')
crawler.createIndexTables()
