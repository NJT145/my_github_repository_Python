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

        # Added for part 2
        self.canvas.bind('<ButtonPress-3>', self.make_circle)

        # Added for part 3
        self.dragging = False

    # Added for part 2
    def make_circle(self, event):
        """Makes a circle item at the location of a button press."""
        item = self.canvas.create_oval(event.x, event.y, event.x+10, event.y+10, outline="red",
            fill="red", width=2)

        # Added for part 3: drag and drop a circle with left click
        self.canvas.tag_bind(item, '<ButtonPress-1>', self.itemSelect)
        self.canvas.tag_bind(item, '<B1-Motion>', self.itemDrag)
        self.canvas.tag_bind(item, '<ButtonRelease-1>', self.itemDrop)

    # Added for part 3: drag and drop a circle with left click
    def itemSelect(self, event):
        """Selects this item for dragging."""
        self.dragging = True
        self.dragx, self.dragy = event.x, event.y
        self.dragitem = self.canvas.find_closest(event.x, event.y)
        self.canvas.itemconfig(self.dragitem, fill="blue") # change color

    # Added for part 3: drag and drop a circle with left click
    def itemDrag(self, event):
        """Move this item using the pixel coordinates in the event object."""
        # see how far we have moved
        if not self.dragging:
            return
        dx = event.x - self.dragx
        dy = event.y - self.dragy
        self.canvas.move(self.dragitem, dx, dy)
        self.dragx, self.dragy = event.x, event.y

    # Added for part 3: drag and drop a circle with left click
    def itemDrop(self, event):
        """Drops this item."""
        if not self.dragging:
            return
        self.canvas.itemconfig(self.dragitem, fill="red") # change color
        self.dragging = False

def main():
    root = Tk()
    root.geometry("600x400+200+200")
    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()