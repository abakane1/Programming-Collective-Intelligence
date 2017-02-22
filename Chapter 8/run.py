import numpredict
import optimization

# print numpredict.winpreice(95.0,3.0)

# print numpredict.winpreice(95.0,8.0)

# print numpredict.winpreice(99.0,1.0)
# data = numpredict.winesetdefaut()
# print data[0]
# print data[1]

# print numpredict.euclidean(data[0]['input'],data[1]['input'])
# print numpredict.knnestimate(data,(99.0,3.0))
# print numpredict.subtractweight(0.1)
# print numpredict.inverseweight(0.1)
# print numpredict.gaussian(0.1)
# print numpredict.gaussian(1.0)
# print numpredict.subtractweight(1)
# print numpredict.inverseweight(1)
# print numpredict.gaussian(3.0)

# print numpredict.weightedknn(data,(99.0,5.0))

# print numpredict.crossvalidate(numpredict.knnestimate,data)

#def knn3(d,v): return numpredict.knnestimate(d,v,k=3)
# print numpredict.crossvalidate(knn3,data)
#def knn1(d,v): return numpredict.knnestimate(d,v,k=1)
#print numpredict.crossvalidate(knn1,data)


# data = numpredict.wineset2()
# print data

#print numpredict.crossvalidate(knn3,data)

#sdata=numpredict.rescale(data,[10,10,0,0.5])
#print numpredict.crossvalidate(knn3,data)

# costf=numpredict.createcostfunction(numpredict.knnestimate,data)
#print optimization.annealingoptimize(numpredict.weightdomian,costf,step=2)

data = numpredict.wineset3()
# print numpredict.winpreice(99.0,20.0)

# print numpredict.weightedknn(data,[99.0,20.0])

# print numpredict.probguess(data,[99,20],40,80)

# print numpredict.probguess(data,[99,20],120,1200)

# numpredict.cumulativegraph(data,(1,1),120)

numpredict.probabilitygraph(data,(1,1),6)