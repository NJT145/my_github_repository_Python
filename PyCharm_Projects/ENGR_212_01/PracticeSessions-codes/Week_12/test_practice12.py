from practice12 import *
#Part A
c=Tweet()
#the name of the company taken just as example
#c.randomsample("Best Buy.txt", "Best Buy.txt")


#Part B
cl= docclass.naivebayes(docclass.getwords)
c.trainall(cl)

#Part C
#c.training(cl,"Best Buy.txt", "Best Buy.txt")
#print c.read("Best Buy.txt", "Best Buy.txt")
# Part D
#c.accuracy(cl,"Best Buy.txt", "Best Buy.txt")
#Part E
#c.tentimes(cl,"Best Buy.txt", "Best Buy.txt")
c.dumptofile(cl)
