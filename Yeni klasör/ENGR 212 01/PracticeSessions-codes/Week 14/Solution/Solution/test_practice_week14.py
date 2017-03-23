from optimization1 import *

#step 1
domain=[(0,8)]*(len(people)*2)
geneticoptimize(domain,schedulecost,popsize=50,step=1,mutprob=0.2,elite=0.2)

#step 2
