# -*- coding: utf-8 -*-
# 定义编码格式
import os

# read the data
def readFile(filename):
    lines = [line for line in file(filename)]
    # first column is the tile
    colnames = line[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        # First row in every column is the row name
        rownames.append(p[0])
        data.append(float(x) for x in p[1:])
    return rownames, colnames, data

# closeness by similarity of pearson
from math import sqrt
def pearson(v1,v2):
    #1 sum
    sum1 = sum(v1)
    sum2 = sum(v2)

    #2 sqrt
    sum1sq = sum(pow(v,2) for v in v1)
    sum2sq = sum(pow(v,2) for v in v2)

    #3 sum
    pSum = sum([v1[i]*v2[i] for i in range(len(v1))])

    #4 calculate the r - pearson score

    num = pSum-(sum1*sum2/len(v1))
    den = sqrt(sum1sq-pow(sum1, 2)/len(v1))*(sum2sq-pow(sum2, 2)/len(v1))
    if den == 0: return 0
    # pearson score 1 两者完全匹配，通过1减，相似的两个元素距离越小
    return 1.0 - num/den

class bicluster:
    def __init__(self, vec, left=None, right=None, distance= 0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance