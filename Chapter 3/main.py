# -*- coding: utf-8 -*-
# 定义编码格式
import clusters
#
#
blognames, words, data = clusters.readFile('Result/blogdata.txt')
clust=clusters.hcluster(data)

#clusters.printcluster(clust, labels=blognames)

# 输出树状图，查看聚类结果
#clusters.drawDendrogram(clust, blognames)

# 根据单词聚类，输出结果
rdata = clusters.rotateMatrix(data)
wordclust = clusters.hcluster(rdata)
clusters.drawDendrogram(wordclust, labels=words, jpeg='Result/wordclust.jpg')