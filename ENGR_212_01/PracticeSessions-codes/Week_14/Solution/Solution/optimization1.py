from optimization import *
def geneticoptimize(domain,costf,popsize=50,step=1,mutprob=0.2,elite=0.2):
  # Mutation Operation
  def mutate(vec):
    i=random.randint(0,len(domain)-1)
    vecb = []
    if random.random()<0.5 and vec[i]>domain[i][0]:
      vecb = vec[0:i]+[vec[i]-step]+vec[i+1:]
    elif vec[i]<domain[i][1]:
      vecb = vec[0:i]+[vec[i]+step]+vec[i+1:]
    else:
        vecb = vec
    #print 'mutate: ', vecb, vec, i
    return vecb
  
  # Crossover Operation
  def crossover(r1,r2):
    i=random.randint(1,len(domain)-2)
    return r1[0:i]+r2[i:]

  # Build the initial population
  pop=[]
  #print 'psize', popsize
  for i in range(popsize):
    vec=[random.randint(domain[i][0],domain[i][1]) 
         for i in range(len(domain))]
    pop.append(vec)
  
  # How many winners from each generation?
  topelite=int(elite*popsize)
  
  # Main loop
  count = 1
  while True:
    for j in  range (len(pop)):
       print j, pop[j]
    scores=[(costf(v),v) for v in pop]
    scores.sort()
    ranked=[v for (s,v) in scores]
    # Start with the pure winners
    pop=ranked[0:topelite]
    # Add mutated and bred forms of the winners
    while len(pop)<popsize:
      if random.random()<mutprob:
        # Mutation
        c=random.randint(0,topelite-1)
        pop.append(mutate(ranked[c]))
        newscore=[(costf(v),v) for v in pop]
        newscore.sort()
      else:
        # Crossover
        c1=random.randint(0,topelite-1)
        c2=random.randint(0,topelite-1)
        pop.append(crossover(ranked[c1],ranked[c2]))
        newscore=[(costf(v),v) for v in pop]
        newscore.sort()
    print scores[0][0] 
    if newscore[0][0]==scores[0][0]:
        count +=1
    else:
        count = 1
    if count == 10:
        return scores[0][1]

