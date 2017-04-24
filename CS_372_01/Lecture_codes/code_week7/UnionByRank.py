class SetNode:
    def __init__(self, label):
        self.label=label
        self.parent=self
        self.rank=0
        
    def __str__(self):
        temp_str=str(self.label) + ": rank= " + str(self.rank) + " parent=" + str(self.parent.label)
        return temp_str
    
    def setRank(self,rank):
        self.rank=rank

    def setParent(self,parent):
        self.parent=parent

    def getLabel(self):
        return self.label

    def getRank(self):
        return self.rank
 
    def getParent(self):
        return self.parent
        
class Sets:
    def __init__(self):
        self.items=dict()
            
    def getNode(self, item):
        return self.items[item]
    
    def printItems(self):
        for item in self.items:
            print self.getNode(item)
            
    def printSets(self):
        temp_sets=dict()
        for item in self.items:
            root=self.find(item).getLabel()
            if root in temp_sets:
                temp_sets[root].append(item)
            else:
                temp_sets[root]=[item]
        for key in temp_sets:
            print "Set=", temp_sets[key]
            
    def makeset(self, x):
        if x in self.items:
            print 'Item %s exists!!!' % x
        else:
            self.items[x]=SetNode(x)      
            
    def find(self, x):
        current_node=self.getNode(x)
        while current_node is not current_node.getParent():
            current_node= current_node.getParent()
        return current_node

    def union(self, x, y):
        r_x=self.find(x)
        r_y=self.find(y)
        if r_x is r_y:
            return
        if r_x.getRank() > r_y.getRank():
            r_y.setParent(r_x)
        else:
            r_x.setParent(r_y)
            if r_x.getRank() == r_y.getRank():
                r_y.setRank(r_y.getRank()+1)
            
     

sets=Sets()
sets.makeset('A')
sets.makeset('B')
sets.makeset('C')
sets.makeset('D')
sets.makeset('E')
sets.printItems()
sets.printSets()
print
sets.union('A','E')
sets.printItems()
sets.printSets()
print
sets.union('E','D')
sets.printItems()
sets.printSets()
print
sets.union('C','B')
sets.printItems()
sets.printSets()
print
sets.union('D','B')
sets.printItems() 
sets.printSets()   
print