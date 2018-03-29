def editDistance(X,Y):

    m= len(X)
    n= len(Y)
    
    E=[[0 for _ in range(0,n+1)] for _ in range(0,m+1)]
    
    for i in range(0,m+1):
        E[i][0]=i
        
    for j in range(0,n+1):
        E[0][j]=j
        
    for i in range(1,m+1):
        for j in range(1,n+1):
            E[i][j]=min([E[i-1][j]+1,E[i][j-1]+1,E[i-1][j-1]+int(X[i-1]!=Y[j-1]),] )
            
    return E[m][n]
    

print editDistance('EXPONENTIAL', 'POLYNOMIAL')

