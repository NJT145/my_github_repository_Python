####Question:
##Write a function that takes a number as an input and checks whether this number is divisible by 8 or not.
##If it is divisible by 8, it should prints:"The number is divisible by 8";If not:"The number is not divisible by 8"
####Answer:
def f8(n):
    if n%8:
        print "The number is divisible by 8"
    else:
        print "The number is not divisible by 8"

####Question:
##Write a countdown() function that takes a number as an input and print all numbers from this number to the 0.
##... (Hint: use for loop)
####Answer:
def countdown(n):
    for i in range(n):
        m=n-i
        print m
#countdown(6)

####Question:
##Write a function that takes two integers and prints the sum of all odd integers and the sum of even integers
## between them (separately). ...
##Note that the boundaries are not taken in the summation.
####Answer:

def sum_oddANDeven(x,m):
    n=0
    s=0
    for i in range(x+1,m):
        if i%2==1:
            n+=i
        else:
            s+=i
    print "Sum of Odds= "+str(n)
    print "Sum of Evens= "+str(s)
#sum_oddANDeven(1,7)

def sumoddeven(start,end):
    sumodd = 0
    sumeven = 0
    for n in range(start+1,end):
       if n%2 == 1:
           sumodd +=n
       else:
           sumeven += n
    print 'Sum of Odds=',sumodd
    print 'Sum of Evens=',sumeven
#sumoddeven(1,7)