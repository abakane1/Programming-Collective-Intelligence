# -*- coding: utf-8 -*-
# 定义编码格式
from recommendations import critics  # 数据层
from ReadRecommendations import sim_distance, transFormPrefs, sim_Tanimoto
from topMatches import topMatches


def calculateSimilarItems(prefs, n=10):
    # 建立字典，以给出与这些物品最为相近的所有其他物品
    result = {}

    itemPrefs = transFormPrefs(prefs)
    c = 0
    for item in itemPrefs:
        c += 1
        if c % 100 == 0: print "%d / %d" % (c, len(itemPrefs))
        scores = topMatches(itemPrefs, item, n=n, similarity=sim_Tanimoto)
        result[item] = scores
    return result


# print(calculateSimilarItems(critics,n=10))

# 为某一个推荐电影
def getRecommendedItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}
    for (item, rating) in userRatings.items():
        for (similarity, item2) in itemMatch[item]:
            # 如果用户对物品做过评价，则将其忽略
            if item2 in userRatings: continue
            scores.setdefault(item2, 0)
            # 将相似度作为加权值估计
            scores[item2] += similarity * rating
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity

    rankings = [(score / totalSim[item], item) for item, score in scores.items()]
    rankings.sort()
    rankings.reverse()
    return rankings


# print(getRecommendedItems(critics, calculateSimilarItems(critics), 'Toby'))
