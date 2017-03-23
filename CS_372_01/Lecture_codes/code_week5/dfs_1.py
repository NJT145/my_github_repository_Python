class Node:
    def __init__(self, label):
        self.label=label
        self.neighbors=[]
        self.visited=False
        
    def __str__(self):
        temp_str=str(self.label) + ": "
        for node in self.neighbors:
            temp_str+=node.label + " "
        return temp_str
    
    def addNeighbor(self, node):
        self.neighbors.append(node)

    def deleteNeighbor(self,node):
        try:
            self.neighbors.remove(node)
        except ValueError:
            print "Node %s : %s is Invalid Neighbor" % (self.label, node.label)

    def getNeighbors(self):
        return self.neighbors

    def setVisited(self):
        self.visited=True

    def clearVisited(self):
        self.visited=False

    def isVisited(self):
        return self.visited

    def getLabel(self):
        return self.label

class Graph:
    def __init__(self):
        self.graph=dict()
    
    def addNode(self, label):
        if label in self.graph:
            print 'Node %s exists!!!' % label
        else:
            self.graph[label]=Node(label)
            
    def addNeighbor(self,node,neighbor):
        if node not in self.graph:
            self.addNode(node)
        if neighbor not in self.graph:
             self.addNode(neighbor)           
        self.graph[node].addNeighbor(self.graph[neighbor]) 
        
    def deleteNeighbor(self,node,neighbor):
        if node not in self.graph:
            print 'Node %s does not exist!!!' % node
        else:
            self.graph[node].deleteNeighbor(self.graph[neighbor])
        
    def printGraph(self):
        for node in self.graph:
            print self.graph[node]

    def getNodeLabels(self):
        return self.graph.keys()

    def getNode(self, label):
        return self.graph[label]
    
    def clearVisited(self):
        for node in self.graph:
            self.graph[node].clearVisited()

    def explore(self, node):
        print node
        if not self.graph[node].isVisited() :
            self.graph[node].setVisited()
            for neighbor in self.graph[node].getNeighbors():
                if not neighbor.isVisited():
                    self.explore(neighbor.getLabel())

    def dfs(self):
        self.clearVisited()
        for node in self.getNodeLabels():
            if not self.graph[node].isVisited():
                self.explore(node)




graph1=Graph()
graph1.printGraph()
graph1.addNode('A')
graph1.addNode('B')
graph1.addNode('C')
graph1.addNode('D')
graph1.addNode('E')
graph1.addNeighbor('A', 'C')
graph1.addNeighbor('D', 'E')
graph1.addNeighbor('B', 'C')
graph1.addNeighbor('A', 'E')
graph1.addNeighbor('C', 'D')
graph1.printGraph()
graph1.deleteNeighbor('F', 'D')
graph1.printGraph()

graph1.explore('A')
for i in graph1.getNodeLabels():
    print i, graph1.getNode(i).isVisited()


graph1.dfs()
for i in graph1.getNodeLabels():
    print i, graph1.getNode(i).isVisited()

