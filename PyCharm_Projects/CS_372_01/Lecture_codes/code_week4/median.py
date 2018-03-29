from time import clock
import random



def selection(S,k):

    v=random.choice(S)
    
    S_left=[]
    S_v=[]
    S_right=[]
    
    for i in S:
        if i==v:
            S_v.append(i)
        elif i < v :
            S_left.append(i)
        else:
            S_right.append(i)

    if k <= len(S_left):
        return selection(S_left,k)
    elif k <= (len(S_left) + len(S_v)):
        return v
    else:
        return selection(S_right, k-len(S_left)-len(S_v))




temp=[2, 3, 10, 6, 4, 1, 8, 5, 9, 7]
print selection(temp, len(temp)/2)



A= random.sample(xrange(1000000),1000000)
repeat=10


start=clock()
for i in range(repeat):
    selection(A,len(A)/2)
print "selection:", clock()-start


