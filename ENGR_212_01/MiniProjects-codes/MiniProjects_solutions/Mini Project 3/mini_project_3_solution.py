# -*- coding: utf-8 -*-

"""
ENGR 212 Spring 2016 Mini Project 3 Solution File
Doğukan Kotan <dogukankotan@std.sehir.edu.tr>

Starting '_<method_name>' functions are related to GUI.
"""
from tkFileDialog import askopenfilename  # Python 2
from Tkinter import *  # Python 2
from tkMessageBox import showerror, showinfo  # Python 2

import clusters


class CourseAnalyzer(Frame):
    def __init__(self, master):
        """

        :param master: initial window object of tkinter
        :return: None

        """
        
        """ Variables """
        Frame.__init__(self, master)
        self.root = master
        self.root.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.path_var = StringVar()
        self.radio_var = IntVar()
        self.path_var.set("Please select a file.")
        self.radio_var.set(1)
        self.selected_distance = clusters.pearson

        # Frames
        self.top_frame = Frame(self.root)
        self.middle_frame = Frame(self.root)
        self.bottom_frame = Frame(self.root, relief=SOLID, bd=2)
        self.middle2_frame = Frame(self.bottom_frame)
        self.area_frame = Frame(self.bottom_frame)

        # Labels
        self.title = Label(self.top_frame, text="COURSE ANALYZER - SEHIR LIMITED EDITION", bg="red", fg="white",
                           font=("Comic Sans", 13), height=2)
        self.upload_label = Label(self.middle_frame, text="Upload a file that contains course descriptions :",
                                  font=("Comic Sans", 12))
        self.selected_label = Label(self.middle_frame, text="Selected File :", font=("Comic Sans", 12))
        self.path_label = Label(self.middle_frame, textvariable=self.path_var, font=("Comic Sans", 10), relief=SOLID,
                                bd=2)
        # self.analyze_label = Label(self.middle_frame, text="Analyze Courses:", font=("Comic Sans", 12))
        self.similarity_label = Label(self.middle2_frame, text="Similarity Measure :", font=("Comic Sans", 10))
        self.group_label = Label(self.middle2_frame, text="Select Course Codes:", font=("Comic Sans", 10))
        # Buttons
        self.browse_button = Button(self.middle_frame, text="Browse", font=("Comic Sans", 10), command=self._do_browse)
        self.show_matrix_button = Button(self.middle2_frame, text="Show Data Matrix", font=("Comic Sans", 10),
                                         command=self._show_matrix)
        self.draw_diagram_button = Button(self.middle2_frame, text="Draw Hierarchical Cluster Diagram",
                                          font=("Comic Sans", 10), command=self._draw_dendogram)
        self.print_diagram_button = Button(self.middle2_frame, text="Print Hierarchical Cluster as Text",
                                           font=("Comic Sans", 10), command=self._print_cluster)

        # Radio
        self.pearson_radio_button = Radiobutton(self.middle2_frame, text="Pearson", font=("Comic Sans", 10), value=1,
                                                variable=self.radio_var, command=self.select_distance)
        self.tanamoto_radio_button = Radiobutton(self.middle2_frame, text="Tanimoto", font=("Comic Sans", 10), value=2,
                                                 variable=self.radio_var, command=self.select_distance)

        # Listbox
        self.listbox = Listbox(self.middle2_frame, height=5, width=15,selectmode='multiple')
        self.listbox.bind_all("<MouseWheel>", self._on_mousewheel)
        self.listbox.bind("<Button-4>", self._on_mousewheel)
        self.listbox.bind("<Button-5>", self._on_mousewheel)

        # Canvas
        self.canvas_area = Canvas(self.area_frame, bg="white", width=800, height=320, scrollregion=(0, 0, 0, 0))
        self.canvas_area.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas_area.bind("<Button-4>", self._on_mousewheel)
        self.canvas_area.bind("<Button-5>", self._on_mousewheel)

        # Scroolbars
        self.hbar = Scrollbar(self.area_frame, orient=HORIZONTAL, command=self.canvas_area.xview)
        self.vbar = Scrollbar(self.area_frame, orient=VERTICAL, command=self.canvas_area.yview)
        self.listhbar = Scrollbar(self.middle2_frame, orient=VERTICAL, command=self.listbox.yview)
        self._customize()

    def _customize(self):
        # Frames
        self.top_frame.grid(row=0, sticky=W + E)
        self.top_frame.columnconfigure(0, weight=1)
        self.middle_frame.grid(row=1, pady=10)
        self.bottom_frame.grid(row=2)
        self.area_frame.grid(row=1, column=0,columnspan=5, sticky=W + E + N + S)
        self.middle2_frame.grid(row=0)

        # Top Frame
        self.title.grid(sticky=W + E)

        # Middle Frame
        self.upload_label.grid(row=0, column=0, sticky=E, columnspan=5)
        self.browse_button.grid(row=0, column=5, sticky=W, padx=70)
        self.selected_label.grid(row=1, column=0, sticky=W)
        self.path_label.grid(row=1, column=1, columnspan=5, sticky=W + E, pady=10)
        # self.analyze_label.grid(row=2, column=0, sticky=W)

        # Middle2 Frame
        self.similarity_label.grid(row=0, rowspan=2, column=0, sticky=E)
        self.pearson_radio_button.grid(row=0, column=1)
        self.tanamoto_radio_button.grid(row=1, column=1)
        # self.show_matrix_button.grid(row=2, column=0, sticky=W, pady=10,padx=10)
        # self.draw_diagram_button.grid(row=2, column=1, sticky=E, pady=10, padx=10)
        # self.print_diagram_button.grid(row=2, column=2, pady=10, padx=10)
        self.show_matrix_button.grid(row=2, column=2, pady=10, padx=10)
        self.draw_diagram_button.grid(row=2, column=0, sticky=W, pady=10,padx=10)
        self.print_diagram_button.grid(row=2, column=1, sticky=E, pady=10, padx=10)

        self.group_label.grid(row=0, column=2, sticky=E)
        self.listbox.grid(row=0, column=3, sticky=E, rowspan=2)
        self.listhbar.grid(row=0, column=4, sticky=N+S+W, rowspan=2)

        # Area Frame
        self.canvas_area.grid(row=0, column=0)
        self.canvas_area.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.hbar.grid(sticky=W + E, row=1)
        self.vbar.grid(sticky=N + S, row=0, column=1)

    def _on_mousewheel(self, event):
        self.canvas_area.yview_scroll(-1 * (event.delta / 120), "units")

    def _show_matrix(self):
        try:
            data = self.create_data(self.path_var.get())
            newdata = {}
            items = map(int,self.listbox.curselection())
            for key in data:
                for item in items:
                    if self.listbox.get(item) == key.split(" ")[0]:
                        newdata[key] = data[key]
            clusters.create_matrix(newdata, outfile='course_matrix.txt')
            self.outfile = 'course_matrix.txt'
            matrix_file = open(self.outfile, "r")
        except IOError:
            showerror("Error", "Please upload data file first!")
        except IndexError:
            showerror("Error", "Please select course code.")
        except ZeroDivisionError:
            showerror("Error", "Please select course code.")
        else:
            if len(newdata) < 1:
                showerror("Error", "Please select course code.")
            else:
                self.print_matrix(matrix_file)

    def _do_browse(self):
        filepath = askopenfilename()
        if filepath:
            self.path_var.set(filepath)
            try:
                self.listbox.delete(0, END)
                data = self.create_data(self.path_var.get())
                keeper = []
                for key in data:
                    if key.split(" ")[0] in keeper:
                        continue
                    keeper.append(key.split(" ")[0])
                keeper.sort()
                for course in keeper:
                    self.listbox.insert(END, course)
            except IndexError:
                showerror("Error", "Unsupported file.")


    def _print_cluster(self):
        try:
            data = self.create_data(self.path_var.get())
            newdata = {}
            items = map(int,self.listbox.curselection())
            for key in data:
                for item in items:
                    if self.listbox.get(item) == key.split(" ")[0]:
                        newdata[key] = data[key]
            clusters.create_matrix(newdata, outfile='course_matrix.txt')
            self.outfile = 'course_matrix.txt'
            clust, courses = self.do_hcluster()
        except IOError:
            showerror("Error", "Please upload data file first!")
        except IndexError:
            showerror("Error", "Please select course code first.")
        except ZeroDivisionError:
            showerror("Error", "Please select course code first.")
        else:
            out = clusters.clust2str(clust, courses)
            self.canvas_area.delete("all")
            self.canvas_area.config(scrollregion=(0, 0, 0, len(out) * 2))
            self.canvas_area.create_text(10, 10, anchor="nw", text=out, font=("Comic Sans", 10))


    def _draw_dendogram(self):
        try:
            data = self.create_data(self.path_var.get())
            newdata = {}
            items = map(int,self.listbox.curselection())
            for key in data:
                for item in items:
                    if self.listbox.get(item) == key.split(" ")[0]:
                        newdata[key] = data[key]
            clusters.create_matrix(newdata, outfile='course_matrix.txt')
            self.outfile = 'course_matrix.txt'
            clust, courses = self.do_hcluster()
        except IOError:
            showerror("Error", "Please upload data file first!")
        except IndexError:
            showerror("Error", "Please select course code first.")
        except ZeroDivisionError:
            showerror("Error", "Please select course code first.")
        else:
            h = clusters.getheight(clust)
            w = self.canvas_area.winfo_height()
            depth = clusters.getdepth(clust)

            self.canvas_area.delete("all")
            # width is fixed, so scale distances accordingly
            scaling = float(w - 150) / (depth +1)

            self.canvas_area.create_line((w, 0, w, h/2), fill="red")

            # Draw the first node
            self.draw_node(clust, (h/2), w, scaling, courses)

            self.canvas_area.config(scrollregion=(-w*h,0, w*h, w))

    def draw_node(self, clust, y, x, scaling, labels):
        if clust.id < 0:
            h1 = clusters.getheight(clust.left) * 70
            h2 = clusters.getheight(clust.right) * 70
            top = x - (h1 + h2) / 2
            bottom = x + (h1 + h2) / 2
            # Line length
            ll = clust.distance * scaling
            # Vertical line from this cluster to children
            self.canvas_area.create_line((top + h1 / 2, y, bottom - h2 / 2, y), fill="red")

            # Horizontal line to left item
            self.canvas_area.create_line((top + h1 / 2, y, top + h1 / 2, y + ll), fill="red")

            # Horizontal line to right item
            self.canvas_area.create_line((bottom - h2 / 2, y, bottom - h2 / 2, y + ll), fill="red")

            # Call the function to draw the left and right nodes
            self.draw_node(clust.left, y + ll, top + h1 / 2, scaling, labels)
            self.draw_node(clust.right, y + ll, bottom - h2 / 2, scaling, labels)
        else:
            # If this is an endpoint, draw the item label
            self.canvas_area.create_text((x - 7, y + 7), text=labels[clust.id], font=("Comic Sans", 8))

    def print_matrix(self, matrix_file):
        out = ""
        for line in matrix_file.readlines():
            out += line + "\n"
        self.canvas_area.delete("all")
        self.canvas_area.config(scrollregion=(0, 0, len(out), len(out) / 12))
        self.canvas_area.create_text(10, 10, anchor="nw", text=out, font=("Comic Sans", 10))


    @staticmethod
    def create_data(path):
        data = {}
        for idx, line in enumerate(file(path)):
            if idx % 2 == 0:
                course = line.strip()
                title = course.split()[0] + " " + course.split()[1]
                continue
            else:
                description = line.strip()
            data[title] = description
        return data

    def select_distance(self):
        getter = self.radio_var.get()
        if getter == 1:
            self.selected_distance = clusters.pearson
        elif getter == 2:
            self.selected_distance = clusters.tanamoto
        else:
            self.selected_distance = clusters.pearson

    def do_hcluster(self):
        courses, words, data = clusters.readfile(self.outfile)
        clust = clusters.hcluster(data, distance=self.selected_distance)
        return clust, courses


if __name__ == '__main__':
    root = Tk()  # Root frame of Tkinter
    root.resizable(width=FALSE, height=FALSE)  # Prevent all resize actions
    root.title('Course Analyzer - Sehir Limited Edition')  # Set GUI Title
    root.geometry('{}x{}+250+0'.format('900', '650'))  # Set GUI geometry
    app = CourseAnalyzer(root)  # Starting our app
    root.mainloop()  # Show GUI to user
