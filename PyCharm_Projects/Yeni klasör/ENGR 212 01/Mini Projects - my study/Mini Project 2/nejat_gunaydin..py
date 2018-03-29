"""
My references:
* for learning how to use xlrd module, i took a look at:
        #https://secure.simplistix.co.uk/svn/xlrd/trunk/xlrd/doc/xlrd.html?p=4966
        #http://www.simplistix.co.uk/presentations/python-excel.pdf
* in order to create my Combobox menu, i used codes in :
        #http://stackoverflow.com/questions/17757451/simple-ttk-combobox-demo
* for vertical scrollbar, i used codes in :
        #http://www.java2s.com/Tutorial/Python/0360__Tkinker/ListBoxwithscrollbar.htm
* for slider widget, i used codes in :
        #http://www.python-course.eu/tkinter_sliders.php
* for RadioButton widget, i used codes in :
        #http://effbot.org/tkinterbook/radiobutton.htm
        #http://www.python-course.eu/tkinter_radiobuttons.php
* in order to create my message boxes, i used this one :
        #http://www.tutorialspoint.com/python/tk_messagebox.htm
* i needed to make a rewision about anydbm database from :
        #https://docs.python.org/2/library/anydbm.html
* from there, i found how can I find path to given file by using os module :
        #http://stackoverflow.com/questions/1124810/how-can-i-find-path-to-given-file
* for getting a appropriate self.value_of_combo, i took a look to :
        #https://docs.python.org/3/howto/unicode.html
        #http://stackoverflow.com/questions/846850/read-unicode-characters-from-command-line-arguments-in-python-2-x-on-windows

* for str.find method on string=str, i took a look to :
        #http://www.tutorialspoint.com/python/string_find.htm

*the rest was mostly referenced from LMS files.
"""
#-*- coding: utf-8 -*-

from Tkinter import *
import ttk
import os
import pickle
import tkMessageBox
from anydbm import *
from xlrd import *


