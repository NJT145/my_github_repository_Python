def knapsackWithRepetition(W, items):
    
    K=[0 for _ in range(W+1)]
    
    for w in range(1,W+1):
        current_max=0
        for (weight,value) in items:
            if weight <= w : 
                current_max=max(current_max,K[w-weight]+value)
        K[w]=current_max
    
    return K[W]
    
def knapsackWithoutRepetition(W, items):
    
    n=len(items)
    
    K=[[0 for _ in range(W+1)] for _ in range(n+1)]
    
    for j in range(n+1):
        K[j][0]= 0
  
    for w in range(W+1):
        K[0][w]= 0             

    for j in range(1,n+1):
         (item_weight,item_value)=items[j-1]
         for w in range(1,W+1):
             if item_weight <= w:
                 K[j][w]=max(K[j-1][w-item_weight]+item_value, K[j-1][w])
             else:
                 K[j][w]= K[j-1][w]
                 
    return K[n][W]
                     
print knapsackWithRepetition(10, [(6,30),(3,14),(4,16),(2,9)])
print knapsackWithoutRepetition(10, [(6,30),(3,14),(4,16),(2,9)])