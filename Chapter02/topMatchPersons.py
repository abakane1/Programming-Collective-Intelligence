# -*- coding: utf-8 -*-
# 定义编码格式
# 有一组每个人对每个电影的评分数据。
# 当查看一部电影，获取类似的电影
# 通过其他喜欢这部电影的人，对其他电影的评价。
from recommendations import critics # 数据层
from ReadRecommendations import sim_distance,transFormPrefs
from topMatches import topMatches

def topMatchPersons (prefs, Moive,similarity=sim_distance):
    #print(prefs)
    result ={}
    movies = transFormPrefs(prefs)
    #print(movies)
    result = topMatches(movies,Moive)
    return result



print(topMatchPersons(critics,'Superman Returns'))
