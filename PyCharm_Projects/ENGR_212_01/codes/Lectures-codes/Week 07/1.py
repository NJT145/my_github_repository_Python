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
        self.initUI()

    def initUI(self):
        self.pack(fill=BOTH, expand=True)

        #title line
        var = StringVar()
        title = Label(self, textvariable=var, bg="red", fg="white", font='Arial 18')
        var.set("COURSE ANALYZER - SEHIR LIMITED EDITION")
        title.pack(fill=X)


        #file selection
        frame1=Frame(self)
        #
        frame11=Frame(frame1)
        Label(frame11,text="Update a file that contains course descriptions:  ", font='Arial 12').pack(side=LEFT)
        Button(frame11, text="Browse", font='Arial 10', command=self.onClickBrowse).pack(side=LEFT, padx=50, pady=5)
        frame11.pack()
        #
        frame12=Frame(frame1)
        Label(frame12,text="Selected File:  ", font='Arial 12').pack(side=LEFT)
        #
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
        self.pathVar.set(self.path)
        self.mylist.delete(0, END)
        self.courses()

    def courses(self):
        if self.path==None:
            pass
        else:

            lines = []
            for line in file(self.path):
                lines.append(line.strip())

            courseNames = []
            n = 1
            while n < len(lines) + 1:
                courseNames.append(lines[n - 1])
                n += 2

            courseInfo = []
            n = 1
            while n < len(lines) + 1:
                courseInfo.append(lines[n])
                n += 2

            courseCodes = []
            mylistList = []
            clusterText = {}

            for i in range(len(courseNames)):
                nameSplit = courseNames[i].split()
                code = nameSplit[0] + " " + nameSplit[1]
                courseCodes.append(code)
                codeGroup = nameSplit[0]
                if codeGroup not in mylistList:
                    mylistList.append(codeGroup)
                clusterText.setdefault(codeGroup, {})
                clusterText[codeGroup].setdefault(nameSplit[1], {})
                clusterText[codeGroup][nameSplit[1]] = courseInfo[i]

            mylistList.sort()

            for i in range(len(mylistList)):
                self.mylist.insert(END, mylistList[i])

            self.clusterWordNum = {}
            for codeGroup in clusterText:
                self.clusterWordNum.setdefault(codeGroup, {})
                for codeNum in clusterText[codeGroup]:
                    self.clusterWordNum[codeGroup].setdefault(codeNum, {})
                    splitted = re.split('\W+', clusterText[codeGroup][codeNum])
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
                self.value.append(value)
            self.wordsUsed = []
            for codeGroup in self.value:
                for codeNum in self.clusterWordNum[codeGroup]:
                    for word in self.clusterWordNum[codeGroup][codeNum].keys():
                        if word not in self.wordsUsed:
                            self.wordsUsed.append(word)
            self.wordsUsed.sort()
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

            self.blognames = []
            self.datas = []
            for codeGroup in self.codeWordCount:
                for codeNum in self.codeWordCount[codeGroup]:
                    blogname = codeGroup + " " + codeNum
                    self.blognames.append(blogname)
                    data = self.codeWordCount[codeGroup][codeNum]
                    self.datas.append(data)

    def onClickDiagram(self):
        if self.path == None:
            pass
        else:
            clust = clusters.hcluster(self.datas, distance=clusters.pearson)

            # height and width
            h = clusters.getheight(clust) * 20
            w = 1200
            depth = clusters.getdepth(clust)

            lenght=max(h,w)
            if lenght < 1000:
                lenght = 1000
            self.canvas.config(width=lenght, height=lenght, scrollregion=(0, 0, lenght, lenght))
            if self.canvasID != []:
                if type(self.canvasID)==list:
                    for i in self.canvasID:
                        self.canvas.delete(i)
                else:
                    self.canvas.delete(self.canvasID)
                self.canvasID = []

            # width is fixed, so scale distances accordingly
            scaling = float(w - 150) / depth

            self.ID=1
            self.canvasID.append(str(self.ID))
            self.ID=self.canvas.create_line(0, h/2, 10, h/2, fill="red")

            # Draw the first node
            self.canvasDrawNode(clust, 10, h/2, scaling, self.blognames)


    def canvasDrawNode(self, clust, x, y, scaling, labels):
        if clust.id < 0:
            h1 = clusters.getheight(clust.left) * 20
            h2 = clusters.getheight(clust.right) * 20
            top = y - (h1 + h2) / 2
            bottom = y + (h1 + h2) / 2
            # Line length
            ll = clust.distance * scaling
            # Vertical line from this cluster to children
            self.ID += 1
            self.canvasID.append(str(self.ID))
            self.ID=self.canvas.create_line(x, top + h1 / 2, x, bottom - h2 / 2, fill="red")

            # Horizontal line to left item
            self.ID += 1
            self.canvasID.append(str(self.ID))
            self.ID=self.canvas.create_line(x, top + h1 / 2, x + 30, top + h1 / 2, fill="red")

            # Horizontal line to right item
            self.ID += 1
            self.canvasID.append(str(self.ID))
            self.ID=self.canvas.create_line(x, bottom - h2 / 2, x + 30, bottom - h2 / 2, fill="red")

            # Call the function to draw the left and right nodes
            self.canvasDrawNode(clust.left, x + 30, top + h1 / 2, scaling, labels)
            self.canvasDrawNode(clust.right, x + 30, bottom - h2 / 2, scaling, labels)
        else:
            # If this is an endpoint, draw the item label
            self.ID += 1
            self.canvasID.append(str(self.ID))
            text=labels[clust.id]
            self.ID = self.canvas.create_text(x + len(text)*4, y + 3,  text=text)


    def onClickText(self):
        if self.path == None or self.value==None or self.value==[]:
            pass
        else:
            if self.canvasID != []:
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
            if self.canvasID!=[]:
                self.canvas.delete(self.canvasID)
            canvas_id = self.canvas.create_text(10, 10, anchor="nw")
            self.canvas.itemconfig(canvas_id, text=clusterAsText)
            self.canvasID=canvas_id

            print clusters.getheight(clust) * 20
            print float(1200 - 150) / clusters.getdepth(clust)
            print clusters.getdepth(clust)

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