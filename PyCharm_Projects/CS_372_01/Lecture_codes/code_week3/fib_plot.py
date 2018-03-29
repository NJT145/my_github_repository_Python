from time import clock
import matplotlib.pyplot as plt

def fib1(n) :
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib1(n-1) + fib1(n-2)

def fib2(n) :
    if n == 0:
        return 0
    f=[0,1]
    for i in range(2,n+1) :
        f.append(f[i-1] + f[i-2])
    return f[n]

fib1_time=[]
fib2_time=[]
n=[]
for i in range(1,37,1):
    n.append(i)
    start = clock()
    fib1(i)
    fib1_time.append(clock()-start)
    start = clock()
    fib2(i)
    fib2_time.append(clock()-start)    
    
print n
print fib1_time
print fib2_time

plt.plot(n, fib1_time, 'b-', n, fib2_time, 'r-')
plt.xlabel('n')
plt.ylabel('run time')
plt.show()