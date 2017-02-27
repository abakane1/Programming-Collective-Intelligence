import newsfeatures
from Chapter06 import docclass
from Chapter03 import clusters
from numpy import *
import nmf

# Coverting to a Matrix
# allw, artw, artt = newsfeatures.getarticlewords()
# wordmatrix, wordvec = newsfeatures.makematrix(allw, artw)

# print wordvec[0:10]
# print artt[1]
# print wordmatrix[1][0:10]

# Bayesian Classification

# def wordmatrixfeatures(x):
#     return [wordvec[w] for w in range(len(x)) if x[w]>0 ]
# print wordmatrixfeatures(wordmatrix[0])
# classifier = docclass.naivebayes(wordmatrixfeatures)
# classifier.setdb('newstest.db')
# print artt[1]
# print classifier.train(wordmatrix[1],'GIS')

# Clustering
# clust = clusters.hcluster(wordmatrix)
# clusters.drawDendrogram(clust,artt,jpeg='news.jpg')

# Using NumPy
ll=[[1,2,3],[4,5,6]]
m1 = matrix(ll)

m2 = matrix([[1,2],[3,4],[5,6]])

#print m1*m2
#w,h = nmf.factorize(m1*m2, pc =3, iter=100)
#print w*h
#print m1*m2

allw, artw, artt = newsfeatures.getarticlewords()
wordmatrix, wordvec = newsfeatures.makematrix(allw, artw)
v = matrix(wordmatrix)
weights, feat = nmf.factorize(v, pc=20,iter=50)

# Displaying the Result

topp,pn= newsfeatures.showfeatures(weights,feat,artt,wordvec)
