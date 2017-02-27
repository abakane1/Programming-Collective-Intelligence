import treepredict

#print treepredict.divideset(treepredict.my_data,2,'yes')
print treepredict.giniimpurity(treepredict.my_data)
print treepredict.entropy(treepredict.my_data)
tree = treepredict.buildtree(treepredict.my_data)
treepredict.printtree(tree)