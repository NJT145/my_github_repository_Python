import docclass

cl = docclass.naivebayes(docclass.getwords)
docclass.sampletrain(cl)
print cl.prob('quick rabbit','good')
print cl.prob('quick rabbit','bad')

print cl.categories()
print cl.fc
print cl.cc
print cl.classify('quick rabbit').split()