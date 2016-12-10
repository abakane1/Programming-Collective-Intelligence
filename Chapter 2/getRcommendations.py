# -*- coding: utf-8 -*-
# 定义编码格式
# 提供推荐
from recommendations import critics # 数据层
from ReadRecommendations import sim_pearson
from ReadRecommendations import sim_distance

def getRcommendations(prefs, person, similarity=sim_distance):
    totals={}
    simSums={}
    for other in prefs:
        if other == person: continue
        sim=similarity(prefs,person,other)

        if sim<0:continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item]==0:
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                simSums.setdefault(item,0)
                simSums[item]+=sim

        rankings=[(total/simSums[item],item) for item, total in totals.items()]

        rankings.sort()
        rankings.reverse()
        return rankings

print getRcommendations(critics,'Toby',similarity=sim_distance)