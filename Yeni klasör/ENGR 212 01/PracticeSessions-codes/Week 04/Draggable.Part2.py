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

        # Added for part 2: right click on canvas: draws a red circle of size 10 at clicked location
        self.canvas.bind('<ButtonPress-3>', self.make_circle)

    # Added for part 2
    def make_circle(self, event):
        """Makes a circle item at the location of a button press."""
        #pos = ca.canvas_coords([event.x, event.y])
        item = self.canvas.create_oval(event.x, event.y, event.x+10, event.y+10, outline="red",
            fill="red", width=2)

def main():
    root = Tk()
    root.geometry("600x400+200+200")
    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()