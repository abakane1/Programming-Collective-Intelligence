# -*- coding: utf-8 -*-
# 定义编码格式
from recommendations import critics

# print (critics['Lisa Rose']['Lady in the Water'])

# pow (n,2) 计算2次方
from math import sqrt


# print(sqrt(pow(4.5-4,2)+pow(1-2,2)))

# 计算两个人基于距离的相似度评价
def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    # 如果没有共同返回0
    if len(si) == 0: return 0
    # 计算所有差值的平方和
    sum_of_sqiares = sum(
        [pow(prefs[person1][item] - prefs[person2][item], 2) for item in prefs[person1] if item in prefs[person2]])

    return 1 / (1 + sqrt(sum_of_sqiares))


print (sim_distance(critics, 'Lisa Rose', 'Gene Seymour'))


# 皮尔逊相关系数，相对于距离算法，修正grade inflation
def sim_pearson(prefs, p1, p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item] = 1
    n = len(si)
    if n == 0: return 1
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * sum2Sq - pow(sum2, 2) / n)
    if den == 0: return 0
    r = num / den
    return r


print sim_pearson(critics, 'Lisa Rose', 'Gene Seymour')


# 从字典中返回最为匹配
# 返回结果的个数和相似度函数均为可选参数
def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]
print topMatches(critics,'Toby', n=2)
