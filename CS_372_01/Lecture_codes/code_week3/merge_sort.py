from time import clock
import random

import sys
sys.setrecursionlimit(10000)

def merge(X,Y):

    if len(X) == 0:
        return Y
    elif len(Y) == 0:
        return X
    elif X[0] <= Y[0]:
         return [X[0]] + merge (X[1:],Y)           
    else:
         return [Y[0]] + merge (X,Y[1:])  

def iterative_merge(X,Y):
    indexX=0
    indexY=0
    merged=[]
    while True:
        if indexX == len(X):
            merged.extend(Y[indexY:])
            return merged
        elif indexY == len(Y):
            merged.extend(X[indexX:])
            return merged
        elif X[indexX] <= Y[indexY]:
            merged.append(X[indexX])
            indexX+=1
        else:
            merged.append(Y[indexY])
            indexY+=1
        



def mergesort(A):
    if len(A) <=1 :
        return A
    else:
        middle=len(A)/2
        return merge(mergesort(A[:middle]), mergesort(A[middle:]))


temp=[2, 3, 10, 6, 4, 1, 8, 5, 9, 7]
print mergesort(temp)


from collections import deque
def iterative_mergesort(A):
    queue=deque()

    for i in A :
        queue.append([i])

    while len(queue) > 1 :
        queue.append(merge(queue.popleft(),queue.popleft()))

    return queue.popleft()


temp=[2, 3, 10, 6, 4, 1, 8, 5, 9, 7]
print iterative_mergesort(temp)

A= random.sample(xrange(9000),9000)
repeat=10

start=clock()
for i in range(repeat):
    mergesort(A)
print "mergesort:", clock()-start

start=clock()
for i in range(repeat):
    iterative_mergesort(A)
print "iterative_mergesort:", clock()-start

