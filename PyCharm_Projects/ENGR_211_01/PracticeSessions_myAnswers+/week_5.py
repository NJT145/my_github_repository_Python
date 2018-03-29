##Q1
def countdown(n):
    while n>0:
        print n
        n=n-1
#countdown(5)

##Q2
def price(n):
    if n<3.0:
        print "If you use "+str(n)+"GB , you pay 20TL."
    elif n>3.0 and n<6.0:
        m=(n-3.0)*8
        print "If you use "+str(n)+"GB , you pay "+str(20+m)+"TL."
    else:
        s=(n-6.0)*12
        t=(3.0*8)
        print "If you use "+str(n)+"GB , you pay "+str(20+t+s)+"TL."
#price(2.4)
#price(1.0)
#price(3.2)
#price(6.5)

##Q3
def f(n):
    if n==1:
        return 3
    else:
        return f(n-1)+3
#print f(3)

##Q4

def gcd_1(a,b):
    if b == 0:
        return a
    if b > a:
        return gcd_1(b,a)
    r = a%b
    if r == 0:
        return b
    return gcd_1(r,b)
#print gcd_1(20,16)

def gcd_2(a,b):
    while b:
        a, b = b, a%b
    return a
#print gcd_2(20,16)

##Q5
def connect():
    username = raw_input("username: ")
    password = raw_input("password: ")
    if username == "Jack" and password == "12345":
        print "welcome to the system!"
    else:
        print "username or password is not correct!"
        connect()
#connect()

##Q6
###a

def fibonacci1(n):
    a, b = 0, 1
    old_a = None
    for i in range(n-1):
        old_a = a
        a = b
        b = old_a+b
    return a
#print fibonacci1(5)

###b
def fibonacci2(n):
    a, b = 0, 1
    old_a=None
    step = 1
    while step < n:
        old_a = a
        a = b
        b = old_a+b
        step += 1
    return a
#print fibonacci2(5)

###c
def fibonacci3(n):
    if n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        return fibonacci3(n-1) + fibonacci3(n-2)
#print fibonacci3(5)

##Q7

######## import random
######## random.random() ---> generates a float number between [0.0,1.0)
######## random.randit(lower,upper)  --->  generates an integer number between [lower,upper]
######## random.choice(A) ---> random element from A (A is a variable which can be
########                                                a number(int or float), tuple, string or a list)

def guess():
    import random
    number_to_be_guessed = random.randint(0,100)
    #print number_to_be_guessed
    while True:
        guess = int(raw_input("please make a guess (between 0-100): "))
        if guess == number_to_be_guessed:
            print "Congratulation, you made it!"
            break
        else:
            if guess < number_to_be_guessed:
                print "try a bigger one"
            else:
                print "try a smaller one"
#guess()

def guess2():
    import random
    number_to_be_guessed = random.randint(0,100)
    #print number_to_be_guessed
    while True:
        guess = (raw_input("please make a guess (between 0-100): "))
        if int(guess) == number_to_be_guessed:
            print "Congratulation, you made it!"
            break
        else:
            if int(guess) < number_to_be_guessed:
                print "try a bigger one"
            else:
                print "try a smaller one"
#guess2()
