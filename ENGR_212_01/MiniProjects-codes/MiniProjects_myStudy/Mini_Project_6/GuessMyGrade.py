"""
My references:
* for choosing a file whith my of Browse buttons, i used codes in :
        #http://tkinter.unpythonic.net/wiki/tkFileDialog
* in order to create my message boxes, i used this one :
        #http://www.tutorialspoint.com/python/tk_messagebox.htm
* in order to get input from textbox, i used codes in :
        #http://stackoverflow.com/questions/14824163/how-to-get-the-input-from-the-tkinter-text-box-widget
* in order to add color to lines of listbox, i used codes in :
        #http://stackoverflow.com/questions/5348454/is-it-possible-to-colour-a-specific-item-in-a-listbox-widget
* for learning how to use xlrd module, i took a look at:
        #https://secure.simplistix.co.uk/svn/xlrd/trunk/xlrd/doc/xlrd.html?p=4966
        #http://www.simplistix.co.uk/presentations/python-excel.pdf
*the rest was mostly referenced from LMS files and from lessons.
"""

import ttk
import tkMessageBox
from Tkinter import *
from tkFileDialog import *

import time
import pickle
import shelve
from xlrd import *


from bs4 import BeautifulSoup
from selenium import webdriver
from urllib2 import *
from urlparse import *

import docclass

combobox_select=None

