# -*- coding: utf-8 -*-

"""
ENGR 212 Spring 2016 Mini Project 1 Solution File
Doğukan Kotan <dogukankotan@std.sehir.edu.tr>

Starting '_<method_name>' functions are related to GUI.
"""
from tkFileDialog import askopenfilename  # Python 2
from Tkinter import *  # Python 2
from tkMessageBox import showwarning, showerror  # Python 2
import ttk
import anydbm
import pickle
import xlrd
import os


class CurriculumViewer(Frame):
    def __init__(self, master):
        """

        :param master: initial frame object of tkinter
        :return: None

        Reads selected curriculum's semester courses and prints out. If it has already saved on database,
        then prints out without giving an excel file.
        """

        """ Variables """
        Frame.__init__(self, master)
        self.root = master
        self.root.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.title = 'Curriculum Viewer v1.0'
        options = ["Semester %d" % i for i in range(1, 9)]
        self.dropdown_var = StringVar(master)
        self.dropdown_var.set(options[0])
        self.db = None
        self.is_cs = False
        self.is_ee = False
        self.is_ie = False

        """ Widgets """
        # Frames
        self.content_frame = Frame(self.root, width=200, height=100)
        self.top_bar_frame = Frame(self.root)
        self.print_area_frame = Frame(self.root)

        # Labels
        self.message_box_label = Label(self.top_bar_frame, text=self.title, height=2, fg='white',
                                       font=("Helvetica", 22))
        self.file_browse_label = Label(self.content_frame, text="Please select curriculum excel file:",
                                       height=1, fg='black',
                                       font=("Helvetica", 12))
        self.dropdown_label = Label(self.content_frame, text="Please select semester that you want to print:",
                                    height=1, fg='black',
                                    font=("Helvetica", 12))

        # Buttons
        self.open_excel_button = Button(self.content_frame, text='Browse', command=self._on_click_browse)
        self.do_button = Button(self.content_frame, text='Display', command=self._on_click_print)

        # Combobox
        self.dropdown = ttk.Combobox(self.content_frame, textvariable=self.dropdown_var, values=options,
                                     state="readonly")

        self._customize()  # calling custom initialize()

    def _customize(self):
        """

        :return: None

        Our custom initialize methods here.
        """
        self.content_frame.grid(row=1, column=0, pady=10, sticky=E)
        self.content_frame.columnconfigure(0, weight=1)
        self.top_bar_frame.grid(row=0, column=0, sticky=W + E)
        self.top_bar_frame.columnconfigure(0, weight=1)

        # Labels
        self.message_box_label.grid(row=0, column=0, columnspan=1, sticky=W + E)
        self.message_box_label.config(background='green')
        self.dropdown_label.grid(row=4, column=0, sticky=E)
        self.file_browse_label.grid(row=3, column=0, sticky=E)

        # Buttons
        self.open_excel_button.grid(row=3, column=2, padx=80)
        self.do_button.grid(row=5, column=2, ipadx=20, padx=80)

        # Dropdown
        self.dropdown.grid(row=4, column=2)

    def _on_click_browse(self):
        """

        :return: None

        Open excel file then reads and saves on database.
        """
        filename = askopenfilename(parent=self.root, title='Choose a file',
                                   initialdir=os.getcwd(), filetypes=[('Excel Files', ('.xlsx', '.xls'))]
                                   )
        if filename:
            try:
                workbook = xlrd.open_workbook(filename)
            except xlrd.XLRDError:
                showerror('Warning', 'Unsupported format detected. Please give only xls and xlsx file!')
            else:
                d = self.read_excel(workbook)
                self.save_to_db(d)

    def _on_click_print(self):
        """

        :return: None

        Reads data from database and prints out each courses on print_area_frame as label.
        If there is no data, shows warning to user.
        """
        try:
            d = self.load_from_db()
        except KeyError:
            showwarning('Warning', 'There is no data in the database. You should upload the excel file first.')
        else:
            semester = int(self.dropdown.get().split()[1])
            self.print_area_frame.grid(row=2, column=0)
            self.print_area_frame.columnconfigure(0, weight=1)
            self.root.geometry('{}x{}'.format('600', '450'))
            for widget in self.print_area_frame.winfo_children():
                widget.destroy()
            course_code_label = Label(self.print_area_frame, text="Course Code", height=1, fg='black',
                                      font=("Helvetica", 14))
            course_title_label = Label(self.print_area_frame, text="Course Title", height=1, fg='black',
                                       font=("Helvetica", 14))
            course_credit_label = Label(self.print_area_frame, text="Credit", height=1, fg='black',
                                        font=("Helvetica", 14))
            course_code_label.grid(row=0, column=0, columnspan=1, sticky=W, )
            course_title_label.grid(row=0, column=1, columnspan=1, sticky=W, padx=140)
            course_credit_label.grid(row=0, column=2, columnspan=1, sticky=E, padx=20)
            for index, course in enumerate(d[semester]):
                Label(self.print_area_frame, text=course['course_code'], height=1, fg='red',
                      font=("Helvetica", 12)).grid(row=index + 1, column=0, columnspan=1, sticky=W)
                Label(self.print_area_frame, text=course['course_title'], height=1, fg='red',
                      font=("Helvetica", 12)).grid(row=index + 1, column=1, columnspan=1, sticky=W)
                Label(self.print_area_frame, text=course['course_credit'], height=1, fg='red',
                      font=("Helvetica", 12)).grid(row=index + 1, column=2, columnspan=1, sticky=E, padx=20)

    def read_excel(self, workbook):
        """

        :param workbook: opened excel file (xlrd object)
        :return: dictionary represents as data

        This method reads excel file with specific column and row.
        Some rules are applied.
        """
        sheet = workbook.sheet_by_index(0)
        get_result = True
        row_count = 0
        cathe = None
        dicti = dict()
        while get_result:
            try:
                cathe = sheet.cell_value(row_count, 0).split('-')[1].strip().lower()
                get_result = False
            except IndexError:
                row_count += 1
        if 'computer' in cathe:
            self.is_cs = True
            self.is_ee = False
            self.is_ie = False
        elif 'electrical' in cathe:
            self.is_ee = True
            self.is_cs = False
            self.is_ie = False
        elif 'industrial' in cathe:
            self.is_ie = True
            self.is_cs = False
            self.is_ee = False

        for i in range(1, 9):
            col = 0
            if i % 2 == 0:
                col = 8
            dicti.setdefault(i, [])
            for row in range(sheet.nrows):
                if self.formatter(i, row):
                    semester_keeper = dict()
                    if sheet.cell_value(row, col) == '':
                        continue  # get rid of empty rows
                    semester_keeper['course_code'] = sheet.cell_value(row, col)
                    semester_keeper['course_title'] = sheet.cell_value(row, col + 1)
                    semester_keeper['course_prerequisites'] = sheet.cell_value(row, col + 2)
                    semester_keeper['course_credit'] = sheet.cell_value(row, col + 5)
                    semester_keeper['course_ects'] = sheet.cell_value(row, col + 6)
                    dicti[i].append(semester_keeper)
        return dicti

    def formatter(self, semester, row):
        """

        :param semester: integer of semester
        :param row: integer of row
        :return: boolean

        This methods returns True if row is in searched area.
        """
        if semester == 1:
            return 5 < row < 13
        elif semester == 2:
            return 5 < row < 15
        elif semester == 3:
            return 17 < row < 24
        elif semester == 4:
            return 17 < row < 26
        elif semester == 5:
            return 28 < row < 35
        elif semester == 6:
            return 28 < row < 37
        elif semester == 7 or semester == 8:
            if self.is_cs:
                return 40 < row < 46
            elif self.is_ee or self.is_ie:
                return 39 < row < 45
        else:
            return False

    @staticmethod
    def save_to_db(data):
        """

        :param data: database file
        :return: None

        This method saves database file in anydbm file using pickle module.
        """
        db = anydbm.open('curriculum.db', 'c')
        db['saved'] = pickle.dumps(data)
        db.close()

    @staticmethod
    def load_from_db():
        """

        :return: database file

        This method loads string from anydbm file and convert it to python database type.
        """
        db = anydbm.open('curriculum.db', 'c')
        loaded = db['saved']
        db.close()
        return pickle.loads(loaded)


if __name__ == '__main__':
    root = Tk()  # Root frame of Tkinter
    root.resizable(width=FALSE, height=FALSE)  # Prevent all resize actions
    root.title('Curriculum Viewer v1.0')  # Set GUI Title
    root.geometry('{}x{}'.format('600', '190'))  # Set GUI geometry
    app = CurriculumViewer(root)  # Starting our app
    root.mainloop()  # Show GUI to user
