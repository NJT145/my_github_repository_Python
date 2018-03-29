####For Swampy applications####
#from swampy.TurtleWorld import *
#world = TurtleWorld()
#bob = Turtle()
## bob.set_delay(0.01) ##for a quicker answer

## fd(bob, dist) --> forward (for dist distance)(dist is an integer number)
## bk(bob, dist) --> backward  "   "     "        "   "  "     "      "
## lt(bob, angl) --> left      "  angl   angle   angl "  "     "      "
## rt(bob, dist) --> right     "  angl   angle   angl "  "     "      "
## pu(bob, dist) --> pen up    "  dist distance  dist "  "     "      "
## pd(bob, dist) --> pen down  "   "     "        "   "  "     "      "    (turtle leaves a trail when it moves)
## die(bob) --> turtle dies.
## set_color(bob, color) --> sets color of the turtle. (color ?? )
## set_pen_color(bob, color) --> sets color of the pen that turtle has. (color ?? )

##print bob.x
##print bob.y
##bob.x= 150
##bob.y= 150

#wait_for_user()

####Questions-Answers####

##Q1
def f1(small, big):
    if small%2==0:
        n=small
    else:
        n=small+1
        print small
    for i in range(n, big, 2):
        print i
#f1(4,10)
#f1(3,10)
def f2(small, big):
    if small%2==1:
        print small
    for i in range(small, big):
        if i%2==0:
            print i
#f2(4,10)
#f2(3,10)

##Q2
def repeat_str_1(str, n):
    m=n*str
    print m
#repeat_str_1("example",3)
def repeat_str_2(str, n):
    m=""
    for i in range(n):
        m+=str
    print m
#repeat_str_2("example",3)


##Q3
def f3(UpLimit, DownLimit):
    n=UpLimit-DownLimit
    for i in range(n):
        m="If I have "+str(UpLimit-i)+" homework an I do finish one of them, I will have "+str(UpLimit-1-i)+" to do."
        print m
######## str(n) makes pyton to take n as a string.
#f3(5,2)

##Q4

###1
def f4_1():
    print "+"
    print "++"
    print "+++"
    print "++++"
    print "+++++"
    print "++++++"
    print "+++++++"
    print "++++++"
    print "+++++"
    print "++++"
    print "+++"
    print "++"
    print "+"
#f4_1()

###2
"""
from swampy.TurtleWorld import *
world = TurtleWorld()
bob = Turtle()
bob.set_delay(0.01)

bob.x=-100

rt(bob, 60)
fd(bob, 50)
lt(bob, 120)
fd(bob, 50)
rt(bob, 120)
fd(bob, 50)
lt(bob, 120)
fd(bob, 50)
rt(bob, 60)
pu(bob)
fd(bob, 10)
pd(bob)
fd(bob, 30)
bk(bob, 30)
rt(bob, 90)
fd(bob, 25)
lt(bob, 90)
fd(bob, 30)
bk(bob, 30)
rt(bob, 90)
fd(bob, 25)
lt(bob, 90)
fd(bob, 30)
pu(bob)
fd(bob, 10)
lt(bob, 90)
fd(bob, 50)
rt(bob, 90)
pd(bob)
fd(bob, 30)
bk(bob, 30)
rt(bob, 90)
fd(bob, 25)
lt(bob, 90)
fd(bob, 30)
bk(bob, 30)
rt(bob, 90)
fd(bob, 25)
lt(bob, 90)
fd(bob, 30)
pu(bob)
fd(bob, 10)
lt(bob, 90)
fd(bob, 50)
rt(bob, 90)
pd(bob)
rt(bob, 90)
fd(bob, 25)
lt(bob, 150)
fd(bob, 30)
bk(bob, 30)
rt(bob, 120)
fd(bob, 30)
bk(bob, 30)
rt(bob, 30)
fd(bob, 25)

wait_for_user()

"""