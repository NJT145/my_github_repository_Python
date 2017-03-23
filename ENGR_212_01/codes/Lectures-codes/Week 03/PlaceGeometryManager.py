from Tkinter import *
class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.pack(fill=BOTH, expand=1)
        var = StringVar()
        label = Label(self, textvariable=var)
        var.set("Hey!? How are you doing?")
        label.place(relx=0.5, rely=0.5, anchor=NW)
        b = Button(self, width=12, height=12, text = 'hello!')
        b.place( x=10, y=2, anchor=NW)

def main():
    root = Tk()
    root.geometry("250x150+300+300")
    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()