import numpredict

# print numpredict.winpreice(95.0,3.0)

# print numpredict.winpreice(95.0,8.0)

# print numpredict.winpreice(99.0,1.0)
data = numpredict.winesetdefaut()
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

print numpredict.weightedknn(data,(99.0,5.0))