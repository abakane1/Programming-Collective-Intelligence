import clusters

blognames, words, data = clusters.readFile('Result/blogdata.txt')
clust=clusters.hcluster(data)
clusters.printcluster(clust, labels=blognames)