from collections import deque

def merge(X,Y):

    if len(X) == 0:
        return Y
    elif len(Y) == 0:
        return X
    elif X[0] <= Y[0]:
         return [X[0]] + merge (X[1:],Y)           
    else:
         return [Y[0]] + merge (X,Y[1:])  


def iterative_mergesort(A):
    queue=deque()

    for i in A :
        queue.append([i])

    while len(queue) > 1 :
        queue.append(merge(queue.popleft(),queue.popleft()))

    return queue.popleft()


temp=[2, 3, 10, 6, 4, 1, 8, 5, 9, 7]
print iterative_mergesort(temp)
