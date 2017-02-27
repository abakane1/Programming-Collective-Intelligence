import docclass

#cl = docclass.classifier(docclass.getwords)
#cl.train('the quick brown fox jumps over the lazy dog','good')
#cl.train('make quick money in the online casino','bad')
#print cl.fcount('quick','good')
#print cl.fcount('quick','bad')

#docclass.sampletrain(cl)
#print cl.fprob('quick','good')

#print cl.weightedprob('money','good',cl.fprob)

#docclass.sampletrain(cl)
#print cl.weightedprob('money','good',cl.fprob)

cl =docclass.naivebayes(docclass.getwords)

docclass.sampletrain(cl)

print cl.classify('quick rabbit', default='unknown')
print cl.classify('quick money', default='unknown')

cl.setthreshold('bad',3.0)
print cl.classify('quick money',default='unknown')