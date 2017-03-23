from time import clock
import random
import matplotlib.pyplot as plt


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


size=[]
selection_time=[]


repeat=20

for n in range(100000,1000001,200000):
    size.append(n)
    A=random.sample(xrange(n),n)
    start=clock()
    for i in range(repeat):
        selection(A,len(A)/2)
    selection_time.append(clock()-start)

print size
print selection_time

plt.plot(size, selection_time, 'r-')
plt.xlabel('list size(n)')
plt.ylabel('run time')
plt.show()
