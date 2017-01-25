# -*- coding: utf-8 -*-
# 定义编码格式
import searchengine

#pagelist =['https://en.wikipedia.org/wiki/Bathsheba']
#crawler = searchengine.crawler('')
#crawler.crawl(pagelist)

#crawler = searchengine.crawler('searchindex.db')
#crawler.createIndexTables()
#pagelist =['https://en.wikipedia.org/wiki/Program']
#crawler.crawl(pagelist)

#e = searchengine.searcher('searchindex.db')
#print e.getMatchRows('function program')
#e.query('function religions')

#pagerank
#crawler = searchengine.crawler('searchindex.db')
#crawler.calculatePageRank()

# the result of pagerank
#crawler = searchengine.crawler('searchindex.db')
#crawler.printPageRankResult()
#e = searchengine.searcher('searchindex.db')
#print e.getUrlName(121)

# 1:1:1 locationscore: frequencyscore: pagerankscore
e = searchengine.searcher('searchindex.db')
print e.getMatchRows('function program')
e.query('function program')
