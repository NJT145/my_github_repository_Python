from time import clock
from collections import deque
import random

stack = list()
start = clock()
for i in xrange(100000):
    stack.append(0)
for i in xrange(100000):
    stack.pop()
print 'list as stack', clock() - start

stack = list()
start = clock()
for i in xrange(100000):
    stack.insert(0,i)
for i in xrange(100000):
    stack.pop()
print 'list as queue', clock() - start

stack = list()
start = clock()
for i in xrange(100000):
    stack.append(i)
for i in xrange(100000):
    stack.pop(0)
print 'list as queue', clock() - start

queue = deque()
start = clock()
for i in xrange(100000):
    queue.append(0)
for i in xrange(100000):
    queue.popleft()
print 'deque as queue', clock() - start


queue = deque()
start = clock()
for i in xrange(100000):
    queue.appendleft(0)
for i in xrange(100000):
    queue.pop()
print 'deque as queue', clock() - start


access=random.sample(xrange(100000), 100000)

stack = list()
for i in xrange(100000):
    stack.append(0)
start = clock()
for i in access:
    stack[i]
print 'list access', clock() - start

queue = deque()
for i in xrange(100000):
    queue.append(0)
start = clock()
for i in access:
    queue[i]
print 'deque access', clock() - start



