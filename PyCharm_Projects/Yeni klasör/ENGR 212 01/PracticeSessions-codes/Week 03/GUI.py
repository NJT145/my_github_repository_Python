__author__ = 'aliuzun'
from Tkinter import *
from ReadWrite import *

class GUI(ReadWrite):

    def __init__(self,root):
        self.root=root
        self.IF()
        self.Settings()

    def IF(self):

        self.Input=Frame(self.root)
        # self.Input.config(background="red")

        #Entry
        self.title_for_path = Label(self.Input,text = "Enter path or file name:",font = "Times 13 bold")

        self.path = Entry(self.Input)

        #dropdown list
        options=["w","r","w+","r+"]
        self.title_combobox=Label(self.Input,text="Mode:",font = "Times 13 bold")
        self.dropdown_variable=StringVar()
        self.dropdown_variable.set(options[0])
        self.option = OptionMenu(self.Input,self.dropdown_variable, *options)

        #Button for Display and Clear and Create
        self.Button_for_display = Button(self.Input,text = """Display""",font = "Times 13 bold",command =self.Display)

        self.Button_for_clear = Button(self.Input,text = """Clear""",font = "Times 13 bold",command = self.Clear)

        self.Button_for_save = Button(self.Input,text = """Create""",font = "Times 13 bold",command = self.Create)

        # # Entry
        self.title_for_input_text = Label(self.Input, text = "Enter text:",font = "Times 13 bold")
        self.text = Text(self.Input, font = "Times 13", height = 20)

    def Settings(self):
        self.title_for_path.grid(row=0,column=0, sticky=E) #
        self.path.grid(row=0,column=1, columnspan = 2, sticky=EW, padx=5) #

        self.title_combobox.grid(row=1,column=0, sticky=E, pady=5)
        self.option.grid(row=1,column=1, columnspan = 2, sticky=W, padx=5, pady=5)

        self.Button_for_display.grid(row=2, column=0, padx=5, pady=5, sticky=E)
        self.Button_for_clear.grid(row=2, column=1, padx=5, pady=5, sticky=W)
        self.Button_for_save.grid(row=2, column=2, padx=5, pady=5, sticky=W)

        self.title_for_input_text.grid(row=3, column=0, sticky=W, pady=5)
        self.text.grid(columnspan=3, sticky=EW, padx=5, pady=5)

        self.Input.pack(fill=BOTH, expand=True) # perfect use case for pack geometry manager

        for i in range(5):
            self.Input.rowconfigure(i, weight=1) # allow resizing with the window

        self.Input.columnconfigure(2, weight=3) # make sure that column 3 is larger than others

    def Display(self):
        try:
            path,mode=self.path.get(),self.dropdown_variable.get()
            text=self.getText(path,mode)
            self.text.insert("1.0",text)
        except IOError:
            print "No file or path selected !!"
            self.text.insert("1.0", "No file or path selected !!")

    def Create(self):
        try:
            path,mode,text=self.path.get(),self.dropdown_variable.get(),self.text.get("1.0",END)
            self.createFile(path,mode,text)
        except IOError:
            self.text.insert("1.0", "No file or path selected !!")


    def Clear(self):
        self.text.delete(1.0,END)



def main():
    root= Tk()
    root.wm_title("File Editor")
    App = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
