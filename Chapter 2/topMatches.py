# -*- coding: utf-8 -*-
# 定义编码格式
from recommendations import critics  # 数据层
from ReadRecommendations import sim_distance


# 从字典中返回最为匹配
# 返回结果的个数和相似度函数均为可选参数
def topMatches(prefs, person, n=5, similarity=sim_distance):
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

# print topMatches(critics,'Toby', n=2)
