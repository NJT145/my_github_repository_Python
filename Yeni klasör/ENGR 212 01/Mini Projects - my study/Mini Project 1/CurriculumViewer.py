"""
My references:
* for choosing a file whith my of Browse buttons, i used codes in :
        #http://tkinter.unpythonic.net/wiki/tkFileDialog
* in order to create my Combobox menu, i used codes in :
        #http://stackoverflow.com/questions/17757451/simple-ttk-combobox-demo
* in order to create my message boxes, i used this one :
        #http://www.tutorialspoint.com/python/tk_messagebox.htm
* i needed to make a rewision about anydbm database from :
        #https://docs.python.org/2/library/anydbm.html
* from there,i found infos about destroy a widget when i do a second click on button Display :
        #https://mail.python.org/pipermail/tutor/2001-February/003453.html
* from there, i found how can I find path to given file by using os module :
        #http://stackoverflow.com/questions/1124810/how-can-i-find-path-to-given-file
* for learning how to use xlrd module, i took a look at:
        #https://secure.simplistix.co.uk/svn/xlrd/trunk/xlrd/doc/xlrd.html?p=4966
        #http://www.simplistix.co.uk/presentations/python-excel.pdf
*the rest was mostly referenced from LMS files.
"""

from Tkinter import *
import ttk
from tkFileDialog import *
import tkMessageBox
from anydbm import *
import pickle
import os
from xlrd import *

browse=None
combobox_select=None
sheet_name=None
semester_row_no__dic={}
semester_col_no__dic={}
semester_no=0

code_by_semester={}
title_by_semester={}
credit_by_semester={}

db_path=None

