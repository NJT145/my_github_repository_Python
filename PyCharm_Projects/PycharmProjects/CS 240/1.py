wine=open("wine.txt", "r+")
winet=[]
fortw={}
dryw={}
sweetw={}
red={}
rose={}
spark={}
total_sales={}
wine.readline()
for line in wine:
    x= line.split()
    winet.append(int(x[0]))
    fortw[int(x[0])]=(int(x[1]))
    dryw[int(x[0])]=(int(x[2]))
    sweetw[int(x[0])]=(int(x[3]))
    red[int(x[0])]=(int(x[4]))
    rose[int(x[0])]=(int(x[5]))
    spark[int(x[0])]=(int(x[6]))

for mounth in range(187):
    total_sales[mounth+1]=fortw[mounth+1]+dryw[mounth+1]+sweetw[mounth+1]+red[mounth+1]+rose[mounth+1]+spark[mounth+1]
print fortw
print dryw
print sweetw
print red
print rose
print spark
print total_sales
