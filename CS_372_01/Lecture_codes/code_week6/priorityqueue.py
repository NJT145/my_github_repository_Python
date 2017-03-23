import heapq

class PriorityQueue:
    
    def __init__(self, inlist=[]):
        self.priorityqueue=inlist
        heapq.heapify(self.priorityqueue)

    def makequeue(self,inlist):
        self.priorityqueue=inlist
        heapq.heapify(self.priorityqueue)
        
    def insert(self,item):
        heapq.heappush(self.priorityqueue,item)
    
    def peek(self):
        if len(self.priorityqueue) > 0:
            return self.priorityqueue[0]
        else:
            return None
            
    def deleteMin(self):
        if len(self.priorityqueue) > 0:
            return heapq.heappop(self.priorityqueue)
        else:
            return None
            
    def decreaseKey(self, item):
        #heapq does not have method to update keys
        #Here, searching the priority queue list to find the item (specifically second value in tuple item. needs to be unique), 
        #then updating the item and re-heapifying
        #VERY ineffecient way to implement this function. If this operation is used a lot, consider implementing your own heap 
        for i in range(len(self.priorityqueue)):
            if self.priorityqueue[i][1] == item[1]:
                self.priorityqueue[i]=item
                break
        heapq.heapify(self.priorityqueue)
           


A=PriorityQueue([(2, 'A'),(1, 'B'), (4, 'C'), (3, 'D')])
print A.peek()
print A.priorityqueue
A.insert((2,'E'))
print A.peek()
print A.priorityqueue
print A.deleteMin()
print A.peek()
print A.priorityqueue
print A.deleteMin()
print A.priorityqueue
A.decreaseKey((1,'D'))
print A.priorityqueue
print A.peek()

B=PriorityQueue([(2, 'A'),(1, 'B'), (4, 'C'), (3, 'D')])
B.makequeue([(2, 'A'),(1, 'B'), (4, 'C'), (3, 'D')])
print B.priorityqueue
print B.peek()
print B.deleteMin()
print B.deleteMin()
print B.deleteMin()
print B.deleteMin()
print B.deleteMin()