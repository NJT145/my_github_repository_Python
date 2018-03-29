from Tkinter import *
class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.pack()
        canvas = Canvas(self)
        canvas.create_oval(10, 10, 80, 80, outline="gray",
            fill="gray", width=2)
        canvas.create_oval(110, 10, 210, 80, outline="gray",
            fill="gray", width=2)
        canvas.create_rectangle(230, 10, 290, 60,
            outline="gray", fill="gray", width=2)

        points = [150, 100, 200, 120, 240, 180, 210,
            200, 150, 150, 100, 200]
        canvas.create_polygon(points, outline='gray',
            fill='gray', width=2)
        canvas.pack()

def main():
    root = Tk()
    root.geometry("350x250+300+300")
    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()