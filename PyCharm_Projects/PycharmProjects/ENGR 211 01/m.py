def count(name):
    d={}
    for k in name:
        if k in d:
            d[k]+=1
        else:
            d[k]=1
    print d
    for k in d:
        print str(str(k)+"="+str(d[k]))
#count("banana")

def func(n, word):
    for i in range(n):
        print word,
#func(5, "example")

# [print "a","b"]=[print "a b"] and [print "a", 1]=[print "a 1"]

def find(str,c):
    notfound = True
    for i in range(len(str)):
        if str[i]== c:
            notfound = False
            print i
    if notfound:
        print -1
#find("abc","c")
#find("abc","e")

def gcd_1(a,b):     # "greatest common divisor" version 1
    if b == 0:
        return a
    if b > a:
        return gcd_1(b,a)
    r = a%b
    if r == 0:
        return b
    return gcd_1(r,b)
#print gcd_1(20,16)

def gcd_2(a,b):     # "greatest common divisor" version 2
    while b:
        a, b = b, a%b
    return a
#print gcd_2(20,16)

def factorial (n):
    if not isinstance(n, int):
        print 'Factorial is only defined for integers.'
        return None
    elif n < 0:
        print 'Factorial is not defined for negative integers.'
        return None
    elif n == 0:
        return 1
    else:
        return n * factorial(n-1)

#######
# divmod(a,b)=((a//b),(a%b))  ## (a//b)=int(a/b)
#######
#print "a\n"*3+"b"
#print "c"
#######
# raw_input()=str(input())
#######
# for a list named list, for integer n, list[-n]=list[(len(list)-n)] , list[-n:]=list[(len(list)-n):] ,
#                                       list[:-n]=list[:(len(list)-n)]
#######
# r'\n' is a two-character string containing "\" and "n" , while '\n' is a one-character string containing a new line.
#######
# take a look to "regular expressions" and "raw string"
#######

def f(liste):
    sum1=0
    for i in liste:
        length=len(i)
        sum1 =sum1 + length
    average=sum1/float(len(liste))
    return average
#print f(["words","araba","car"])

def f1(s):
    empty=""
    i=0
    while i <len(s)-1:
        a,b=s[i],s[i+1]
        nw_s=int(a)*b
        empty = empty+nw_s
        i +=2
    return empty
#print f1("2a3b1c")

def f2(s):
    for i in s:
        if i.isupper():
            print i
#f2("AraBa")

def f3(s):
    d={"k":"a","l":"b","m":"c","n":"d"}
    empty= ""

    for i in s:
        val=d[i]
        empty =empty+val
    return empty
#print f3("kml")

def f4(d):
    val=d.values()
    d1={}
    for i in val:
        for j in i:
            if j not in d1:
                d1[j]=1
            else:
                d1[j] +=1
    items=d1.items()
    liste=[]
    for i,j in items:
        tp=tuple((j,i))
        liste.append(tp)
    liste.sort(reverse=True)
    return liste[0][1]
dicti={"b1":["r1","r2","r5"],"b2":["r2","r4"],"b3":["r2"]}
#print f4(dicti)

def f5(t):
    maximum=0
    for i,j in t:
        if abs(i-j) >maximum:
            maximum=abs(i-j)
    return maximum
tup=[(1,5),(8,13),(2,4)]
#print f5(tup)

class phone:
    pass
phone1=phone()
phone1.brand="x"
phone1.memory=64
photo=24
number=phone1.memory*1024/photo
#print number

