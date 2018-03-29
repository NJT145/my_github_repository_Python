
class Graph:
    def __init__(self):
        self.graph=dict()
    
    def addNode(self, label):
        if label in self.graph:
            print 'Node %s exists!!!' % label
        else:
            self.graph[label]=[]
            
    def addNeighbor(self,node,neighbor):
        if node not in self.graph:
            self.addNode(node)
        if neighbor not in self.graph:
             self.addNode(neighbor)           
        self.graph[node].append(neighbor) 

    def deleteNeighbor(self,node,neighbor):
        if node not in self.graph:
            print 'Node %s does not exist!!!' % node
        else: 
            try:
                self.graph[node].remove(neighbor)
            except ValueError:
                print "Node %s : %s is Invalid Neighbor" % (node, neighbor)

    def printGraph(self):
        for node in self.graph:
            print node, '=', self.graph[node]


graph1= Graph()
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
graph1.deleteNeighbor('A', 'D')
graph1.printGraph()
