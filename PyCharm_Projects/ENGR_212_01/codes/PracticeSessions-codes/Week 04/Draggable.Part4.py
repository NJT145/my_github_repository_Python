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

        # Added for Part 4: Create a custom oval with left click and drag
        #  if the clicked location is empty
        self.canvas.bind('<ButtonPress-1>', self.canvasSelect)
        self.canvas.bind('<B1-Motion>', self.canvasDrag)
        self.canvas.bind('<ButtonRelease-1>', self.canvasDrop)
        self.drawingCircle = False

    # Added for Part 3:
    def make_circle(self, event):
        """Makes a circle item at the location of a button press."""
        #pos = ca.canvas_coords([event.x, event.y])
        item = self.canvas.create_oval(event.x, event.y, event.x+10, event.y+10, outline="red",
            fill="red", width=2)

        self.canvas.tag_bind(item, '<ButtonPress-1>', self.itemSelect)
        self.canvas.tag_bind(item, '<B1-Motion>', self.itemDrag)
        self.canvas.tag_bind(item, '<ButtonRelease-1>', self.itemDrop)

    # Added for Part 3:
    def itemSelect(self, event):
        """Selects this item for dragging."""
        self.dragging = True
        self.dragx, self.dragy = event.x, event.y
        self.dragitem = self.canvas.find_closest(event.x, event.y)
        self.canvas.itemconfig(self.dragitem, fill="blue") # change color

    # Added for Part 3:
    def itemDrag(self, event):
        """Move this item using the pixel coordinates in the event object."""
        # see how far we have moved
        if not self.dragging:
            return
        dx = event.x - self.dragx
        dy = event.y - self.dragy
        self.canvas.move(self.dragitem, dx, dy)
        self.dragx, self.dragy = event.x, event.y

    # Added for Part 3:
    def itemDrop(self, event):
        """Drops this item."""
        if not self.dragging:
            return
        self.canvas.itemconfig(self.dragitem, fill="red") # change color
        self.dragging = False

    # Added for Part 4
    def canvasSelect(self, event):
        if self.dragging:
            return
        self.drawingCircle = True
        self.startx, self.starty = event.x, event.y
        item = self.canvas.create_oval(self.startx, self.starty, event.x, event.y, outline="red")

        self.circle = item

    # Added for Part 4
    def canvasDrag(self, event):
        """Move this item using the pixel coordinates in the event object."""
        # see how far we have moved
        if self.drawingCircle:
            item = self.canvas.find_closest(event.x, event.y)
            self.canvas.coords(self.circle, self.startx, self.starty, event.x, event.y)

    # Added for Part 4
    def canvasDrop(self, event):
        """Drops this item."""
        if self.drawingCircle:
            self.drawingCircle = False
            self.canvas.itemconfig(self.circle, fill="red") # change color

def main():
    root = Tk()
    root.geometry("600x400+200+200")
    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()