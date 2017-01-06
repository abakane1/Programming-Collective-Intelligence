# -*- coding: utf-8 -*-
# 定义编码格式
import os
from PIL import Image, ImageDraw


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
    distances = {}
    currentclusterid = -1

    clust = [bicluster(rows[i], id=i) for i in range(len(rows))]

    while len(clust) > 1:
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)

        for i in range(len(clust)):
            for j in range(i + 1, len(clust)):
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)
                d = distances[(clust[i].id, clust[j].id)]
                if d < closest:
                    closest = d
                    lowestpair = (i, j)

        mergevec = [(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) / 2.0 for i in range(len(clust[0].vec))]

        newcluster = bicluster(mergevec, left=clust[lowestpair[0]], right=clust[lowestpair[1]], distance=closest,
                               id=currentclusterid)

        currentclusterid -= 1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]


def printcluster(clust, labels=None, n=0):
    for i in range(n): print ' ',
    if clust.id < 0:
        print '-'
    else:
        if labels is None:
            print clust.id
        else:
            print labels[clust.id]

    if clust.left is not None: printcluster(clust.left, labels=labels, n=n + 1)
    if clust.right is not None: printcluster(clust.right, labels=labels, n=n + 1)


def getHeight(clust):
    # 递归找到树的高度
    if clust.left is None and clust.right is None: return 1
    return getHeight(clust.left) + getHeight(clust.right)


def getDepth(clust):
    if clust.left is None and clust.right is None: return 0
    return max(getDepth(clust.left), getDepth(clust.right)) + clust.distance


def drawDendrogram(clust, labels, jpeg='Result/cluster.jpg'):
    h = getHeight(clust) * 20
    w = 1200
    depth = getDepth(clust)

    scaling = float(w - 150) / depth

    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.line((0, h / 2, 10, h / 2), fill=(255, 0, 0))

    drawNode(draw, clust, 10, (h / 2), scaling, labels)
    img.save(jpeg, 'JPEG')

# 画图函数,递归画节点
def drawNode(draw, clust, x, y, scaling, labels):
    if clust.id < 0:
        h1 = getHeight(clust.left) * 20
        h2 = getHeight(clust.right) * 20
        top = y - (h1 + h2) / 2
        bottom = y + (h1 + h2) / 2
        ll = clust.distance * scaling
        draw.line((x, top + h1 / 2, x, bottom - h2 / 2), fill=(255, 0, 0))

        draw.line((x, top + h1 / 2, x + ll, top + h1 / 2), fill=(255, 0, 0))

        draw.line((x, bottom - h2 / 2, x + ll, bottom - h2 / 2), fill=(255, 0, 0,))

        drawNode(draw, clust.left, x + ll, top + h1 / 2, scaling, labels)
        drawNode(draw, clust.right, x + ll, bottom - h2 / 2, scaling, labels)
    else:
        draw.text((x + 5, y - 7), labels[clust.id], (0, 0, 0))

# 列聚类
# 分析哪些单词结合使用的情况
#1. 对之前的大矩阵进行转置，获取单词之间相关性
def rotateMatrix(data):
    newdata = []
    for i in range(len(data[0])):
        newrow=[data[j][i] for j in range(len(data))]
        newdata.append(newrow)
    return newdata

# K-means

