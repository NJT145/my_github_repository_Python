__author__ = 'jarethmoyo'
import Tkinter as tk
import ttk
from urllib2 import urlopen
import io
from tkMessageBox import *
# allows for image formats other than gif
# source in adding images
# https://www.daniweb.com/programming/software-development/code/440946/display-an-image-from-a-url-tkinter-python
import base64
from PIL import Image, ImageTk
from bs4 import BeautifulSoup

"""Create a project blueprint that holds all the details about a project. To do this we have to use a class
   that holds this information. Essentially each project is an object"""


class Project(object):
    def __init__(self):
        self.proj_title=None
        self.full_date=None  # will be disregarded later
        self.start_date=None
        self.end_date=None
        self.funding_institution=None
        self.principle_investigator=None
        self.proj_details=None
        self.image_url=None

    def is_year(self, year):
        """This method performs the comparison between the queried year and the start and end year
            of the project"""
        if year=="All Years":
            return True
        else:
            return self.start_date <= int(year) <= self.end_date

    def is_investigator(self, target):
        """This method performs the comparison between the queried investigator and the actual investigator
           for the project"""
        if target=="All Investigators":
            return True
        else:
            return target==self.principle_investigator

    def is_institution(self, target):
        """This method performs the comparison between the queried institution and the actual institution
           for the project"""
        if target=="All Institutions":
            return True
        else:
            return target==self.funding_institution


class FetchProjects(object):
    def __init__(self, link):
        self.link=link
        self.all_projects=[]  # we will store our project objects in this list
        self.proj_to_disp=[]  # the projects we ought to display

    def fetch(self):
        """This method fetches all data  from the web and populates the list self.all_projects
           with information about each project"""
        content=urlopen(self.link)
        soup=BeautifulSoup(content.read(),'html.parser')
        # now to fetch all the data that we need
        all_data=soup.findAll("li",{"class":"list-group-item"})  # all the data we need
        for proj in all_data:
            p=Project()
            p.proj_title=proj.find("h4").string.strip()
            p.image_url= proj.find("img").get("src")
            p_details=proj.findAll("p")
            p_details=map(lambda x: x.text.strip(), p_details)
            p.full_date= p_details[0]  # get the full date
            p.funding_institution= p_details[1]  # get the funding institution
            p.principle_investigator= p_details[2]  # get the principle investigator
            p.proj_details=p_details[4]  # get the project details
            self.all_projects.append(p)
        # see below for method descriptions
        self.format_date()
        self.format_investigators()
        self.format_institutions()

    def format_date(self):
        """This method formats the date in the appropriate format that can be used for comparison later on"""
        for p in self.all_projects:
            date=p.full_date.split("-")
            start_date= date[0].strip()
            end_date= date[1].strip()
            p.start_date=int(start_date[-4:len(start_date)])  # just get the year
            p.end_date=int(end_date[-4:len(end_date)])  # again, just get the year

    def format_investigators(self):
        """This method formats the principle investigators, and removes all the noise from the data fetched
           earlier with the fetch method"""
        for p in self.all_projects:
            p.principle_investigator=p.principle_investigator.split("\n")[-1].strip()

    def format_institutions(self):
        """This method formats the funding institutions, and removes all the noise from the data fetched
           earlier with the fetch method"""
        for p in self.all_projects:
            p.funding_institution=p.funding_institution.split("\n")[-1].strip()

# test=FetchProjects("http://cs.sehir.edu.tr/en/research/")
# test.fetch()
# test.format_institutions()
# http://cs.sehir.edu.tr/en/research/