class CurriculumViewer(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.value_of_combo = None
        self.frame4 = None
        self.CurriculumProblem=True
        self.initUI()

    def initUI(self):
        self.pack(fill=BOTH, expand=True)

        #title line
        var = StringVar()
        title = Label(self, textvariable=var, bg="black", fg="white", font='Helvetica 20 bold')
        var.set("Guess My Grade! v1.0\n(Designed for SEHIR webpages at year 2016")
        title.pack(fill=X)

        # user will upload curriculum by using Browse button at there
        browseCurriculumFrame=Frame(self)
        Label(browseCurriculumFrame, text="Please upload your curriculum file with the grades:"+(" "*50),
              fg="blue", font='Helvetica 12 bold').pack(side=LEFT)
        Button(browseCurriculumFrame, text=(" "*15)+"Browse"+(" "*15), relief=RAISED, font='Helvetica 15 bold',
               fg="white", bg="brown",command=self.onClickBrowse).pack(side=LEFT, padx=10)
        browseCurriculumFrame.pack(pady=15)

        # "| |" separator
        Label(self, text=("| |" * 999), font='Arial 1').pack()

        # user will enter URLs for course descriptions, at here
        enterURLframe=Frame(self)
        Label(enterURLframe, text="Enter URLs for course descriptions"+(" "*170),  font='Helvetica 12 bold').pack()

        TextBoxWithScrollbar = Frame(enterURLframe)
        scrollbar1 = Scrollbar(TextBoxWithScrollbar)
        self.TextBox = Text(TextBoxWithScrollbar, height=6, width=118,
                            yscrollcommand=scrollbar1.set)
        scrollbar1.config(command=self.TextBox.yview)
        self.TextBox.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar1.pack(side=LEFT, fill=Y)
        url1="http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=12"
        url2="http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=13"
        url3="http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=14"
        url4="http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=32"
        text=url1+"\n"+url2+"\n"+url3+"\n"+url4+"\n"
        self.TextBox.insert(END, text)
        TextBoxWithScrollbar.pack()

        Label(enterURLframe, text="Key:"+(" "*152), font='Helvetica 15 bold').pack()

        keysAndPREDICTGRADESbuttonFrame=Frame(enterURLframe)

        Label(keysAndPREDICTGRADESbuttonFrame, text=(" " * 5) + "A" + (" " * 5), bg="green", fg="white",
              font='Verdana 14 italic').pack(side=LEFT,padx=10)
        Label(keysAndPREDICTGRADESbuttonFrame, text=(" " * 5) + "B" + (" " * 5), bg="gray", fg="green",
              font='Verdana 14 italic').pack(side=LEFT, padx=10)
        Label(keysAndPREDICTGRADESbuttonFrame, text=(" " * 5) + "C" + (" " * 5), bg="yellow", fg="white",
              font='Verdana 14 italic').pack(side=LEFT, padx=10)
        Label(keysAndPREDICTGRADESbuttonFrame, text=(" " * 5) + "D" + (" " * 5), bg="red", fg="white",
              font='Verdana 14 italic').pack(side=LEFT, padx=10)
        Label(keysAndPREDICTGRADESbuttonFrame, text=(" " * 5) + "F" + (" " * 5), bg="black", fg="white",
              font='Verdana 14 italic').pack(side=LEFT, padx=10)
        Label(keysAndPREDICTGRADESbuttonFrame, text=" "*15, font='Verdana 14 italic').pack(side=LEFT, padx=10)

        Button(keysAndPREDICTGRADESbuttonFrame, text=(" " * 10) + "Predict Grades" + (" " * 10),
               relief=RAISED, font='Helvetica 15 bold', fg="white", bg="brown",
               command=self.onClickPredictGrades).pack(side=LEFT, padx=10)

        keysAndPREDICTGRADESbuttonFrame.pack()
        enterURLframe.pack(pady=10)

        # "| |" separator
        Label(self, text=("| |" * 999), font='Arial 1').pack()

        resultsPredictGrades=Frame(self)

        Label(resultsPredictGrades, text="Predicted Grades"+(" "*132),  font='Helvetica 15 bold').pack()

        listBoxWithScrollbar = Frame(resultsPredictGrades)
        scrollbar = Scrollbar(listBoxWithScrollbar)
        self.mylist = Listbox(listBoxWithScrollbar, height=12, width=158, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.mylist.yview)
        self.mylist.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=LEFT, fill=Y)
        listBoxWithScrollbar.pack(pady=10)

        resultsPredictGrades.pack(pady=10)

    def onClickBrowse(self):
        browse = askopenfilename()

        self.CurriculumProblem=False
        try:
            # let's get our curriculum's infos
            wb = open_workbook(browse)
            semester_no = 0
            semester_row_no__dic = {}
            semester_col_no__dic = {}
            self.code_by_semester = {}
            self.title_by_semester = {}
            self.credit_by_semester = {}
            self.grade_by_semester = {}
            self.code_list_by_grade_by_semester={}
            for s in wb.sheets():
                if "curriculum" in s.name:
                    for row in range(s.nrows):
                        for col in range(s.ncols):
                            if type(s.cell(row, col).value) == float:
                                pass
                            elif type(s.cell(row, col).value) == int:
                                pass
                            elif "Semester I" in s.cell(row, col).value:
                                semester_no += 1
                                semester_row_no__dic[semester_no] = row
                                semester_col_no__dic[semester_no] = col
                            elif "Semester V" in s.cell(row, col).value:
                                semester_no += 1
                                semester_row_no__dic[semester_no] = row
                                semester_col_no__dic[semester_no] = col
                    semester_row_no__dic[semester_no+1]=semester_row_no__dic[semester_no-1]+9
                    semester_row_no__dic[semester_no + 2] = semester_row_no__dic[semester_no] + 9

                    for i in range(semester_no):
                        semester = "Semester " + str(i + 1)
                        code_row = None
                        code_col = None
                        title_col = None
                        credit_col = None
                        grade_col = None

                        start_row = semester_row_no__dic[i + 1]
                        start_col = semester_col_no__dic[i + 1]
                        end_row = semester_row_no__dic[i + 3]
                        end_col = semester_col_no__dic[i + 1] + 7

                        for row in range(start_row, end_row):
                            for col in range(start_col, end_col):
                                if type(s.cell(row, col).value) == float:
                                    pass
                                elif type(s.cell(row, col).value) == int:
                                    pass
                                elif "Code" in s.cell(row, col).value:
                                    code_row = row
                                    code_col = col
                        for col in range(start_col, end_col):
                            if type(s.cell(code_row, col).value) == float:
                                pass
                            elif type(s.cell(code_row, col).value) == int:
                                pass
                            elif "Title" in s.cell(code_row, col).value:
                                title_col = col
                            elif "Cr" in s.cell(code_row, col).value:
                                credit_col = col
                            elif "Grade" in s.cell(code_row, col).value:
                                grade_col = col
                        codes = []
                        titles = []
                        creditss = []
                        grades = []
                        for row in range(code_row + 1, end_row):
                            if s.cell(row, code_col).value != "":
                                codes.append(str(s.cell(row, code_col).value))
                                titles.append(str(s.cell(row, title_col).value))
                                creditss.append(str(s.cell(row, credit_col).value))
                                grades.append(str(s.cell(row, grade_col).value))
                        self.code_by_semester[semester] = codes
                        self.title_by_semester[semester] = titles
                        self.credit_by_semester[semester] = creditss
                        self.grade_by_semester[semester] = grades
                        self.code_list_by_grade_by_semester.setdefault(semester,{})
                        self.code_list_by_grade_by_semester[semester].setdefault("A", [])
                        self.code_list_by_grade_by_semester[semester].setdefault("B", [])
                        self.code_list_by_grade_by_semester[semester].setdefault("C", [])
                        self.code_list_by_grade_by_semester[semester].setdefault("D", [])
                        self.code_list_by_grade_by_semester[semester].setdefault("F", [])
                        self.code_list_by_grade_by_semester[semester].setdefault("GUESS", [])
                        self.code_list_by_grade_by_semester[semester]["A"]=[]
                        self.code_list_by_grade_by_semester[semester]["B"]=[]
                        self.code_list_by_grade_by_semester[semester]["C"]=[]
                        self.code_list_by_grade_by_semester[semester]["D"]=[]
                        self.code_list_by_grade_by_semester[semester]["F"]=[]
                        self.code_list_by_grade_by_semester[semester]["GUESS"]=[]
                        for y in range(len(self.code_by_semester[semester])):
                            grade=self.grade_by_semester[semester][y]
                            if grade.find("A")!=-1:
                                self.code_list_by_grade_by_semester[semester]["A"].append(self.code_by_semester[semester][y])
                            elif grade.find("B")!=-1:
                                self.code_list_by_grade_by_semester[semester]["B"].append(self.code_by_semester[semester][y])
                            elif grade.find("C") != -1:
                                self.code_list_by_grade_by_semester[semester]["C"].append(self.code_by_semester[semester][y])
                            elif grade.find("D") != -1:
                                self.code_list_by_grade_by_semester[semester]["D"].append(self.code_by_semester[semester][y])
                            elif grade.find("F") != -1:
                                self.code_list_by_grade_by_semester[semester]["F"].append(self.code_by_semester[semester][y])
                            elif grade=="":
                                self.code_list_by_grade_by_semester[semester]["GUESS"].append(self.code_by_semester[semester][y])
            self.classifyCoursesFromCurriculum()
        except:
            self.CurriculumProblem = True
            tkMessageBox.showinfo("Warning!", "Hey mate! Upload a valid curriculum file, please.")

    def classifyCoursesFromCurriculum(self):
        self.listA=[]
        self.listB=[]
        self.listC=[]
        self.listD=[]
        self.listF=[]
        self.dictGuess={}

        for semester in self.code_list_by_grade_by_semester:
            self.listA.extend(self.code_list_by_grade_by_semester[semester]["A"])
            self.listB.extend(self.code_list_by_grade_by_semester[semester]["B"])
            self.listC.extend(self.code_list_by_grade_by_semester[semester]["C"])
            self.listD.extend(self.code_list_by_grade_by_semester[semester]["D"])
            self.listF.extend(self.code_list_by_grade_by_semester[semester]["F"])
            self.dictGuess.setdefault(semester, [])
            for coursecode in (self.code_list_by_grade_by_semester[semester]["GUESS"]):
                if coursecode.split()[0]=="UNI":
                    pass
                elif coursecode.split()[0] == "EECS":
                    pass
                elif coursecode.split()[0].lower() == "xxx":
                    pass
                else:
                    self.dictGuess[semester].append(coursecode)

        self.listUsedUNI=[]
        self.listUsedEECS=[]

        for coursecodeA in self.listA:
            if coursecodeA.split()[0]=="UNI":
                self.listUsedUNI.append(coursecodeA)
            if coursecodeA.split()[0] == "EECS":
                self.listUsedEECS.append(coursecodeA)

        for coursecodeB in self.listB:
            if coursecodeB.split()[0] == "UNI":
                self.listUsedUNI.append(coursecodeB)
            if coursecodeB.split()[0] == "EECS":
                self.listUsedEECS.append(coursecodeB)

        for coursecodeC in self.listC:
            if coursecodeC.split()[0] == "UNI":
                self.listUsedUNI.append(coursecodeC)
            if coursecodeC.split()[0] == "EECS":
                self.listUsedEECS.append(coursecodeC)

        for coursecodeD in self.listD:
            if coursecodeD.split()[0] == "UNI":
                self.listUsedUNI.append(coursecodeD)
            if coursecodeD.split()[0] == "EECS":
                self.listUsedEECS.append(coursecodeD)

        for coursecodeF in self.listF:
            if coursecodeF.split()[0] == "UNI":
                self.listUsedUNI.append(coursecodeF)
            if coursecodeF.split()[0] == "EECS":
                self.listUsedEECS.append(coursecodeF)


        self.listUNI=[]
        self.listEECS=[]
        for courseCode in self.listA:
            if courseCode.split()[0]=="UNI":
                self.listUNI.append(courseCode)
            if courseCode.split()[0] == "EECS":
                self.listEECS.append(courseCode)
        for courseCode in self.listB:
            if courseCode.split()[0] == "UNI":
                self.listUNI.append(courseCode)
            if courseCode.split()[0] == "EECS":
                self.listEECS.append(courseCode)
        for courseCode in self.listC:
            if courseCode.split()[0] == "UNI":
                self.listUNI.append(courseCode)
            if courseCode.split()[0] == "EECS":
                self.listEECS.append(courseCode)
        for courseCode in self.listD:
            if courseCode.split()[0] == "UNI":
                self.listUNI.append(courseCode)
            if courseCode.split()[0] == "EECS":
                self.listEECS.append(courseCode)
        for courseCode in self.listF:
            if courseCode.split()[0] == "UNI":
                self.listUNI.append(courseCode)
            if courseCode.split()[0] == "EECS":
                self.listEECS.append(courseCode)

    def onClickPredictGrades(self):

        # at first, let's clear our listBox
        self.mylist.delete(0, END)

        if self.CurriculumProblem==False:
            try:
                URLs1=self.TextBox.get("1.0", END).split("\n")
                URLs=[]
                for urls1 in URLs1:
                    if urls1!="":
                        URLs.append(urls1)

                self.getDescriptions(URLs)
                predictedGrades = self.classifyCoursesAll()

                colors = ["green", "gray", "yellow", "red", "black"]

                groups=predictedGrades.keys()
                groups.sort()

                n = 0

                for semester in groups[1:(len(groups)-1)]:
                    self.mylist.insert(n, semester)
                    n+=1
                    for code in predictedGrades[semester]:
                        grade=predictedGrades[semester][code]
                        text=code+" --> "+grade
                        self.mylist.insert(n, text)
                        if grade=="A":
                            self.mylist.itemconfig(n, {"fg": "white"})
                            self.mylist.itemconfig(n, {"bg": colors[0]})
                        if grade=="B":
                            self.mylist.itemconfig(n, {"fg": "green"})
                            self.mylist.itemconfig(n, {"bg": colors[1]})
                        if grade=="C":
                            self.mylist.itemconfig(n, {"fg": "white"})
                            self.mylist.itemconfig(n, {"bg": colors[2]})
                        if grade=="D":
                            self.mylist.itemconfig(n, {"fg": "white"})
                            self.mylist.itemconfig(n, {"bg": colors[3]})
                        if grade=="F":
                            self.mylist.itemconfig(n, {"fg": "white"})
                            self.mylist.itemconfig(n, {"bg": colors[4]})
                        n+=1
                    self.mylist.insert(n, " ")
                    n += 1

                self.mylist.insert(n, groups[0])
                n += 1
                for code in predictedGrades[groups[0]]:
                    grade = predictedGrades[groups[0]][code]
                    text = code + " --> " + grade
                    self.mylist.insert(n, text)
                    if grade == "A":
                        self.mylist.itemconfig(n, {"fg": "white"})
                        self.mylist.itemconfig(n, {"bg": colors[0]})
                    if grade == "B":
                        self.mylist.itemconfig(n, {"fg": "green"})
                        self.mylist.itemconfig(n, {"bg": colors[1]})
                    if grade == "C":
                        self.mylist.itemconfig(n, {"fg": "white"})
                        self.mylist.itemconfig(n, {"bg": colors[2]})
                    if grade == "D":
                        self.mylist.itemconfig(n, {"fg": "white"})
                        self.mylist.itemconfig(n, {"bg": colors[3]})
                    if grade == "F":
                        self.mylist.itemconfig(n, {"fg": "white"})
                        self.mylist.itemconfig(n, {"bg": colors[4]})
                    n += 1
                self.mylist.insert(n, " ")
                n += 1

                self.mylist.insert(n, groups[(len(groups)-1)])
                n += 1
                for code in predictedGrades[groups[(len(groups)-1)]]:
                    grade = predictedGrades[groups[(len(groups)-1)]][code]
                    text = code + " --> " + grade
                    self.mylist.insert(n, text)
                    if grade == "A":
                        self.mylist.itemconfig(n, {"fg": "white"})
                        self.mylist.itemconfig(n, {"bg": colors[0]})
                    if grade == "B":
                        self.mylist.itemconfig(n, {"fg": "green"})
                        self.mylist.itemconfig(n, {"bg": colors[1]})
                    if grade == "C":
                        self.mylist.itemconfig(n, {"fg": "white"})
                        self.mylist.itemconfig(n, {"bg": colors[2]})
                    if grade == "D":
                        self.mylist.itemconfig(n, {"fg": "white"})
                        self.mylist.itemconfig(n, {"bg": colors[3]})
                    if grade == "F":
                        self.mylist.itemconfig(n, {"fg": "white"})
                        self.mylist.itemconfig(n, {"bg": colors[4]})
                    n += 1
                self.mylist.insert(n, " ")
                n += 1

            except:
                tkMessageBox.showinfo("Warning!", "Some of URLs are not valid or cannot be opened...")

        else:
            tkMessageBox.showinfo("Warning!", "Hey mate! Upload a valid curriculum file, please.")

    def getDescriptions(self, url_list):
        self.course_names=[]
        self.descriptions_list=[]
        self.features_list=[]
        for url in url_list:
            driver = webdriver.Firefox()
            driver.get(url)
            time.sleep(2)
            element = driver.find_elements_by_tag_name("a")
            clickCourseDescriptions = False
            for i in element:
                if i.text == "Course Descriptions":
                    i.click()
                    clickCourseDescriptions = True
            time.sleep(2)
            html_doc = driver.page_source
            driver.close()
            soup = BeautifulSoup(html_doc, "html.parser")
            soup.prettify()
            for i1 in soup.find_all(class_="fakulte_ack"):
                i1.prettify()
            soup_div_list = soup.find_all(class_="fakulte_ack")

            text_list = []
            for i2 in soup_div_list:
                text_list.append(i2.text.strip())

            text = ""
            for i3 in text_list:
                for n in i3.split():
                    text += " " + n

            course_names = []

            for i4 in soup_div_list:
                if clickCourseDescriptions == True:
                    if i4.strong != None:
                        for s in i4.find_all("strong"):
                            split = s.text.split()
                            if split != [] and len(split) > 2:
                                text1 = " ".join(split[:3])
                                text2 = " ".join(split)
                                warning = False
                                if text1.find("ECTS") != -1:
                                    warning = True
                                if text1.find("credits") != -1:
                                    warning = True
                                if warning == False:
                                    if text1 not in course_names:
                                        course_names.append(text2)

                else:
                    if i4.p != None:
                        for s in i4.find_all("p"):
                            text1 = " ".join(s.text.split())
                            if text1.find("UNI") != -1:
                                course_names.append(text1)

            list3 = []
            firstStep = text.split(course_names[0])[1]
            secondStep = firstStep.split(course_names[1])
            list3.extend(secondStep)
            list4 = list3
            for i5 in range(len(course_names) - 2):
                x = i5 + 2
                list5 = []
                list5.extend(list4[:(len(list4) - 1)])
                item = list4[len(list4) - 1]
                splitItem = item.split(course_names[x])
                list5.extend(splitItem)
                list4 = list5
            descriptions_list = list4

            self.course_names.extend(course_names)
            self.descriptions_list.extend(descriptions_list)

        for num in range(len(self.course_names)):
            feature=(self.course_names[num])+"\n"+(self.descriptions_list[num])
            self.features_list.append(feature)

    def classifyCoursesAll(self):
        self.classified={}
        self.classified.setdefault("A",[])
        self.classified.setdefault("B",[])
        self.classified.setdefault("C",[])
        self.classified.setdefault("D",[])
        self.classified.setdefault("F",[])
        self.classified["A"]=[]
        self.classified["B"]=[]
        self.classified["C"]=[]
        self.classified["D"]=[]
        self.classified["F"]=[]

        for num1 in range(len(self.features_list)):
            courseText=(self.features_list[num1])
            courseName=(self.features_list[num1].split("\n")[0])
            if courseName.find("UNI ")==-1:
                for courseCodeA in self.listA:
                    if courseName.find(courseCodeA) != -1:
                        for coursetext in self.classified["A"]:
                            if courseName not in coursetext.split("\n"):
                                self.classified["A"].append(courseText)
                for courseCodeB in self.listB:
                    if courseName.find(courseCodeB) != -1:
                        for coursetext in self.classified["B"]:
                            if courseName not in coursetext.split("\n"):
                                self.classified["B"].append(courseText)
                for courseCodeC in self.listC:
                    if courseName.find(courseCodeC) != -1:
                        for coursetext in self.classified["C"]:
                            if courseName not in coursetext.split("\n"):
                                self.classified["C"].append(courseText)
                for courseCodeD in self.listD:
                    if courseName.find(courseCodeD) != -1:
                        for coursetext in self.classified["D"]:
                            if courseName not in coursetext.split("\n"):
                                self.classified["D"].append(courseText)
                for courseCodeF in self.listF:
                    if courseName.find(courseCodeF) != -1:
                        for coursetext in self.classified["F"]:
                            if courseName not in coursetext.split("\n"):
                                self.classified["F"].append(courseText)
            else:
                for courseCodeA in self.listA:
                    if courseName.find(courseCodeA.split()[0]) != -1:
                        if courseName.find(courseCodeA.split()[1]) != -1:
                            if courseText not in self.classified["A"]:
                                self.classified["A"].append(courseText)
                for courseCodeB in self.listB:
                    if courseName.find(courseCodeB.split()[0]) != -1:
                        if courseName.find(courseCodeB.split()[1]) != -1:
                            if courseText not in self.classified["B"]:
                                self.classified["B"].append(courseText)
                for courseCodeC in self.listC:
                    if courseName.find(courseCodeC.split()[0]) != -1:
                        if courseName.find(courseCodeC.split()[1]) != -1:
                            if courseText not in self.classified["C"]:
                                self.classified["C"].append(courseText)
                for courseCodeD in self.listD:
                    if courseName.find(courseCodeD.split()[0]) != -1:
                        if courseName.find(courseCodeD.split()[1]) != -1:
                            if courseText not in self.classified["D"]:
                                self.classified["D"].append(courseText)
                for courseCodeF in self.listF:
                    if courseName.find(courseCodeF.split()[0]) != -1:
                        if courseName.find(courseCodeF.split()[1]) != -1:
                            if courseText not in self.classified["F"]:
                                self.classified["F"].append(courseText)

        cl = docclass.naivebayes(docclass.getwords)
        for grade in self.classified:
            for course in self.classified[grade]:
                cl.train(course, grade)

        """
        dictGuess1[semester] is a dictionary.
        dictGuess1[semester]=courseCodeFromCurriculum
        dictGuess1[semester][courseCodeFromCurriculum]=courseText
        """

        dictGuess1 = {}

        for semester in self.dictGuess:
            if len(self.dictGuess[semester])>0:
                dictGuess1.setdefault(semester,{})
                for courseCodeGuess in self.dictGuess[semester]:
                    dictGuess1[semester].setdefault(courseCodeGuess,[])
                    dictGuess1[semester][courseCodeGuess]=[]
                    for num2 in range(len(self.features_list)):
                        courseText2 = (self.features_list[num2])
                        courseName2 = (self.features_list[num2].split("\n")[0])
                        if courseName2.find(courseCodeGuess) != -1:
                            if courseText2 not in dictGuess1[semester][courseCodeGuess]:
                                dictGuess1[semester][courseCodeGuess].append(courseText2)

        dictGuess1.setdefault("UNI COURSES",{})
        for num3 in range(len(self.features_list)):
            courseText3 = (self.features_list[num3])
            courseName3 = (self.features_list[num3].split("\n")[0])
            if courseName3.find("UNI ") != -1:
                coursecodes3=[]
                for word in courseName3.split():
                    if len(word)==3:
                        try:
                            num=int(word)
                            code3="UNI "+str(num)
                            coursecodes3.append(code3)
                        except:
                            pass
                for courseCodeUNI in coursecodes3:
                    if courseCodeUNI not in self.listUsedUNI:
                        dictGuess1["UNI COURSES"].setdefault(courseCodeUNI, [])
                        if courseText3 not in dictGuess1["UNI COURSES"][courseCodeUNI]:
                            dictGuess1["UNI COURSES"][courseCodeUNI].append(courseText3)

        dictGuess1.setdefault("EECS COURSES",{})
        for num4 in range(len(self.features_list)):
            courseText4 = (self.features_list[num4])
            courseName4 = (self.features_list[num4].split("\n")[0])
            if courseName4.split()[0].find("EECS") != -1:
                courseCodeEECS=" ".join(courseName4.split()[:2])
                if courseCodeEECS not in self.listUsedEECS:
                    dictGuess1["EECS COURSES"].setdefault(courseCodeEECS, [])
                    if courseText4 not in dictGuess1["EECS COURSES"][courseCodeEECS]:
                        dictGuess1["EECS COURSES"][courseCodeEECS].append(courseText4)

        """
        self.predictedGradesDict[group][courseCodeFromCurriculum]=predictedGrade
        """
        self.predictedGradesDict = {}
        for group in dictGuess1:
            self.predictedGradesDict.setdefault(group, {})
            for courseCodeFromCurriculum in dictGuess1[group]:
                if len(dictGuess1[group][courseCodeFromCurriculum])>0:
                    self.predictedGradesDict[group].setdefault(courseCodeFromCurriculum, {})
                    self.predictedGradesDict[group][courseCodeFromCurriculum]=cl.classify(dictGuess1[group][courseCodeFromCurriculum][0])

        return self.predictedGradesDict


def main():
    root = Tk()
    root.wm_title("Guess My Grade")
    root.geometry("1010x620+150+30")
    app = CurriculumViewer(root)
    root.mainloop()

if __name__ == '__main__':
    main()
