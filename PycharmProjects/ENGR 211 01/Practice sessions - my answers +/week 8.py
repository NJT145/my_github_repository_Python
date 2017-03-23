##Q1
def func1():
    print "DooWaa"
    for i in range(3):
        print "Diddy"
        if i==1:
            print "Dum"
    print "Doo"
#func1()

##Q2

###a
def f1(n):
    m=0
    for i in range(n+1):
        m+=i
    print m
#f1(5)

###b

def sumofsequence1(sequence):
    i=0
    n=0
    while n<(len(sequence)):
        i+=sequence[n]
        n+=1
    print i
#sumofsequence1([1,2,3,4,5])
#sumofsequence1((1,2,3,4,5))

def sumofsequence2(sequence):
    print sum(sequence)
#sumofsequence2([1,2,3,4,5])
#sumofsequence2((1,2,3,4,5))

###c
"""
i=1
while i<10:
    print "i = ", i
    i+=1
"""

###d
"""
i=20
for n in range(i):
    print "i = ", (i-n)
"""

##Q3
marks = open('marks.txt')
def examscorelessthan50():
    for line in marks:
        x = line.split()
        if int(x[2])<50:
            print line.strip()
#examscorelessthan50()

##Q4
def convert(str):
    list = str.split('_')
    empty = ''
    new_list = []
    new_list.append(list[0])
    n = 1
    while n<len(list):
        new_list.append(list[n].capitalize())
        n+=1
    converted = empty.join(new_list)
    print converted
#convert('is_prime')
#convert('_is_prime_')

##Q5
def read_and_print():
    empty = ""
    list = []
    n = 0
    while True:
        inputs = raw_input()
        if inputs!=" ":
            list.append(inputs)
            list.append("\n")
        else:
            list.pop(len(list)-1)
            print empty.join(list)
            break
#read_and_print()

##Q6