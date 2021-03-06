# -*- coding: utf-8 -*-
# 定义编码格式

from math import tanh
from pysqlite2 import dbapi2 as sqlite


def dtanh(y):
    return 1.0 - y * y


class searchnet:
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)

    def __del__(self):
        self.con.close()

    def maketables(self):
        self.con.execute('create table hiddennode(create_key)')
        self.con.execute('create table wordhidden(fromid,toid,strength)')
        self.con.execute('create table hiddenurl(fromid,toid,strength)')
        self.con.commit()

    # the default strength is -0.5
    def getStrength(self, fromid, toid, layer):
        if layer == 0:
            table = 'wordhidden'
        else:
            table = 'hiddenurl'
        res = self.con.execute(
            'select strength from %s where fromid =%d and toid=%d' % (table, fromid, toid)).fetchone()
        if res is None:
            if layer == 0: return -0.2
            if layer == 1: return 0
        return res[0]

    # update the strength
    def setStrength(self, fromid, toid, layer, strength):
        if layer == 0:
            table = 'wordhidden'
        else:
            table = 'hiddenurl'
        res = self.con.execute(
            'select rowid from %s where fromid =%d and toid=%d' % (table, fromid, toid)).fetchone()
        if res is None:
            self.con.execute(
                'insert into %s (fromid, toid,strength) values (%d,%d,%f)' % (table, fromid, toid, strength))
        else:
            rowid = res[0]
            self.con.execute('update %s set strength=%f where rowid=%d' % (table, strength, rowid))

    #
    def generateHiddenNode(self, wordids, urls):
        if len(wordids) > 3: return None
        createkey = '_'.join(sorted([str(wi) for wi in wordids]))
        res = self.con.execute("select rowid from hiddennode where create_key ='%s' " % createkey).fetchone()

        if res is None:
            cur = self.con.execute("insert into hiddennode (create_key) values ('%s')" % createkey)
            hiddenid = cur.lastrowid

            for wordid in wordids:
                self.setStrength(wordid, hiddenid, 0, 1.0 / len(wordids))
            for urlid in urls:
                self.setStrength(hiddenid, urlid, 1, 0.1)
            self.con.commit()

    #
    def getAllHiddenIDs(self, wordids, urlids):
        ll = {}
        for wordid in wordids:
            cur = self.con.execute('select toid from wordhidden where fromid=%d' % wordid)
            for row in cur: ll[row[0]] = 1
        for urlid in urlids:
            cur = self.con.execute('select fromid from hiddenurl where toid=%d' % urlid)
            for row in cur: ll[row[0]] = 1
        return ll.keys()

    #
    def setUpNetwork(self, wordids, urlids):
        # list of values
        self.wordids = wordids
        self.hiddenids = self.getAllHiddenIDs(wordids, urlids)
        self.urlids = urlids

        # output the nodes
        self.ai = [1.0] * len(self.wordids)
        self.ah = [1.0] * len(self.hiddenids)
        self.ao = [1.0] * len(self.urlids)

        # the matrix
        self.wi = [[self.getStrength(wordid, hiddenid, 0) for hiddenid in self.hiddenids] for wordid in self.wordids]
        self.wo = [[self.getStrength(hiddenid, urlid, 1) for urlid in self.urlids] for hiddenid in self.hiddenids]

    #
    def feedForward(self):
        for i in range(len(self.wordids)):
            self.ai[i] = 1.0

        for j in range(len(self.hiddenids)):
            sum = 0.0
            for i in range(len(self.wordids)):
                sum += self.ai[i] * self.wi[i][j]
            self.ah[j] = tanh(sum)

        for k in range(len(self.urlids)):
            sum = 0.0
            for j in range(len(self.hiddenids)):
                sum += self.ah[j] * self.wo[j][k]
            self.ao[k] = tanh(sum)

        return self.ao[:]

    def getResult(self, wordids, urlids):
        self.setUpNetwork(wordids, urlids)
        return self.feedForward()

    #
    def backPropGate(self, targets, N=0.5):
        output_deltas = [0.0] * len(self.urlids)
        for k in range(len(self.urlids)):
            error = targets[k] - self.ao[k]
            output_deltas[k] = dtanh(self.ao[k]) * error

        hidden_deltas = [0.0] * len(self.hiddenids)
        for j in range(len(self.hiddenids)):
            error = 0.0
            for k in range(len(self.urlids)):
                error += output_deltas[k] * self.wo[j][k]
            hidden_deltas[j] = dtanh(self.ah[j]) * error

        # renew the output w
        for j in range(len(self.hiddenids)):
            for k in range(len(self.urlids)):
                change = output_deltas[k] * self.ah[j]
                self.wo[j][k] += N * change

        # renew the input w
        for i in range(len(self.wordids)):
            for j in range(len(self.hiddenids)):
                change = hidden_deltas[j] * self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N * change

    def trainQuery(self, wordids, urlids, selectedurl):
        # create a hiddennode if needed
        self.generateHiddenNode(wordids, urlids)
        self.setUpNetwork(wordids, urlids)
        self.feedForward()
        targets = [0.0] * len(urlids)
        targets[urlids.index(selectedurl)] = 1.0
        self.backPropGate(targets)
        self.updateDatabase()

    def updateDatabase(self):
        for i in range(len(self.wordids)):
            for j in range(len(self.hiddenids)):
                self.setStrength(self.wordids[i], self.hiddenids[j], 0, self.wi[i][j])

        for j in range(len(self.hiddenids)):
            for k in range(len(self.urlids)):
                self.setStrength(self.hiddenids[j], self.urlids[k], 1, self.wo[j][k])

        self.con.commit()
