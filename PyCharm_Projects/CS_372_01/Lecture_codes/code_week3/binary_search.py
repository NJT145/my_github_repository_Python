from time import clock
import random


def binarysearch (A, start, end, k):

    middle= (start+end)/2

    if start > end :
        return None
    elif A[middle] == k:
        return middle
    elif A[middle] > k:
        return binarysearch(A, start, middle-1, k)
    else:
        return binarysearch(A, middle+1, end, k)


def binarysearch2 (A, k):

    middle= len(A)/2
    
    if len(A) == 0 :
        return None
    elif A[middle] == k:
        return middle
    elif A[middle] > k:
        left_search=binarysearch2(A[:middle], k)
        return left_search
    else:
        right_search=binarysearch2(A[(middle+1):], k)
        if right_search == None:
            return None
        else:
            return middle + 1 + right_search

def binarysearch3 (A, k):

    return binarysearch (A, 0, len(A)-1, k)
 
        
A= random.sample(xrange(0,2000000,2),1000000)
access= random.sample(xrange(0,2000000,1),1000) 

start=clock()
for i in access:
    binarysearch(A,0,999999,i)
print "binarysearch:", clock()-start

start=clock()
for i in access:
    binarysearch2(A,i)
print "binarysearch2:", clock()-start





