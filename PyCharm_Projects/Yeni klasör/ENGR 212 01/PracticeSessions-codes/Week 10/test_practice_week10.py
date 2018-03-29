import clusters
import mysearchengine


#step1
# -loosely speaking; this step is required to create two methods: getWordFrequency and createWordFrequencyMatrix_perUrl
# -and as being the result of the modification done into addtoindex method, just added a return statement to the end
# so by getting the result of it for each url in crawl method, we create wordsFrequency_perUrl.
# -and by giving this result to createWordFrequencyMatrix_perUrl method as parameter, we get word_frequency matrix.


#step2
dbtables = {'urllist': 'urllist.db', 'wordlocation':'wordlocation.db',
            'link':'link.db', 'linkwords':'linkwords.db', 'pagerank':'pagerank.db'}

crawler= mysearchengine.crawler(dbtables)
crawler.createindextables()

pagelist=["http://www.sehir.edu.tr/en/Pages/Academic/Fakulteler.aspx"]

urls_wordsFrequency = crawler.crawl(pagelist, depth=2)
crawler.createWordFrequencyMatrix_perUrl(urls_wordsFrequency, "wordFrequencyMatrix")

crawler.close()


#step3
urls, words, data = clusters.readfile('wordFrequencyMatrix')
hclust = clusters.hcluster(data)
# #print clusters.printclust(clust, labels=None, n=0)
# #print clusters.printclust(clust, labels=urls)
clusters.drawdendrogram(hclust, urls)

#step4
kclust = clusters.kcluster(data, k=11)
print kclust
