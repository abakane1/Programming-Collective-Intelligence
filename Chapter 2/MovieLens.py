# -*- coding: utf-8 -*-
# 定义编码格式
# metadata please readme.txt in the fold
import os
import calculateSimilarItems


def loadMovieLens(path='/Data/ml-latest-small'):
    path = os.path.join(os.path.dirname(__file__) + path)
    movies = {}
    for line in open(path + '/movies.csv'):
        (id, title) = line.split(',')[0:2]
        movies[id] = title

    prefs = {}
    for line in open(path + '/ratings.csv'):
        (user, movieid, rating, ts) = line.split(',')
        prefs.setdefault(user, {})
        prefs[user][movies[movieid]] = float(rating)

    return prefs


# import thee data
prefs = loadMovieLens()

# print (prefs['87'])
# 给用户ID为88的用户推荐电影
# print(getRecommendations(prefs,'88'))





# it will cost lots of time, you could have a cup of coffee :)
itmesim = calculateSimilarItems.calculateSimilarItems(prefs, n=50)
print calculateSimilarItems.getRecommendedItems(prefs, itmesim, '87')[0:30]
