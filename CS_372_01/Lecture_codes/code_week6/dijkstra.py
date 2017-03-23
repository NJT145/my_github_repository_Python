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
            
    def isEmpty(self):
        if len(self.priorityqueue) == 0:
            return True
        else:
            return False
            
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
           
class Node:
    def __init__(self, label):
        self.label=label
        self.edges=[]
        self.dist=float("inf")
        self.visited=False
        
    def __str__(self):
        temp_str=str(self.label) + ": "
        for edge in self.edges:
            temp_str+="("+ edge.getEnd().label + "," + str(edge.getWeigth()) + ") "
        return temp_str
    
    def addEdge(self, edge):
        self.edges.append(edge)
        
    def getEdges(self):
        return self.edges

    def setVisited(self):
        self.visited=True

    def clearVisited(self):
        self.visited=False

    def isVisited(self):
        return self.visited

    def getLabel(self):
        return self.label

    def clearDist(self):
        self.dist=float("inf")

    def setDist(self, dist):
        self.dist=dist

    def getDist(self):
        return self.dist

class Edge:
    def __init__(self, start,end,weight):
        self.weigth=weight
        self.start=start
        self.end=end
        
    def __str__(self):
        temp_str=self.start.getLabel() + "-->" + self.end.getLabel() + ":" + str(weigth)
        return temp_str
        
    def getWeigth(self):
        return self.weigth  

    def getStart(self):
        return self.start  
                                    
    def getEnd(self):
        return self.end  
                            
class Graph:
    def __init__(self):
        self.graph=dict()
        self.clock=None
    
    def addNode(self, label):
        if label in self.graph:
            print 'Node %s exists!!!' % label
        else:
            self.graph[label]=Node(label)
            
    def addEdge(self,start,end,weigth):
        if start not in self.graph:
            self.addNode(start)
        if end not in self.graph:
             self.addNode(end)           
        self.graph[start].addEdge(Edge(self.graph[start],self.graph[end],weigth)) 
                
    def printGraph(self):
        for node in self.graph:
            print self.getNode(node)
            
    def printDistances(self):
        for node in self.graph:
            print node, self.getNode(node).getDist()

    def getNodeLabels(self):
        return self.graph.keys()

    def getNode(self, label):
        return self.graph[label]
    
    def clearVisited(self):
        for node in self.graph:
            self.graph[node].clearVisited()

    def clearDist(self):
        for node in self.graph:
            self.graph[node].clearDist()

    def dijkstra(self, node):
        V=[]
        
        self.clearDist()
        startingNode=self.getNode(node)
        startingNode.setDist(0)
         
        #create a list of (dist,node_label) pairs
        for i in  self.graph:
            V.append((self.graph[i].getDist(),i))
        
        #create and initialize priority queue with all nodes
        H= PriorityQueue()
        H.makequeue(V) 
    
        
        while H.isEmpty() is not True:
            (distu,u)=H.deleteMin()
            for edge in self.getNode(u).getEdges():
                if edge.getEnd().getDist() > distu + edge.getWeigth():
                    edge.getEnd().setDist(distu + edge.getWeigth())
                    H.decreaseKey((edge.getEnd().getDist(),edge.getEnd().getLabel()))

               

graph1=Graph()
graph1.printGraph()
graph1.addNode('A')
graph1.addNode('B')
graph1.addNode('C')
graph1.addNode('D')
graph1.addNode('E')
graph1.addEdge('A', 'B', 4)
graph1.addEdge('A', 'C', 2)
graph1.addEdge('B', 'C', 3)
graph1.addEdge('B', 'D', 2)
graph1.addEdge('B', 'E', 3)
graph1.addEdge('C', 'B', 1)
graph1.addEdge('C', 'D', 4)
graph1.addEdge('C', 'E', 5)
graph1.addEdge('E', 'D', 1)
graph1.printGraph()
graph1.dijkstra('A')
graph1.printDistances()