class CurriculumViewer(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.value_of_combo = None
        self.frame4 = None
        self.initUI()

    def initUI(self):
        self.pack(fill=BOTH, expand=True)
        #title line
        var = StringVar()
        title = Label(self, textvariable=var, bg="green", fg="white", font='Helvetica 40')
        var.set("Curriculum Viewer v1.0")
        title.pack(fill=X)
        #first line
        frame1 = Frame(self)
        ##browse button at right
        Button(frame1, text="Browse", command=self.onClickBrowse).pack(side=RIGHT)
        #label at left
        Label(frame1, text="Please select curriculum excel file:").pack(side=RIGHT)
        #need to pack first line to see it
        frame1.pack()
        #second line
        frame2 = Frame(self)
        #Combobox at right
        self.box_value = StringVar()
        self.box = ttk.Combobox(frame2, textvariable=self.box_value)
        self.box.bind("<<ComboboxSelected>>", self.newselection)
        self.box['values'] = ("Semester 1","Semester 2","Semester 3","Semester 4","Semester 5","Semester 6",
                                "Semester 7", "Semester 8")
        self.box.pack(side=RIGHT)
        #second label at left
        Label(frame2, text="           Please select semester that you want to print:").pack(side=RIGHT)
        #need to pack second line to see it
        frame2.pack()
        #third line
        frame3 = Frame(self)
        #display button at right
        Button(frame3, text="Display", command=self.onClickDisplay).pack(side=RIGHT)
        #empty space for geometry
        Label(frame3, text="                                                         ").pack(side=RIGHT)
        #need to pack third line to see it
        frame3.pack()

    #the function that defines what's going to happen when you select a semester on Combobox
    def newselection(self, event):
        self.value_of_combo = self.box.get()
        global combobox_select
        for i in range(8):
            if self.value_of_combo==("Semester "+str(i+1)):
                combobox_select="Semester "+str(i+1)
    #the function that makes you able to choose an excel file to use
    def onClickBrowse(self):
        browse = askopenfilename()
        #let's find our infos
        wb = open_workbook(browse)
        for s in wb.sheets():
            if "curriculum" in s.name:
                global sheet_name
                sheet_name=s.name
                for row in range(s.nrows):
                    global semester_no
                    global semester_row_no__dic
                    global semester_col_no__dic
                    for col in range(s.ncols):
                        if type(s.cell(row,col).value)==float:
                            pass
                        elif type(s.cell(row,col).value)==int:
                            pass
                        elif "Semester I" in s.cell(row,col).value:
                            semester_no+=1
                            semester_row_no__dic[semester_no]=row
                            semester_col_no__dic[semester_no]=col
                        elif "Semester V" in s.cell(row,col).value:
                            semester_no+=1
                            semester_row_no__dic[semester_no]=row
                            semester_col_no__dic[semester_no]=col
                semester_row_no__dic[semester_no+1]=semester_row_no__dic[semester_no-1]+9
                semester_row_no__dic[semester_no+2]=semester_row_no__dic[semester_no]+9
                for i in range(semester_no):
                    semester="Semester "+str(i+1)
                    code_row=None
                    code_col=None
                    title_col=None
                    credit_col=None

                    start_row=semester_row_no__dic[i+1]
                    start_col=semester_col_no__dic[i+1]
                    end_row=semester_row_no__dic[i+3]
                    end_col=semester_col_no__dic[i+1]+7

                    for row in range(start_row,end_row):
                        for col in range(start_col,end_col):
                            if type(s.cell(row,col).value)==float:
                                pass
                            elif type(s.cell(row,col).value)==int:
                                pass
                            elif "Code" in s.cell(row,col).value:
                                code_row=row
                                code_col=col
                    for col in range(start_col,end_col):
                        if type(s.cell(code_row,col).value)==float:
                            pass
                        elif type(s.cell(code_row,col).value)==int:
                            pass
                        elif "Title" in s.cell(code_row,col).value:
                            title_col=col
                        elif "Cr" in s.cell(code_row,col).value:
                            credit_col=col
                    codes=[]
                    titles=[]
                    creditss=[]
                    for row in range(code_row+1,end_row):
                        if s.cell(row,code_col).value!="":
                            codes.append(str(s.cell(row,code_col).value))
                            titles.append(str(s.cell(row,title_col).value))
                            creditss.append(str(s.cell(row,credit_col).value))
                    code_by_semester[semester]=codes
                    title_by_semester[semester]=titles
                    credit_by_semester[semester]=creditss

        #let's save our datas
        curriculumdb=open("curriculum.db","n")
        #we need to pickle our info dictionaries (by twice because they are dictionaries of lists) in order to save it
        codes=pickle.dumps(pickle.dumps(code_by_semester))
        titles=pickle.dumps(pickle.dumps(title_by_semester))
        credits=pickle.dumps(pickle.dumps(credit_by_semester))
        curriculumdb["codes_by_semester"]=codes
        curriculumdb["title_by_semester"]=titles
        curriculumdb["credit_by_semester"]=credits
        curriculumdb.close()

    #the function that shows information about the file that you choose
    def onClickDisplay(self):
        #we need to check if "curriculum.db" exists
        global db_path
        for root, dirs, files in os.walk(os.getcwd()):
            for name in files:
                if name == "curriculum.db":
                    db_path=os.path.abspath(os.path.join(root, name))
        if db_path==None:
            tkMessageBox.showinfo(
                "Warning!","A curriculum file should be selected first by clicking on the Browse button")
        else:
            #let's recover our datas
            curriculumdb=open("curriculum.db","c")
            codes_pickled=curriculumdb["codes_by_semester"]
            codes=pickle.loads(pickle.loads(codes_pickled))
            titles_pickled=curriculumdb["title_by_semester"]
            titles=pickle.loads(pickle.loads(titles_pickled))
            credits_pickled=curriculumdb["credit_by_semester"]
            credits=pickle.loads(pickle.loads(credits_pickled))

            #check if self.frame4 is created(changed from None to a frame) by clicking Display button;
            # and if it's created, we need to destroy it in order to prevent a creation of endless copies of it at
            # endless click on Display button.
            if self.frame4!=None:
                self.frame4.destroy()
                self.frame4=None
            #At first, check if a semester is choosen or not
            if combobox_select==None:
                tkMessageBox.showinfo("Warning!","You need to select a semester at first")
            else:
                #After selecting a semester,,let's create our dinamic frame which contains informations about our chosen file
                self.frame4 = Frame(self)
                #course codes column
                self.frame41 = Frame(self.frame4)
                Label(self.frame41, text="Course Code", font="system").pack()
                for i in range(len(codes[combobox_select])):
                    Label(self.frame41, text=codes[combobox_select][i]).pack()
                self.frame41.pack(side=LEFT)
                #course titles column
                self.frame42 = Frame(self.frame4)
                Label(self.frame42, text="Course Title", font="system").pack()
                for i in range(len(titles[combobox_select])):
                    Label(self.frame42, text=titles[combobox_select][i]).pack()
                self.frame42.pack(side=LEFT)
                #credits column
                self.frame43 = Frame(self.frame4)
                Label(self.frame43, text="Credit", font="system").pack()
                for i in range(len(credits[combobox_select])):
                    Label(self.frame43, text=credits[combobox_select][i]).pack()
                self.frame43.pack(side=LEFT)
                #Label(self.frame4, text=self.value_of_combo).pack()
                self.frame4.pack()



def main():
    root = Tk()
    root.wm_title("Curriculum Viewer v1.0")
    root.geometry("600x400+400+150")
    app = CurriculumViewer(root)
    root.mainloop()

if __name__ == '__main__':
    main()
