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
        cur = self.con.execute("select rowid from %s where %s = '%s' " % (table, field, value))
        res = cur.fetchone()
        if res == None:
            cur = self.con.execute("insert into %s (%s) values ('%s')" % (table, field, value))
            return cur.lastrowid
        else:
            return res[0]

    # 为网页建立索引
    def addtoIndex(self, url, soup):
        if self.isIndexd(url): return
        print  'indexing ' + url

        # get every word
        text = self.getTextOnly(soup)
        words = self.sparatewords(text)

        # get the id of the url
        urlid = self.getEntryID('urllist', 'url', url)

        # attach the word with the url
        for i in range(len(words)):
            word = words[i]
            if word in ignoreWords: continue
            wordid = self.getEntryID('wordlist', 'word', word)
            self.con.execute("insert into wordlocation(urlid,wordid,location) values (%d,%d,%d)" % (urlid, wordid, i))
            # print 'Indexing %s' % url

    # 提取文字（no html）
    def getTextOnly(self, soup):
        v = soup.string
        if v == None:
            c = soup.contents
            resulttext = ''
            for t in c:
                subtext = self.getTextOnly(t)
                resulttext += subtext + '\n'
            return resulttext
        else:
            return v.strip()

    # 根据空白分词
    def sparatewords(self, text):
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s != '']

    # 判断是否索引
    def isIndexd(self, url):
        u = self.con.execute("select rowid from urllist where url = '%s'" % url).fetchone()
        if u != None:
            v = self.con.execute('select * from wordlocation where urlid = %d' % u[0]).fetchone()
            if v != None: return True
        return False

    # 添加链接
    def addLinkRef(self, urlFrom, urlTo, linkText):
        words = self.sparatewords(linkText)
        fromid = self.getEntryID('urllist', 'url', urlFrom)
        toid = self.getEntryID('urllist', 'url', urlTo)
        if fromid == toid: return
        cur = self.con.execute("insert into link(fromid,toid) values (%d,%d)" % (fromid, toid))
        linkid = cur.lastrowid
        for word in words:
            if word in ignoreWords: continue
            wordid = self.getEntryID('wordlist', 'word', word)
            self.con.execute("insert into linkwords(linkid,wordid) values (%d,%d)" % (linkid, wordid))

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

    # PageRank
    def calculatePageRank(self, iterations=20):
        # the score table should be inited
        self.con.execute('drop table if exists pagerank')
        self.con.execute('create table pagerank(urlid primary key, score)')

        # the init score of every url is 1,0
        self.con.execute('insert into pagerank select rowid, 1.0 from urllist')
        self.dbcommit()

        for i in range(iterations):
            print "Iteration %d" % (i)
            for (urlid,) in self.con.execute('select rowid from urllist'):
                pr = 0.15

                for (linker,) in self.con.execute('select distinct fromid from link where toid=%d' % urlid):
                    linkingpr = self.con.execute('select score from pagerank where urlid = %d' % linker).fetchone()[0]

                    linkingcount = self.con.execute('select count(*) from link where fromid=%d' % linker).fetchone()[0]
                    pr += 0.85 * (linkingpr / linkingcount)
                self.con.execute('update pagerank set score=%f where urlid=%d' % (pr, urlid))
            self.dbcommit()

    def printPageRankResult(self):
        cur = self.con.execute('select * from pagerank order by score desc')
        for i in range(3): print cur.next()


class searcher:
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)

    def __del__(self):
        self.con.close()

    def getMatchRows(self, q):
        # sql string
        fieldlist = 'w0.urlid'
        tablelist = ''
        clauselist = ''
        wordids = []

        # split words by space
        words = q.split(' ')
        tablenumber = 0

        for word in words:
            wordrow = self.con.execute("select rowid from wordlist where word='%s'" % word).fetchone()
            if wordrow != None:
                wordid = wordrow[0]
                wordids.append(wordid)
                if tablenumber > 0:
                    tablelist += ','
                    clauselist += ' and '
                    clauselist += 'w%d.urlid=w%d.urlid and ' % (tablenumber - 1, tablenumber)
                fieldlist += ',w%d.location' % tablenumber
                tablelist += 'wordlocation w%d' % tablenumber
                clauselist += 'w%d.wordid=%d' % (tablenumber, wordid)
                tablenumber += 1

        fullquery = 'select %s from %s where %s' % (fieldlist, tablelist, clauselist)
        cur = self.con.execute(fullquery)
        rows = [row for row in cur]

        return rows, wordids

    def getScoredList(self, rows, wordids):
        totalscores = dict([(row[0], 0) for row in rows])

        weights = [(1.0, self.locationscore(rows)), (1.0, self.frequencyScore(rows)), (1.0, self.pageRankScore(rows))]

        for (weight, scores) in weights:
            for url in totalscores:
                totalscores[url] += weight * scores[url]

        return totalscores

    def getUrlName(self, id):
        return self.con.execute("select url from urllist where rowid=%d" % id).fetchone()[0]

    def query(self, q):
        rows, wordids = self.getMatchRows(q)
        scores = self.getScoredList(rows, wordids)
        rankedscores = sorted([(score, url) for (url, score) in scores.items()], reverse=1)
        for (score, urlid) in rankedscores[0:10]:
            print '%f\t%s' % (score, self.getUrlName(urlid))

    def normalizescores(self, scores, smallIsBetter=0):
        vsmall = 0.00001
        if smallIsBetter:
            minscore = min(scores.values())
            return dict([(u, float(minscore) / max(vsmall, l)) for (u, l) in scores.items()])
        else:
            maxscore = max(scores.values())
            if maxscore == 0: maxscore = vsmall
            return dict([(u, float(c) / maxscore) for (u, c) in scores.items()])

    # 按词频的评价函数
    def frequencyScore(self, rows):
        counts = dict([(row[0], 0) for row in rows])
        for row in rows: counts[row[0]] += 1
        return self.normalizescores(counts)

    # 根据单词位置评价函数
    def locationscore(self, rows):
        locations = dict([(row[0], 1000000) for row in rows])
        for row in rows:
            loc = sum(row[1:])
            if loc < locations[row[0]]: locations[row[0]] = loc

        return self.normalizescores(locations, smallIsBetter=1)

    # simple count
    def inBoundLinkScore(self, rows):
        uniqueurls = set([row[0] for row in rows])
        inboundcount = dict(
            [(u, self.con.execute('select count(*) from link where toid=%d' % u).fetchone()[0]) for u in uniqueurls])
        return self.normalizescores(inboundcount)

    def pageRankScore(self, rows):
        pageranks = dict(
            [(row[0], self.con.execute('select score from pagerank where urlid=%d' % row[0]).fetchone()[0]) for row in
             rows])
        maxrank = max(pageranks.values())
        normalizedscores = dict([(u, float(l) / maxrank) for (u, l) in pageranks.items()])
        return normalizedscores