class App(FetchProjects):
    def __init__(self, master):
        super(App, self).__init__("")
        master.title("SEHIR Research Projects Analyzer")
        # defining our frames
        # first define top level frames
        top_frame=tk.Frame(master)
        top_frame.pack()
        nw_widgets_frame=tk.Frame(master)
        nw_widgets_frame.pack(anchor=tk.W)
        ne_widgets_frame=tk.Frame(nw_widgets_frame)
        ne_widgets_frame.pack(side=tk.RIGHT)
        mid_frame=tk.Frame(master)
        mid_frame.pack(anchor=tk.W)
        filter_frame=tk.Frame(master)
        filter_frame.pack(anchor=tk.W)
        filter_subframe=tk.Frame(filter_frame)
        filter_subframe.pack(side=tk.RIGHT)
        list_box_frame=tk.Frame(filter_subframe)
        list_box_frame.pack(side=tk.RIGHT)
        lower_mid_frame=tk.Frame(master)
        lower_mid_frame.pack(anchor=tk.W)
        skip_frame=tk.Frame(master)
        skip_frame.pack()
        bottom_frame=tk.Frame(master)
        bottom_frame.pack(anchor=tk.E)

        # top labels definition
        tl_text="SEHIR Research Projects Analyzer - CS Edition"
        top_label=tk.Label(top_frame, text=tl_text, font="Times 23 bold", bg="blue",fg="white",width=55)
        top_label.pack()
        url_label=tk.Label(nw_widgets_frame, text="Please provide a url:", font="Helvetica 15")
        url_label.pack(anchor=tk.W,padx=10,pady=5)
        self.url_box=tk.Text(nw_widgets_frame, width=50, height=1,font="Verdana 13", bg='yellow')
        self.url_box.pack(padx=12,pady=(5,5))
        self.url_box.insert(tk.END, "http://cs.sehir.edu.tr/en/research/")
        self.download_button=tk.Button(ne_widgets_frame, text="Fetch Research Projects", width=20,
                                  font="Verdana 11 bold", fg="blue", command=self.fetch_projects)
        self.download_button.pack(pady=5,padx=(60,0))
        skip_widget=tk.Label(mid_frame, text="."*330)
        skip_widget.pack()
        # now defining middle level widgets
        filter_label=tk.Label(mid_frame, text="Filter Research Projects By:"+" "*70+"Pick a Project:",
                              font="Helvetica 15 bold")
        filter_label.pack(anchor=tk.W,padx=10)

        year_label=tk.Label(filter_frame, text="Year:",font="Verdana 13", fg="darkblue")
        year_label.pack(anchor=tk.W,pady=(20,0),padx=10)
        principal_label=tk.Label(filter_frame, text="Principal Investigator:", font="Verdana 13", fg="darkblue")
        principal_label.pack(anchor=tk.W,padx=10,pady=3)
        funding_label=tk.Label(filter_frame, text="Funding Institution:", font="Verdana 13", fg="darkblue")
        funding_label.pack(anchor=tk.W, padx=10,pady=3)

        # filter by year
        self.year_box_value=tk.StringVar()
        self.year_box=ttk.Combobox(filter_subframe, state="readonly", textvariable=self.year_box_value,width=30)
        self.year_box.bind("<<ComboboxSelected>>")
        self.year_box.pack(anchor=tk.W, padx=(100,0), pady=(25,0))

        # filter by principal investigator
        self.p_box_value=tk.StringVar()
        self.p_box=ttk.Combobox(filter_subframe, state="readonly", textvariable=self.p_box_value,width=30)
        self.p_box.bind("<<ComboboxSelected>>")
        self.p_box.pack(anchor=tk.W, padx=(100,0), pady=(10,0))

        # filter by funding institution
        self.f_box_value=tk.StringVar()
        self.f_box=ttk.Combobox(filter_subframe, state="readonly", textvariable=self.f_box_value,width=30)
        self.f_box.bind("<<ComboboxSelected>>")
        self.f_box.pack(anchor=tk.W, padx=(100,0), pady=(10,0))

        # mid frame list box
        self.view_box=tk.Listbox(list_box_frame,height=7, width=70,font="Times 10")
        scroll_0=ttk.Scrollbar(list_box_frame,command=self.view_box.yview)
        scroll_0.pack(side=tk.RIGHT,fill=tk.Y)
        self.view_box.config(yscrollcommand=scroll_0.set)
        self.view_box.pack(side=tk.LEFT, padx=(30,0),pady=5)

        disp_button=tk.Button(lower_mid_frame, text="Display Project Titles",
                              font="Times 12 bold", width=25,fg="darkgreen", command=self.display_titles)
        disp_button.pack(side=tk.LEFT,anchor=tk.W,padx=10, pady=5)
        show_button=tk.Button(lower_mid_frame,text="Show Description",
                              font="Times 12 bold", width=20, fg="darkgreen", command=self.show_details)
        show_button.pack(anchor=tk.E, pady=5,padx=(520,0))

        skip_widget2=tk.Label(skip_frame, text="."*330)
        skip_widget2.pack()

        proj_des=tk.Label(skip_frame, text="Project Description:", font="Helvetica 15 ")
        proj_des.pack(anchor=tk.E, padx=180)

        self.proj_result_box=tk.Text(bottom_frame, width=60,height=10, font="Verdana 10", fg="darkblue")
        scroll_1=ttk.Scrollbar(bottom_frame,command=self.proj_result_box.yview)
        scroll_1.pack(side=tk.RIGHT,fill=tk.Y)
        self.proj_result_box.config(yscrollcommand=scroll_1.set)
        self.proj_result_box.pack(side=tk.RIGHT,padx=0,pady=10)

        self.image=tk.Label(bottom_frame)
        self.image.pack(pady=10, padx=10)

    def fetch_projects(self):
        """command for the download button to fetch projects from the site"""
        self.link=self.url_box.get("1.0","end-1c")
        self.fetch()
        self.populate_investigators()
        self.populate_years()
        self.populate_institutions()

    def populate_investigators(self):
        # populating the principle investigators combobox
        investigators=[]  # we will later sort these investigators by last name
        for p in self.all_projects:
            investigators.append(p.principle_investigator)
        # now to sort the investigators by last name, call the method that does it
        investigators=list(set(investigators))  # use set to remove duplicates
        self.sort_investigators(investigators)
        self.p_box["values"]=["All Investigators"]+investigators
        self.p_box.current(0)

    def populate_years(self):
        # populating the years combobox
        years=[]
        for p in self.all_projects:
            years.append(p.start_date)
            years.append(p.end_date)
        years=list(set(years))
        years.sort()
        self.year_box["values"]=["All Years"]+years
        self.year_box.current(0)

    def populate_institutions(self):
        # populating the institutions combobox
        institutions=[]
        for p in self.all_projects:
            institutions.append(p.funding_institution)
        institutions=list(set(institutions))
        institutions.sort()
        self.f_box["values"]=["All Institutions"]+institutions
        self.f_box.current(0)

    def sort_investigators(self, array):
        """This method sorts all the investigators by last name
           Input: Array of raw investigators
           Action: Sorted array of investigators"""
        array.sort(key=lambda x: x.split()[-1])

    def display_titles(self):
        """This method filters out the projects titles we wish to get rid of"""
        self.view_box.delete(0, tk.END)
        s_year = self.year_box.get()  # selected year
        s_inv = self.p_box.get()  # selected investigator
        s_inst = self.f_box.get()  # selected institution
        for proj in self.all_projects:
            if proj.is_year(s_year) and proj.is_investigator(s_inv) and proj.is_institution(s_inst):
                self.proj_to_disp.append(proj)
                self.view_box.insert(tk.END,proj.proj_title)
        return

    def show_details(self):
        """This project shows the description and fetches the image of currently selected project"""
        try:
            self.proj_result_box.delete("1.0","end-1c")
            sel_proj_title=self.view_box.get(self.view_box.curselection())  # currently selected project
            width, height=460, 150  # width and height of label to display
            for proj in self.proj_to_disp:
                if proj.proj_title == sel_proj_title:
                    self.proj_result_box.insert(tk.END, proj.proj_details)
                    url_sub1= self.link.split("//")
                    url_sub2=url_sub1[1].split("/")[0]
                    url=url_sub1[0]+"//"+url_sub2
                    url=url+proj.image_url
                    image_byt = urlopen(url).read()
                    data_stream = io.BytesIO(image_byt)
                    pil_image = Image.open(data_stream)
                    self.photo_res = pil_image.resize((width,height), Image.ANTIALIAS)
                    self.photo = ImageTk.PhotoImage(self.photo_res)
                    self.image.configure(image=self.photo)
                    break
            return
        except:
            showerror("Operational Error", message="Please select a project to view")














root=tk.Tk()
root.resizable(0,0)
app=App(root)
root.mainloop()