class CafeCrownRecommendationEngine(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.value_of_combo = None
        self.ownratings=None
        self.db_path = None
        self.initUI()

    def initUI(self):
        self.pack(fill=BOTH, expand=True)

        #title line
        var = StringVar()
        title = Label(self, textvariable=var, bg="black", fg="yellow", font='Arial 20 bold')
        var.set("Cafe Crown Recommendation Engine - SEHIR Special Edition")
        title.pack(fill=X)

        #"Welcome" message labels
        Label(self,text="Welcome!"+"\n"+"Please rate entries that you have had at CC, and we will recommend you "+
                                        "what you may like to have!", font='Arial 14').pack(fill=X)

        # "||" separator
        Label(self, text=("||"*999), font='Arial 5').pack()

        #Let's use a frame to put some of our following tools in.
        frame1=Frame(self)
        #"Choose a meal" inner-frame, with ComboBox menu
        frame11=Frame(frame1)
        Label(frame11, text="Choose a meal:    \n\n", fg='red', font='Arial 12 bold').pack()
        meals=self.meal_names()
        self.box_value = StringVar()
        self.box = ttk.Combobox(frame11, textvariable=self.box_value)
        self.box.bind("<<ComboboxSelected>>", self.newselection)
        self.box['values'] = meals
        self.box.pack()
        frame11.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=5)
        #"Enter your rating" inner-frame
        frame12=Frame(frame1)
        Label(frame12, text="\nEnter your rating:   \n", fg='red', font='Arial 12 bold').pack()
        self.scale=IntVar()
        Scale(frame12, from_=0, to=10, length=180, orient=HORIZONTAL, variable=self.scale).pack()
        frame12.pack(side=LEFT, fill=BOTH, expand=True, padx=20)
        # user ratings add/remove
        frame13=Frame(frame1)
        Button(frame13, text="Add", font='ArialBlack 10 bold', fg='blue',
               command=self.onClickAdd).pack(side=LEFT, padx=20)
        listBoxWithScrollbar=Frame(frame13)
        scrollbar=Scrollbar(listBoxWithScrollbar)
        self.mylist=Listbox(listBoxWithScrollbar, height=5, width=30,yscrollcommand=scrollbar.set)
        self.mylist.bind("<Double-Button-1>", self.OnDouble)
        self.search_ownratings()
        self.mylistshow()
        scrollbar.config(command=self.mylist.yview)
        self.mylist.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=LEFT, fill=Y)
        listBoxWithScrollbar.pack(side=LEFT, fill=BOTH, expand=True)
        Button(frame13, text="Remove\nSelected", font='ArialBlack 10 bold',
               fg='red', command=self.onClickRemoveSelected).pack(side=LEFT, padx=20)
        frame13.pack(side=LEFT, padx=20)
        frame1.pack(pady=5)

        # "||" separator, again.
        Label(self, text=("||" * 999), font='Arial 5').pack()
        #
        Label(self, text="Get Recommendations", font='Arial 15 bold').pack()

        # "||" separator, again.
        Label(self, text=("||" * 999), font='Arial 5').pack()

        # the part where user configure settings for the recommendation engine
        frame2=Frame(self)
        frame21=Frame(frame2)
        Label(frame21, text="Settings:                                   ", fg='red', font='Arial 12 bold').pack()
        frame21a=Frame(frame21)
        Label(frame21a, text="Number of recommendations:   ", font='Arial 10').pack(side=LEFT)
        self.numOfRecom=Entry(frame21a, width=4)
        self.numOfRecom.pack(side=LEFT)
        self.numOfRecom.insert(0, "10")
        frame21a.pack()
        frame21.pack(side=LEFT, padx=10)
        frame22=Frame(frame2)
        frame22a=Frame(frame22)
        Label(frame22a, text="\nChoose recommendation method:", fg='purple', font='Arial 9 italic').pack()
        self.method=StringVar()
        self.method.set("userBased")  # initialize our selected point
        Radiobutton(frame22a, text="User-Based", padx=20, variable=self.method, value="userBased").pack(anchor=W)
        Radiobutton(frame22a, text="Item-Based", padx=20, variable=self.method, value="itemBased").pack(anchor=W)
        Label(frame22a, text="Choose similarity metric:                    ", fg='purple', font='Arial 9 italic').pack()
        self.metric=StringVar()
        self.metric.set("EuclideanScore")  # initialize our selected point
        Radiobutton(frame22a,text="Euclidean Score",padx=20,variable=self.metric,value="EuclideanScore").pack(anchor=W)
        Radiobutton(frame22a,text="Pearson Score",padx=20,variable=self.metric,value="PearsonScore").pack(anchor=W)
        Radiobutton(frame22a,text="Jaccard Score",padx=20,variable=self.metric,value="JaccardScore").pack(anchor=W)
        frame22a.pack(side=LEFT, padx=20)
        Button(frame22, text="Get Recommendations", font='ArialBlack 10 bold', fg='blue',
               command=self.onClickGetRecom).pack(side=LEFT)
        frame22.pack(side=RIGHT, padx=10)
        frame2.pack(fill=X)

        # "||" separator, again.
        Label(self, text=("||" * 999), font='Arial 5').pack()

        #
        frame3=Frame(self)
        frame31=Frame(frame3)
        Label(frame31, text="Result Box (Recommendations):   ", font='Arial 10').pack()
        listBoxWithScrollbar2 = Frame(frame31)
        scrollbar2 = Scrollbar(listBoxWithScrollbar2)
        self.mylist2 = Listbox(listBoxWithScrollbar2, selectmode=BROWSE, height=8, width=30,
                               yscrollcommand=scrollbar2.set)
        self.search_recommendations()
        scrollbar2.config(command=self.mylist2.yview)
        self.mylist2.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar2.pack(side=LEFT, fill=Y)
        listBoxWithScrollbar2.pack(side=LEFT, fill=BOTH, expand=True)
        frame31.pack(side=LEFT, padx=10)

        frame32=Frame(frame3)

        listBoxWithScrollbar3 = Frame(frame32)
        scrollbar3 = Scrollbar(listBoxWithScrollbar3)
        self.mylist3 = Listbox(listBoxWithScrollbar3, selectmode=BROWSE, height=8, width=30,
                               yscrollcommand=scrollbar3.set)
        self.search_recommendations()
        scrollbar3.config(command=self.mylist3.yview)
        self.mylist3.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar3.pack(side=LEFT, fill=Y)
        listBoxWithScrollbar3.pack(side=LEFT, fill=BOTH, expand=True)
        frame32.pack(side=LEFT, padx=10)
        frame3.pack(fill=X)

    def meal_names(self):
        meals={}
        menu = open_workbook("Menu.xlsx")
        for s in menu.sheets():
            for row in range(1, s.nrows):
                meals[s.cell(row, 0).value.encode("utf-8")] = float(s.cell(row, 1).value)
        values=meals.keys()
        values.sort()
        return values


    def newselection(self, event):
        self.value_of_combo = self.box.get()


    def search_ownratings(self):
        for root, dirs, files in os.walk(os.getcwd()):
            for name in files:
                if name == "ownratings.db":
                    self.db_path = os.path.abspath(os.path.join(root, name))

    def mylistshow(self):
        if self.db_path==None:
            pass
        else:
            self.ownratings=open("ownratings.db",'r')
            for i in self.ownratings:
                line=pickle.loads(i)+" --> "+str(pickle.loads(self.ownratings[i]))
                self.mylist.insert(END, line)
            self.ownratings.close()

    def OnDouble(self, event):
        widget = event.widget
        selection = widget.curselection()
        self.value = widget.get(selection[0])

    def onClickAdd(self):
        if self.value_of_combo == None:
            tkMessageBox.showinfo("Warning!","Chose a meal, please.")
        else:
            meal=self.value_of_combo+" --> "+str(self.scale.get())
            linelist=list(self.mylist.get(0, END))
            if len(linelist) == 0:
                self.mylist.insert(0, meal)
            else:
                inlistnum=None
                for i in range(len(linelist)):
                    if self.value_of_combo in linelist[i]:
                            inlistnum=i
                if inlistnum!=None:
                    self.mylist.delete(inlistnum,inlistnum)
                    self.mylist.insert(inlistnum, meal)
                else:
                    self.mylist.insert(0, meal)
            #
            self.ownratings=open("ownratings.db",'c')
            meal_db=pickle.dumps(self.value_of_combo)
            rating=pickle.dumps(self.scale.get())
            self.ownratings[meal_db]=rating
            print self.ownratings
            self.ownratings.close()

    def onClickRemoveSelected(self):
        print self.value

        self.ownratings = open("ownratings.db", 'c')

        self.ownratings.close()
        #self.mylistrefresh()
        linelist = list(self.mylist.get(0, END))
        inlistnum = None
        for i in range(len(linelist)):
            if self.value in linelist[i]:
                inlistnum = i
        if inlistnum != None:
            self.mylist.delete(inlistnum, inlistnum)

    def onClickGetRecom(self):
        numOfRecomendations = self.numOfRecom.get()
        print numOfRecomendations
        print self.method.get()
        print self.metric.get()

    def mylistrefresh(self):
        self.mylist.delete(0, END)
        self.ownratings = open("ownratings.db", 'r')
        for i in self.ownratings:
            line = pickle.loads(i) + " --> " + str(pickle.loads(self.ownratings[i]))
            self.mylist.insert(END, line)
        self.ownratings.close()

    def search_recommendations(self):
        print 1

def main():
    root = Tk()
    root.wm_title("CafeCrownRecommendationEngine")
    root.geometry("850x650+250+35")
    app = CafeCrownRecommendationEngine(root)
    root.mainloop()

if __name__ == '__main__':
    main()