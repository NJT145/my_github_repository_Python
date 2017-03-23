####### SOLUTION MANUAL######
###Q1
def ahmet():
    notebook=1.25
    pen=0.25
    total=notebook*2+pen*5
    remain=10-total
    kurus=remain*100
    number, kalan=divmod(kurus,75)
    print kalan
#ahmet()
###Q2
def square():
    print "+---+---+"
    print "|    |   |"
    print "|    |   |"
    print "|    |   |"
    print "+---+---+"
#square()
###Q4
def twice(a):
    print a
    print a
#twice("hello")

def full(name, surname):
    fullname=name+ " " +    surname
    twice(fullname)
#full("ali","cakmak")
###Q5
def square(a):
    result=4*a
    print "The peripheral length of sqaure is:"  + str(result)
#square(8)
###Q6
def distance(x1,x2,y1,y2):
    xd=x2-x1
    yd=y2-y1
    sq=xd**2 + yd**2
    sqrt=sq**0.5
    print  sqrt
#distance(3,7,4,7)
###Q7
def exact(s):
    hour, seconds=divmod(s,3600)
    minutes, se=divmod(seconds,60)
    print "Exact time is:" + str(hour)+ ":"+ str(minutes)+ ":" + str(se)
#exact(7264)

