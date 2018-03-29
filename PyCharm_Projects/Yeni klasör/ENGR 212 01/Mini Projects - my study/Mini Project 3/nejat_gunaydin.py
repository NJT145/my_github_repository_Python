"""
My references:
* for choosing a file whith my of Browse buttons, i used codes in :
        #http://tkinter.unpythonic.net/wiki/tkFileDialog
* for listbox with scrollbar, i used codes in :
        #http://www.java2s.com/Tutorial/Python/0360__Tkinker/ListBoxwithscrollbar.htm
* for RadioButton widget, i used codes in :
        #http://effbot.org/tkinterbook/radiobutton.htm
        #http://www.python-course.eu/tkinter_radiobuttons.php
*for canvas with scrollbar, i took a look to :
        #http://stackoverflow.com/questions/7727804/python-and-tkinter-using-scrollbars-on-a-canvas/7734187#7734187
* i needed to make a rewision about regular expression module re from :
        #https://docs.python.org/2/library/re.html
* for canvas methods, i used codes in :
        #http://stackoverflow.com/questions/14423959/python-tkinter-inserting-text-into-canvas-windows
* at CourseAnalyzer.onClickDiagram, i put a series of codes which is an adaptation of clusters.drawdendogram() to canvas
    modification. (Instead of creating a jpg image an drawing lines and inserting texts on it, i use my canvas widget
    and draw lines and insert text on it)
    **CourseAnalyzer.canvasDrawNode() is an adaptation of clusters.drawnode() to canvas implementation type, similarly.
* i used clusters module from LMS.
*the rest was mostly referenced from LMS files.
"""

#-*- coding: utf-8 -*-

from Tkinter import *
from tkFileDialog import *

import clusters


