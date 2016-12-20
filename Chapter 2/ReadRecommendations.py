# -*- coding: utf-8 -*-
# 定义编码格式
# 相似度评价函数集

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


# print (sim_distance(critics, 'Lisa Rose', 'Gene Seymour'))


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


# print sim_pearson(critics, 'Lisa Rose', 'Gene Seymour')


# 重构数据格式 将人对每部电影 的评价，转化为每部电影 多个人的评分
def transFormPrefsByMovie(prefs, movie):
    result = {}
    temp ={}
    result.setdefault(movie,temp)
    for person in prefs:
        for item in prefs[person]:
            if item == movie:
                result[movie][person] = prefs[person][item]
    return result

def transFormPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})

            result[item][person]=prefs[person][item]
    return result
# print transFormPrefs(critics, 'Lady in the Water')

# print(critics['Lisa Rose'])

# Tanimoto 相似度
def sim_Tanimoto(prefs, p1,p2):
    common ={}
    for item in prefs[p1]:
        if item in prefs[p2]:
            common[item] = 1

    if len(common) ==0:
        return 0

    common_num = len(common)
    p1_num = len(prefs[p1])
    p2_num = len(prefs[p2])
    res = float(common_num)/(p1_num + p2_num - common_num)

    return res

# print sim_Tanimoto(critics, 'Lisa Rose', 'Gene Seymour')

