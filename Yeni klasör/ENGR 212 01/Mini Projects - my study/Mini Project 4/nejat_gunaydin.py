"""
My references:
* for listbox with scrollbar, i used codes in :
        #http://www.java2s.com/Tutorial/Python/0360__Tkinker/ListBoxwithscrollbar.htm
* in order to display an image from an URL at Tkinter in Python, i used codes in :
        #https://gist.github.com/dogukankotan/1b3277d1f0ab00f3771eee7dc862360b
*the rest was mostly referenced from LMS files and from lessons.
"""

#-*- coding: utf-8 -*-

from Tkinter import *
import ttk
import urllib2
from urllib2 import urlopen
from bs4 import *
import pickle
import io
from PIL import Image, ImageTk

class SEHIRResearchProjectsAnalyzer(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.years=None
        self.investigators=None
        self.institutions=None
        self.projectNames=None
        self.value_of_combo1 = None
        self.value_of_combo2 = None
        self.value_of_combo3 = None
        self.url = None
        self.projectTitles=[]
        self.titleSelection=None
        self.mycluster=None
        self.tupleListIMG_src = None
        self.tupleIMG_summary = None
        self.projectIMGsrc=None
        self.projectIMGsummary=None
        self.initUI()

    def initUI(self):
        self.pack(fill=BOTH, expand=True)

        #title line
        var = StringVar()
        var.set("SEHIR Research Projects Analyzer - CS Edition")
        title = Label(self, textvariable=var, bg="blue", fg="white", font='Verdana 14 bold', width=(len(var.get())+8))
        title.pack()


        #
        frame1=Frame(self)

        frame11=Frame(frame1)
        Label(frame11,text="Please provide an url:"+" "*75, font='10').pack()
        self.urlbox=Entry(frame11, width=75, bg="yellow")
        self.urlbox.insert(0,"http://cs.sehir.edu.tr/en/research/")
        self.urlbox.pack()
        frame11.pack(side=LEFT)

        Button(frame1, text="    Fetch Research Projects    ", relief=GROOVE, font="Verdana 8",
               command=self.onClickFetchResearchProjects).pack(side=LEFT, padx=170, pady=20)

        frame1.pack(pady=10)

        # "||" separator
        Label(self, text=("||" * 999), font='Arial 5').pack()

        #
        selection=Frame(self)

        selectionSettings=Frame(selection)
        Label(selectionSettings, text="Filter Research Projects By:"+" "*56, font="Verdana 10 bold").pack()

        #year selection inner-frame
        yearFrame=Frame(selectionSettings)
        Label(yearFrame, text="Year:"+" "*84, fg="blue", font="Helvetica 9").pack(side=LEFT)
        self.box1_value = StringVar()
        self.box1 = ttk.Combobox(yearFrame, textvariable=self.box1_value)
        self.box1.bind("<<ComboboxSelected>>", self.newselection1)
        self.box1['values'] = self.years
        self.box1.pack(side=LEFT)
        yearFrame.pack(pady=5)

        #investigator selection inner-frame
        investigatorFrame=Frame(selectionSettings)
        Label(investigatorFrame, text="Principal Investigator:"+" "*55, fg="blue", font="Helvetica 9").pack(side=LEFT)
        self.box2_value = StringVar()
        self.box2 = ttk.Combobox(investigatorFrame, textvariable=self.box2_value)
        self.box2.bind("<<ComboboxSelected>>", self.newselection2)
        self.box2['values'] = self.investigators
        self.box2.pack(side=LEFT)
        investigatorFrame.pack(pady=5)

        #institution selection inner-frame
        institutionFrame=Frame(selectionSettings)
        Label(institutionFrame, text="Funding Institution:"+" "*59, fg="blue", font="Helvetica 9").pack(side=LEFT)
        self.box3_value = StringVar()
        self.box3 = ttk.Combobox(institutionFrame, textvariable=self.box3_value)
        self.box3.bind("<<ComboboxSelected>>", self.newselection3)
        self.box3['values'] = self.institutions
        self.box3.pack(side=LEFT)
        institutionFrame.pack(pady=5)

        Button(selectionSettings, text="    Display Project Titles    ", relief=GROOVE, font="Verdana 8",
               command=self.onClickDisplayProjectTitles).pack(pady=10)

        selectionSettings.pack(side=LEFT)

        selectionProject=Frame(selection)
        Label(selectionProject, text="Pick a Project:"+" "*78, font="Verdana 10 bold").pack()

        listBoxWithScrollbar = Frame(selectionProject)
        scrollbar = Scrollbar(listBoxWithScrollbar)
        self.mylist = Listbox(listBoxWithScrollbar, height=6, width=70,
                              yscrollcommand=scrollbar.set)
        self.mylist.bind("<<ListboxSelect>>", self.OnClick)

        scrollbar.config(command=self.mylist.yview)
        self.mylist.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=LEFT, fill=Y)
        listBoxWithScrollbar.pack()

        Button(selectionProject, text="    Show Descriptions    ", relief=GROOVE, font="Verdana 8",
               command=self.onClickShowDescriptions).pack(pady=10)

        selectionProject.pack(padx=60,side=LEFT)

        selection.pack(pady=10)


        # "||" separator
        Label(self, text=("||" * 999), font='Arial 5').pack()

        #description results frame
        self.results=Frame(self)


        listBoxWithScrollbarResults = Frame(self.results)
        scrollbarY = Scrollbar(listBoxWithScrollbarResults)
        self.mylistResults = Listbox(listBoxWithScrollbarResults, height=15, width=70,
                              yscrollcommand=scrollbarY.set)
        scrollbarY.config(command=self.mylistResults.yview)
        self.mylistResults.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbarY.pack(side=LEFT, fill=Y)
        listBoxWithScrollbarResults.pack(side=RIGHT,pady=10)

        self.image = Canvas(self.results, bg='white')
        self.image.pack(side=RIGHT, fill='both', expand='yes', padx=60, pady=10)

        self.results.pack()


    def onClickFetchResearchProjects(self):
        self.url=self.urlbox.get()
        self.fetchProjects()
        if self.years != None:
            self.box1.set("All Years")
            self.box1['values'] = self.years
            self.value_of_combo1 = "All Years"
        if self.investigators != None:
            self.box2.set("All Investigators")
            self.box2['values'] = self.investigators
            self.value_of_combo2 = "All Investigators"
        if self.institutions != None:
            self.box3.set("All Institutions")
            self.box3['values'] = self.institutions
            self.value_of_combo3 = "All Institutions"
        print self.url


    def newselection1(self, event):
        self.value_of_combo1 = self.box1.get()

    def newselection2(self, event):
        self.value_of_combo2 = self.box2.get()

    def newselection3(self, event):
        self.value_of_combo3 = self.box3.get()

    def fetchProjects(self):
        pageInfo = urllib2.urlopen(self.url).read()
        pageSoup = BeautifulSoup(pageInfo, "html.parser")
        projectsSoup = pageSoup.find_all("li", "list-group-item")

        #
        self.mycluster = {}
        #
        projectDates = []
        projectDates_all = []
        for project in projectsSoup:
            projectDatesHTML = project.p.string
            dates = ""
            for lines in projectDatesHTML.split("\n"):
                if len(lines.split()) > 1:
                    date = (lines.split()[2])
                    dates = dates + "-" + date
                    projectDates_all.append(date)
            self.mycluster.setdefault(dates, {})
        for date in projectDates_all:
            if date not in projectDates:
                projectDates.append(date)
        projectDates.sort()
        self.years = projectDates
        self.years.insert(0, "All Years")

        investigators = []
        for project in projectsSoup:
            investigatorsHTML = project.contents[9]
            investigator = investigatorsHTML.a.string.strip()
            inv = pickle.dumps(investigator)
            if investigator not in investigators:
                investigators.append(investigator)
            projectDatesHTML = project.p.string
            dates = ""
            for lines in projectDatesHTML.split("\n"):
                if len(lines.split()) > 1:
                    date = (lines.split()[2])
                    dates = dates + "-" + date
            self.mycluster[dates].setdefault(investigator, {})
        investigators.sort()
        self.investigators = investigators
        self.investigators.insert(0, "All Investigators")

        institutions = []
        for project in projectsSoup:
            institutionsHTML = project.contents[7]
            inst = (str(institutionsHTML).split(">")[3].split("\n"))[1].strip()

            projectDatesHTML = project.p.string
            dates = ""
            for lines in projectDatesHTML.split("\n"):
                if len(lines.split()) > 1:
                    date = (lines.split()[2])
                    dates = dates + "-" + date

            investigatorsHTML = project.contents[9]
            investigator = investigatorsHTML.a.string.strip()

            if inst.find("&amp;") > 0:
                institution = inst[0:inst.find("&amp;")] + "&" + inst[inst.find("&amp;") + 5:len(inst)]
                self.mycluster[dates][investigator].setdefault(institution, {})
                if institution not in institutions:
                    institutions.append(institution)
            else:
                self.mycluster[dates][investigator].setdefault(inst, {})
                if inst not in institutions:
                    institutions.append(inst)
        institutions.sort()
        self.institutions=institutions
        self.institutions.insert(0, "All Institutions")

        #
        projectNames_all=[]
        self.tupleListIMG_src=[]
        self.tupleIMG_summary =[]
        for project in projectsSoup:
            projectName = project.a.get("id")
            projectNames_all.append(projectName)

            projectDatesHTML = project.p.string
            dates = ""
            for lines in projectDatesHTML.split("\n"):
                if len(lines.split()) > 1:
                    date = (lines.split()[2])
                    dates = dates + "-" + date

            investigatorsHTML = project.contents[9]
            investigator = investigatorsHTML.a.string.strip()

            institutionsHTML = project.contents[7]
            inst = (str(institutionsHTML).split(">")[3].split("\n"))[1].strip()
            if inst.find("&amp;") > 0:
                institution = inst[0:inst.find("&amp;")] + "&" + inst[inst.find("&amp;") + 5:len(inst)]
            else:
                institution=inst
            self.mycluster[dates][investigator][institution]=(projectName)

            projectIMGsrc = project.img.get("src")
            tupleIMG_src=(project,projectName,projectIMGsrc)
            self.tupleListIMG_src.append(tupleIMG_src)

            projectIMGsummary=project.img.p.text
            tupleIMG_summary=(project,projectName,projectIMGsummary)
            self.tupleIMG_summary.append(tupleIMG_summary)

        self.projectNames=projectNames_all

    def OnClick(self, event):
        if self.projectTitles == []:
            pass
        else:
            widget = event.widget
            selection = widget.curselection()
            self.titleSelection = widget.get(selection[0])
            print self.titleSelection

    #let's add project titles from projectNames to
    def onClickDisplayProjectTitles(self):
        if self.projectTitles!=[]:
            self.mylist.delete(0, END)
        if self.mycluster!=None:

            dates=[]
            for date in self.mycluster.keys():
                start_year=date.split("-")[1]
                end_year=date.split("-")[2]
                if self.value_of_combo1=="All Years":
                    dates.append(date)
                else:
                    if start_year<=self.value_of_combo1<=end_year:
                        dates.append(date)

            investigators=[]
            for date in dates:
                for investigator in self.mycluster[date]:
                    if self.value_of_combo2=="All Investigators":
                        investigators.append(investigator)
                    else:
                        if investigator==self.value_of_combo2:
                            investigators.append(investigator)

            institutions = []
            for date in dates:
                for investigator in self.mycluster[date]:
                    for institution in self.mycluster[date][investigator]:
                        if self.value_of_combo3 == "All Institutions":
                            institutions.append(institution)
                        else:
                            if institution == self.value_of_combo3:
                                institutions.append(institution)

            for  date in dates:
                self.titles=[]
                for investigator in investigators:
                    if investigator in self.mycluster[date]:
                        for institution in institutions:
                            if institution in self.mycluster[date][investigator]:
                                title=self.mycluster[date][investigator][institution]
                                if title not in self.titles:
                                    self.titles.append(title)
                for title in self.titles:
                    self.mylist.insert(END, title)
                    self.projectTitles.append(title)

    def onClickShowDescriptions(self):
        if self.titleSelection!=None:
            projectName = self.titleSelection
            for project,projectNames,projectIMGsrc in self.tupleListIMG_src:
                if projectName==projectNames:
                    self.projectIMGsrc=projectIMGsrc
            for project, projectNames, projectIMGsummary in self.tupleIMG_summary:
                if projectName == projectNames:
                    self.projectIMGsummary=projectIMGsummary

            self.mylistResults.delete(0, END)
            div=70
            index=0
            text=self.projectIMGsummary
            for a in range(len(text) / div):
                empty = ""
                for i in range(div):
                    empty += text[i + (a * div)]
                    index+=1
                self.mylistResults.insert(END, empty)
            if index!=len(text):
                leftOne=text[index-1:len(text)-1]
                self.mylistResults.insert(END, leftOne)

            urlListed=self.url.split("/")
            new_urlListed=[]
            for i in range(3):
                new_urlListed.append(urlListed[i])
            new_url="/".join(new_urlListed)
            new_url=new_url+self.projectIMGsrc

            self.image.destroy()

            url = new_url
            image_bytes = urlopen(url).read()
            # internal data file
            data_stream = io.BytesIO(image_bytes)
            # open as a PIL image object
            pil_image = Image.open(data_stream)
            tk_image = ImageTk.PhotoImage(pil_image)
            self.image = Canvas(self.results, bg='white')
            self.image.pack(side=RIGHT, fill='both', expand='yes', padx=60, pady=10)
            # put the image on the canvas with
            # create_image(xpos, ypos, image, anchor)
            self.image.create_image(10, 10, image=tk_image)
            print new_url


def main():
    root = Tk()
    root.wm_title("SEHIR Research Projects Analyzer")
    root.geometry("1010x620+150+30")
    app = SEHIRResearchProjectsAnalyzer(root)
    root.mainloop()

if __name__ == '__main__':
    main()