class CourseAnalyzer(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.value = None
        self.path = None
        self.canvasID=[]
        self.ID = None
        self.initUI()

    def initUI(self):
        self.pack(fill=BOTH, expand=True)

        #title line
        var = StringVar()
        title = Label(self, textvariable=var, bg="red", fg="white", font='Arial 18')
        var.set("COURSE ANALYZER - SEHIR LIMITED EDITION")
        title.pack(fill=X)


        #file selection frame
        frame1=Frame(self)

        frame11=Frame(frame1)
        Label(frame11,text="Update a file that contains course descriptions:  ", font='Arial 12').pack(side=LEFT)
        Button(frame11, text="Browse", font='Arial 10', command=self.onClickBrowse).pack(side=LEFT, padx=50, pady=5)
        frame11.pack()

        frame12=Frame(frame1)
        Label(frame12,text="Selected File:  ", font='Arial 12').pack(side=LEFT)

        ##this is the file path label. this label will change according to selected file.
        self.pathVar=StringVar()
        self.pathVar.set("  "*24+"Please select a file."+"  "*24)
        Label(frame12,textvariable=self.pathVar, font='Arial 8', borderwidth=2,relief=GROOVE).pack(side=LEFT)

        frame12.pack()
        frame1.pack(pady=10)

        #
        frame2 = Frame(self, borderwidth=2, relief=GROOVE)
        #settings
        frame2a=Frame(frame2)
        frame21=Frame(frame2a)
        Label(frame21,text="Similarity Measure: ").pack(side=RIGHT)
        frame21.pack(side=LEFT)

        #
        frame22 = Frame(frame2a)
        self.simMeasure = StringVar()
        self.simMeasure.set("Pearson")  # initialize our selected point
        Radiobutton(frame22, text="Pearson", padx=20, variable=self.simMeasure, value="Pearson").pack(anchor=W)
        Radiobutton(frame22, text="Tanimoto", padx=20, variable=self.simMeasure, value="Tanimoto").pack(anchor=W)
        frame22.pack(side=LEFT, padx=15)
        #
        frame23=Frame(frame2a)
        Label(frame23,text="Select Course Codes: ").pack(side=LEFT)
        listBoxWithScrollbar = Frame(frame23)
        scrollbar = Scrollbar(listBoxWithScrollbar)
        self.mylist = Listbox(listBoxWithScrollbar,height=5,width=30,selectmode=MULTIPLE,yscrollcommand=scrollbar.set)
        self.mylist.bind("<<ListboxSelect>>", self.OnClick)

        scrollbar.config(command=self.mylist.yview)
        self.mylist.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=LEFT, fill=Y)
        listBoxWithScrollbar.pack(side=LEFT)
        frame23.pack(side=RIGHT)

        frame2a.pack()

        #buttons
        frame2b=Frame(frame2)
        Button(frame2b, text="Draw Hierarchical Cluster Diagram", font='Arial 8',
               command=self.onClickDiagram).pack(side=LEFT, padx=10)
        Button(frame2b, text="Print Hierarchical Cluster as Text", font='Arial 8',
               command=self.onClickText).pack(side=LEFT, padx=10)
        Button(frame2b, text="Show Data Matrix", font='Arial 8',
               command=self.onClickMatrix).pack(side=LEFT, padx=10)
        frame2b.pack(fill=X, pady=10)

        #the canvas frame that will show our results.
        canvasFrame = Frame(frame2, width=300, height=300)
        self.canvas = Canvas(canvasFrame, bg='#FFFFFF', width=1000, height=1000, scrollregion=(0, 0, 1000, 1000))
        hbar = Scrollbar(canvasFrame, orient=HORIZONTAL)
        hbar.config(command=self.canvas.xview)
        hbar.pack(side=BOTTOM, fill=X)
        vbar = Scrollbar(canvasFrame, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.pack()
        canvasFrame.pack()

        frame2.pack()


    def onClickBrowse(self):
        browse = askopenfilename()
        self.path=browse
        self.pathVar.set(self.path) #let's modify the file path label according to our choise.
        self.mylist.delete(0, END)  #we need to reflesh self.mylist
        self.courses()

    #this one will fill self.mylist and create two cluster dictionaries which will be used later, according to our choise.
    def courses(self):
        if self.path==None:
            pass
        else:
            #we need to seperate each line in order to use.
            lines = []
            for line in file(self.path):
                lines.append(line.strip())

            #let's take our course names in a seperate list.
            courseNames = []
            n = 1
            while n < len(lines) + 1:
                courseNames.append(lines[n - 1])
                n += 2

            #let's take course descriptions in a seperate list, that the index of descriptions will be the index of matching course name.
            courseInfo = []
            n = 1
            while n < len(lines) + 1:
                courseInfo.append(lines[n])
                n += 2

            #we need to get course departments' codes ("CS", "MATH", and so on...) and put them on our mylistList.
            mylistList = []
            ##this one will take each [course departments' code][course number]=(text of description of the course)
                ## and will be used while we count the frequency of each word in course description.
            clusterText = {}
            for i in range(len(courseNames)):
                nameSplit = courseNames[i].split()
                codeGroup = nameSplit[0]
                if codeGroup not in mylistList:
                    mylistList.append(codeGroup)
                clusterText.setdefault(codeGroup, {})
                clusterText[codeGroup].setdefault(nameSplit[1], {})
                clusterText[codeGroup][nameSplit[1]] = courseInfo[i]
            # we need to sort the mylistList at insert it on self.mylist after that.
            mylistList.sort()
            for i in range(len(mylistList)):
                self.mylist.insert(END, mylistList[i])

            #this will count the frequency of each word in course description for each word in description for each course.
            self.clusterWordNum = {}
            for codeGroup in clusterText:
                self.clusterWordNum.setdefault(codeGroup, {})
                for codeNum in clusterText[codeGroup]:
                    self.clusterWordNum[codeGroup].setdefault(codeNum, {})
                    splitted = re.split('\W+', clusterText[codeGroup][codeNum]) #that will just take words and put "" for the others.
                    #we need to clear the "" ones because we only want words.
                    words = []
                    for word in splitted:
                        if word != "":
                            words.append(word)
                    for word in words:
                        if word not in self.clusterWordNum[codeGroup][codeNum].keys():
                            self.clusterWordNum[codeGroup][codeNum].setdefault(word, {})
                            self.clusterWordNum[codeGroup][codeNum][word] = 1
                        else:
                            self.clusterWordNum[codeGroup][codeNum][word] += 1

            #let's find common words on each couple of courses.
            self.clusterCommonWords = {}
            for codeGroup in self.clusterWordNum:
                self.clusterCommonWords.setdefault(codeGroup, {})
                for codeNum1 in self.clusterWordNum[codeGroup]:
                    self.clusterCommonWords[codeGroup].setdefault(codeNum1, {})
                    for codeNum2 in self.clusterWordNum[codeGroup]:
                        if codeNum1 != codeNum2:
                            self.clusterCommonWords[codeGroup][codeNum1].setdefault(codeNum2, [])
                            for word in self.clusterWordNum[codeGroup][codeNum2]:
                                if word in self.clusterWordNum[codeGroup][codeNum1]:
                                    self.clusterCommonWords[codeGroup][codeNum1][codeNum2].append(word)

    def OnClick(self, event):
        if self.path == None:
            pass
        else:
            widget = event.widget
            selection = widget.curselection()
            self.value=[]
            for i in selection:
                value = widget.get(i)
                self.value.append(value)  #insert our selection into our selection list self.value
            # self.wordsUsed is list of commonly used words in all course departments that we choosed on self.mylist.
            self.wordsUsed = []
            for codeGroup in self.value:
                for codeNum in self.clusterWordNum[codeGroup]:
                    for word in self.clusterWordNum[codeGroup][codeNum].keys():
                        if word not in self.wordsUsed:
                            self.wordsUsed.append(word)
            self.wordsUsed.sort()
            # self.codeWordCount is a dictionary that stores frequency of each word in self.wordsUsed from each description text.
                # ( [courseCode][courseNumber]=(list of frequencies of words) )
            self.codeWordCount = {}
            for codeGroup in self.value:
                self.codeWordCount.setdefault(codeGroup, {})
                for codeNum in self.clusterWordNum[codeGroup]:
                    self.codeWordCount[codeGroup].setdefault(codeNum,[])
                    for wordNum in range(len(self.wordsUsed)):
                        if self.wordsUsed[wordNum] not in self.clusterWordNum[codeGroup][codeNum].keys():
                            self.codeWordCount[codeGroup][codeNum].append(0)
                        else:
                            self.codeWordCount[codeGroup][codeNum].append(self.clusterWordNum[codeGroup][codeNum][self.wordsUsed[wordNum]])

            # self.blognames is list of courseCode+" "+courseNumber .
            # self.datas is list of frequency lists for words used at all.
            self.blognames = []
            self.datas = []
            for codeGroup in self.codeWordCount:
                for codeNum in self.codeWordCount[codeGroup]:
                    blogname = codeGroup + " " + codeNum
                    self.blognames.append(blogname)
                    data = self.codeWordCount[codeGroup][codeNum]
                    self.datas.append(data)

    # this method will draw Hierarchical Cluster Diagram on canvas.
    def onClickDiagram(self):
        if self.path == None:
            pass
        else:
            if self.simMeasure.get=="Pearson":
                clust = clusters.hcluster(self.datas, distance=clusters.pearson)
            else:
                clust = clusters.hcluster(self.datas, distance=clusters.tanimoto)

            #########this part is an adaptation of clusters.drawdendogram() to canvas.#########

            # height and width
            h = clusters.getheight(clust) * 20
            w = 1200
            depth = clusters.getdepth(clust)

            lenght=max(h,w)
            if lenght < 1000:
                lenght = 1000
            self.canvas.config(width=lenght, height=lenght, scrollregion=(0, 0, lenght, lenght))
            if self.canvasID != []:
                if self.ID_1!=None:
                    self.canvas.delete(self.ID_1)
                if type(self.canvasID)==list:
                    for i in range(len(self.canvasID)):
                        self.canvas.delete(self.canvasID[i])
                else:
                    self.canvas.delete(self.canvasID)
                self.canvasID = []

            # width is fixed, so scale distances accordingly
            scaling = float(w - 150) / depth

            self.ID_1=self.canvas.create_line(0, h/2, 10, h/2, fill="red")

            # Draw the first node
            self.canvasDrawNode(clust, 10, h/2, scaling, self.blognames)

            ##################

    #this method is an adaptation of clusters.drawnode() to canvas.
    def canvasDrawNode(self, clust, x, y, scaling, labels):
        if clust.id < 0:
            h1 = clusters.getheight(clust.left) * 20
            h2 = clusters.getheight(clust.right) * 20
            top = y - (h1 + h2) / 2
            bottom = y + (h1 + h2) / 2
            # Line length
            ll = clust.distance * scaling
            # Vertical line from this cluster to children
            self.ID=self.canvas.create_line(x, top + h1 / 2, x, bottom - h2 / 2, fill="red")
            self.canvasID.append((self.ID))

            # Horizontal line to left item
            self.ID=self.canvas.create_line(x, top + h1 / 2, x + 30, top + h1 / 2, fill="red")
            self.canvasID.append((self.ID))

            # Horizontal line to right item
            self.ID=self.canvas.create_line(x, bottom - h2 / 2, x + 30, bottom - h2 / 2, fill="red")
            self.canvasID.append((self.ID))

            # Call the function to draw the left and right nodes
            self.canvasDrawNode(clust.left, x + 30, top + h1 / 2, scaling, labels)
            self.canvasDrawNode(clust.right, x + 30, bottom - h2 / 2, scaling, labels)
        else:
            # If this is an endpoint, draw the item label
            text=labels[clust.id]
            self.ID = self.canvas.create_text(x + len(text)*4, y + 3,  text=text)
            self.canvasID.append((self.ID))

    #this method will show a text format of Hierarchical Cluster Diagram on canvas.
    def onClickText(self):
        if self.path == None or self.value==None or self.value==[]:
            pass
        else:
            if self.canvasID != []:
                if self.ID_1 != None:
                    self.canvas.delete(self.ID_1)
                if type(self.canvasID) == list:
                    for i in self.canvasID:
                        self.canvas.delete(i)
                else:
                    self.canvas.delete(self.canvasID)
                self.canvasID = []

            measureMethod=None
            if self.simMeasure.get()=="Pearson":
                measureMethod= clusters.pearson
            elif self.simMeasure.get()=="Tanimoto":
                measureMethod= clusters.tanimoto
            clust = clusters.hcluster(self.datas, distance=measureMethod)
            clusterAsText= clusters.clust2str(clust, labels=self.blognames, n=0)

            lenght=0
            for line in clusterAsText:
                lenght+=1
            if  lenght < 1000 :
                lenght=1000

            self.canvas.config(width=lenght,height=lenght, scrollregion=(0, 0, lenght, lenght))
            canvas_id = self.canvas.create_text(10, 10, anchor="nw")
            self.canvas.itemconfig(canvas_id, text=clusterAsText)
            self.canvasID=canvas_id

    #this method will show a table-likely matrix of frequency of words for each courses.
    def onClickMatrix(self):
        if self.path == None:
            pass
        else:
            if self.value==[]:
                text=" "
            else:

                text="COURSES\t"
                firstLine = "\t".join(self.wordsUsed)
                text=text+firstLine+"\n"

                length=len(text)*10
                self.canvas.config(width=length, height=length, scrollregion=(0, 0, length, length))

                for i in range(len(self.blognames)):
                    datas=[]
                    for n in range(len(self.datas[i])):
                        datas.append(str(self.datas[i][n]))
                    text=text+self.blognames[i]+"\t\t"+"\t".join(datas)+"\n"

            if self.canvasID != []:
                if type(self.canvasID) == list:
                    for i in self.canvasID:
                        self.canvas.delete(i)
                else:
                    self.canvas.delete(self.canvasID)
                self.canvasID = []
            canvas_id = self.canvas.create_text(10, 10, anchor="nw")
            self.canvas.itemconfig(canvas_id, text=text)
            self.canvasID = canvas_id



def main():
    root = Tk()
    root.wm_title("Course Analyzer - Sehir Limited Edition")
    root.geometry("850x600+250+35")
    app = CourseAnalyzer(root)
    root.mainloop()

if __name__ == '__main__':
    main()