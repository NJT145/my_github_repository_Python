from clusters import *

#step 1
createfile = createDataset("delicious.tiny.txt")
# the the name of the file that created is bookmarkdataset.txt

#step 2  hierarchical clustering and K-means clustering

blognames, word, data = readfile('bookmarkdataset.txt')

clust = hcluster(data)
kclust= kcluster(data,k=10)

print printclust(clust, labels=None, n=0)
print printclust(clust, labels=blognames)
print drawdendrogram(clust,blognames, jpeg='clusters.jpg')
# print kclust
#
# #step3
#
newdata = rotatematrix(data)

newclust = hcluster(newdata)
newkclust= kcluster(newdata,k=10)
print "---"
# print draw2d(newclust,word,jpeg='clusters2.jpg')
# print printclust(newclust)
# print drawdendrogram(newclust,blognames, jpeg='clusters.jpg')
# print newkclust
