import advancedclassify

agesonly = advancedclassify.loadmatch('agesonly.csv',allnum=True)

# matchmaker = advancedclassify.loadmatch('matchmaker.csv')
#print matchmaker

# advancedclassify.plotagematches(agesonly)
# avgs = advancedclassify.lineartrain(agesonly)
# print avgs

# print advancedclassify.dpclassify([30,30],avgs)
# print advancedclassify.milesdistance(matchmaker[0].data[4],matchmaker[1].data[4])
# numericalset=advancedclassify.loadnumerical()
# numericalset = advancedclassify.loadmatch('newmatch.csv')
# scaledset,scalf=advancedclassify.scaledata(numericalset)
# avgs=advancedclassify.lineartrain(scaledset)

# print numericalset[0].data
# offset = advancedclassify.getoffset(numericalset)
# print advancedclassify.nlclassify([30,30],agesonly,offset)

# ssoffset = advancedclassify.getoffset(scaledset)
# print numericalset[0].match
# print advancedclassify.nlclassify(scalf(numericalset[0].data),scaledset,ssoffset)

# newrow=[28.0,-1,-1,26.0,-1,1,2,0.8]
# print advancedclassify.nlclassify(scalf(newrow),scaledset,ssoffset)

print advancedclassify.testLIBSVM()