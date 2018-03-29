
x=file("C:/Users/nejatgunaydin/Desktop/MyProjects/ENGR_212_01/MiniProjects_myStudy/Mini_Project_3/courses_cs.txt")
lines=[]
for line in x:
    lines.append(line.strip())
print lines[0]
print lines[len(lines)-2]
print lines[len(lines)-1]

courseNames=[]
n=1
while n<len(lines)+1:
    courseNames.append(lines[n-1])
    n+=2

courseInfo=[]
n=1
while n<len(lines)+1:
    courseInfo.append(lines[n])
    n+=2

courseCodes=[]
for name in courseNames:
    nameSplit=name.split()
    code=nameSplit[0]+" "+nameSplit[1]
    courseCodes.append(code)

mylistList=[]
for code in courseNames:
    codeSplit=code.split()
    list=codeSplit[0]
    if list not in mylistList:
        mylistList.append(list)
mylistList.sort()
print mylistList

