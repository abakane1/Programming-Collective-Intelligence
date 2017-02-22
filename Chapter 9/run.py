import advancedclassify

agesonly = advancedclassify.loadmatch('agesonly.csv',allnum=True)

matchmaker = advancedclassify.loadmatch('matchmaker.csv')
#print matchmaker

# advancedclassify.plotagematches(agesonly)
avgs = advancedclassify.lineartrain(agesonly)
# print avgs

# print advancedclassify.dpclassify([30,30],avgs)
# print advancedclassify.milesdistance(matchmaker[0].data[4],matchmaker[1].data[4])
numericalset=advancedclassify.loadnumerical()
print numericalset[0].data