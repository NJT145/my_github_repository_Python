from Tkinter import *
class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.pack(fill=BOTH, expand=True)
        self.canvas = Canvas(self, bg='white')
        self.canvas.pack(fill=BOTH, expand=True)

def main():
    root = Tk()
    root.geometry("600x400+200+200")
    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()