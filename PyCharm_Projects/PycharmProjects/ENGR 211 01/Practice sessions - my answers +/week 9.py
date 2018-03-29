####Question:
##Write a function which takes a string and return the count of the each letter as below.
####Answer:
def is_count(name):
    d={}
    for k in name:
        if k in d:
            d[k]+=1
        else:
            d[k]=1
    #print d
    for k in d:
        print (str(k)+"="+str(d[k]))
#is_count("banana")

####Question:
##Write a Python program that reads in lines of input from the user until you enter same input more than three times.
## Note: use dictionary datastructure to keep the previous inputs.
####Answer:
