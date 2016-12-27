# -*- coding: utf-8 -*-
# 定义编码格式
import os


# read the data
def readFile(filename):
    lines = [line for line in file(filename)]
    # first column is the tile
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        # First row in every column is the row name
        rownames.append(p[0])
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data


# closeness by similarity of pearson
from math import sqrt


def pearson(v1, v2):
    # 1 sum
    sum1 = sum(v1)
    sum2 = sum(v2)

    # 2 sqrt
    sum1sq = sum(pow(v, 2) for v in v1)
    sum2sq = sum(pow(v, 2) for v in v2)

    # 3 sum
    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

    # 4 calculate the r - pearson score

    num = pSum - (sum1 * sum2 / len(v1))
    den = sqrt(sum1sq - pow(sum1, 2) / len(v1)) * (sum2sq - pow(sum2, 2) / len(v1))
    if den == 0: return 0
    # pearson score 1 两者完全匹配，通过1减，相似的两个元素距离越小
    return 1.0 - num / den


class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance

def hcluster(rows, distance=pearson):
    distances={}
    currentclusterid = -1

    clust = [bicluster(rows[i], id=i) for i in range(len(rows))]

    while len(clust) >1:
        lowestpair = (0, 1)
        closest = distance(clust[0].vec,clust[1].vec)

        for i in range(len(clust)):
            for j in range(i+1,len(clust)):
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec,clust[j].vec)
                d = distances[(clust[i].id, clust[j].id)]
                if d < closest:
                    closest = d
                    lowestpair = (i, j)

        mergevec = [(clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i]) / 2.0 for i in range(len(clust[0].vec))]

        newcluster = bicluster(mergevec, left=clust[lowestpair[0]], right= clust[lowestpair[1]], distance=closest, id=currentclusterid)

        currentclusterid-=1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]

def printcluster(clust, labels=None, n=0):
    for i in range(n): print ' ',
    if clust.id < 0:
        print '-'
    else:
        if labels==None: print clust.id
        else: print labels[clust.id]

    if clust.left != None: printcluster(clust.left, labels=labels, n=n+1)
    if clust.right != None: printcluster(clust.right, labels=labels, n=n+1)
