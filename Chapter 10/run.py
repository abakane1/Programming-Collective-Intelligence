import newsfeatures

# Coverting to a Matrix
allw, artw, artt = newsfeatures.getarticlewords()
wordmatrix, wordvec = newsfeatures.makematrix(allw, artw)
print wordvec[0:10]
print artt[1]
print wordmatrix[1][0:10]
