import random
from time import clock

def exercise1_1(A):
   # sort the list (O(nlogn)), iterate over it  and create a separate list of unique numbers. 
   uniqA=[]
   
   sortedA= sorted(A)
   if len(sortedA) != 0 :
       uniqA.append(sortedA[0])

   for i in range(1,len(sortedA)):
       if sortedA[i] != sortedA[i-1] :
           uniqA.append(sortedA[i])
   return uniqA

def exercise1_2(A):
    # Similarly to first implementation but delete the duplicates directly from the sorted list. Deleting from the middle of a list is O(n). Check the run time below to see the huge slow down
    
   sortedA= sorted(A)

   i=1
   while i < len(sortedA):
       if sortedA[i] == sortedA[i-1] :
           del sortedA[i]
       else:
           i=i+1
           
   return sortedA


def exercise1_3(A):
   # Iterate through the list and create a dict of unique items (O(n)). Compare the the run time with other implementations
   
   uniqA=dict()
   
   for i in A:
       if i not in uniqA:
           uniqA[i]= True
               
   return uniqA.keys()

A=[]
n=100
for i in range(n):
    A.append(random.randint(1, 100))

print  len(exercise1_1(A))
print  len(exercise1_2(A))
print  len(exercise1_3(A))

A=[]
n=100000
repeat=10
for i in range(n):
    A.append(random.randint(1, 10000))


start = clock()
for i in xrange(repeat):
    exercise1_1(A)
print 'exercise1_1:New List', clock() - start


start = clock()
for i in xrange(repeat):
    exercise1_2(A)
print 'exercise1_2:In Place', clock() - start

start = clock()
for i in xrange(repeat):
    exercise1_3(A)
print 'exercise1_3: Dict (Hash)', clock() - start


    
