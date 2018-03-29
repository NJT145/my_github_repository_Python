"""
My references:
* in order to open and use a photo image, i used infos in this :
        #http://effbot.org/tkinterbook/photoimage.htm
* in order to build my color chooser, i used example as a reference from :
        #http://knowpapa.com/cchoser/
        #http://www.java2s.com/Tutorial/Python/0360__Tkinker/Colorchooser.htm
* in order to build the Spinbox widget for the thickness setting, i used codes in :
        #http://effbot.org/tkinterbook/spinbox.htm
* i made a review for button widget options from :
        #http://effbot.org/tkinterbook/button.htm
* i made a review for canvas widget options from :
        #http://effbot.org/tkinterbook/canvas.htm
* for adding scroolbars to canvas, i took a look to there :
        #http://effbot.org/zone/tkinter-scrollbar-patterns.htm
*  for the change on mouse cursor according to the chosen tool, i took a look to :
        #http://www.tutorialspoint.com/python/tk_cursors.htm
        #http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/cursors.html
*the rest was mostly referenced from LMS files and from lessons.
"""

from Tkinter import *
import os
from PIL import Image, ImageTk
from tkColorChooser import askcolor

class MyPaint(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.path = None
        self.listItems = ['drag.gif', 'drag.png', 'eraser.gif', 'eraser.png', 'line.gif', 'line.png', 'oval.gif', 'oval.png', 'rectangle.gif', 'rectangle.png']

        self.initUI()

    def initUI(self):
        self.pack(fill=BOTH, expand=True)

        #title line
        var = StringVar()
        title = Label(self, textvariable=var, bg="orange", fg="white", font='Helvetica 20 bold')
        var.set("My Paint")
        title.pack(fill=X)

        # let's check if all items needed are there
        self.checkItems()

        # let's get items from file
        if self.path!=None:
            self.getItems()

        #
        toolbar = Frame(self)

        self.ClickedRectangle = True
        self.rectangleButton = Button(toolbar, command=self.OnClickRectangle)
        self.rectangleButton.config(relief=SUNKEN)
        if self.path != None:
            image1=self.rectangle_gif
            self.rectangleButton.config(image=image1)
        else:
            self.rectangleButton.config(text="rectangle\nClicked")
        self.rectangleButton.pack(side=LEFT, padx=2)

        self.ClickedOval = False
        self.ovalButton = Button(toolbar, command=self.OnClickOval)
        self.ovalButton.config(relief=RAISED)
        if self.path != None:
            image2 = self.oval_png
            self.ovalButton.config(image=image2)
        else:
            self.ovalButton.config(text="circle\nClicked")
        self.ovalButton.pack(side=LEFT, padx=2)

        self.ClickedLine = False
        self.lineButton = Button(toolbar, command=self.OnClickLine)
        self.lineButton.config(relief=RAISED)
        if self.path != None:
            image3 = self.line_png
            self.lineButton.config(image=image3)
        else:
            self.lineButton.config(text="line\nClicked")
        self.lineButton.pack(side=LEFT, padx=2)

        self.ClickedDrag = False
        self.dragButton = Button(toolbar, command=self.OnClickDrag)
        self.dragButton.config(relief=RAISED)
        if self.path != None:
            image4 = self.drag_png
            self.dragButton.config(image=image4)
        else:
            self.dragButton.config(text="drag\nNotClicked")
        self.dragButton.pack(side=LEFT, padx=2)

        self.ClickedEraser = False
        self.eraserButton = Button(toolbar, command=self.OnClickEraser)
        self.eraserButton.config(relief=RAISED)
        if self.path != None:
            image5 = self.eraser_png
            self.eraserButton.config(image=image5)
        else:
            self.eraserButton.config(text="eraser\nNotClicked")
        self.eraserButton.pack(side=LEFT, padx=2)

        Label(toolbar, text=(6*" ")+"Fill Color:", font='Helvetica 10 bold').pack(side=LEFT)
        self.fillColor = "#ff0000"
        self.FillColorButton = Button(toolbar, text=(" "*8), bg="#ff0000", relief=FLAT, command=self.setFillColor)
        self.FillColorButton.pack(side=LEFT)
        Label(toolbar, text=(3*" ") + "Border Color:", font='Helvetica 10 bold').pack(side=LEFT)
        self.borderColor = "#000000"
        self.BorderColorButton = Button(toolbar, text=(" "*8), bg="#000000", relief=FLAT, command=self.setBorderColor)
        self.BorderColorButton.pack(side=LEFT)
        Label(toolbar, text=(3*" ") + "Weight:", font='Helvetica 10 bold').pack(side=LEFT)

        self.weightSpinBox = Spinbox(toolbar, from_=1, to=999, increment=1, width=3)
        self.weightSpinBox.pack(side=LEFT)
        toolbar.pack()

        #
        canvasFrameWithScroolbars = Frame(self)
        xscrollbar = Scrollbar(canvasFrameWithScroolbars, orient=HORIZONTAL)
        canvasFrameWithScroolbarY =Frame(canvasFrameWithScroolbars)
        yscrollbar = Scrollbar(canvasFrameWithScroolbarY)
        self.canvas = Canvas(canvasFrameWithScroolbarY, bg='white', scrollregion=(0, 0, 1000, 1000), xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
        xscrollbar.config(command=self.canvas.xview)
        yscrollbar.config(command=self.canvas.yview)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        yscrollbar.pack(side=LEFT, fill=Y)
        canvasFrameWithScroolbarY.pack(fill=BOTH, expand=True)
        xscrollbar.pack(fill=X)
        canvasFrameWithScroolbars.pack(padx=30, pady=10, fill=BOTH, expand=True)

        # by default, rectangle is selected. so, we need to bind its functions.
        self.canvas.bind('<ButtonPress-1>', self.canvasSelect_rectangle)
        self.canvas.bind('<B1-Motion>', self.canvasDrag_rectangle)
        self.drawingRectangle = False
        self.canvas.config(cursor="tcross")

    # this function checks if the directory 'assets' containing icon images of buttons exists in current directory
    def checkItems(self):
        # get current directory as cwd
        cwd = os.getcwd()
        # check if our directory named 'assets' exists in our cwd
        if os.path.exists('assets') == True:
            for name in os.listdir(cwd):
                if 'assets' == name:
                    path = os.path.join(cwd, 'assets')
                    # check if 'assets' is a file
                    if os.path.isdir(path) == True:
                        listItems = os.listdir(path)
                        listItems.sort()
                        if listItems == self.listItems:
                            self.path = path

    def getIconImage(self, index):
        path = os.path.join(self.path, self.listItems[index])
        image = Image.open(path)
        photo = ImageTk.PhotoImage(image)
        return photo

    def getItems(self):
        self.drag_gif = self.getIconImage(0)
        self.drag_png = self.getIconImage(1)
        self.eraser_gif = self.getIconImage(2)
        self.eraser_png = self.getIconImage(3)
        self.line_gif = self.getIconImage(4)
        self.line_png = self.getIconImage(5)
        self.oval_gif = self.getIconImage(6)
        self.oval_png = self.getIconImage(7)
        self.rectangle_gif = self.getIconImage(8)
        self.rectangle_png = self.getIconImage(9)

    def OnClickRectangle(self):
        if self.ClickedRectangle == True:
            if self.path != None:
                image1 = self.rectangle_png
                self.rectangleButton.config(image=image1)
            else:
                self.rectangleButton.config(text="rectangle\nNotClicked")
            self.rectangleButton.config(relief=RAISED)
            self.ClickedRectangle = False
            self.canvas.config(cursor="arrow")
        else:
            if self.path != None:
                image1 = self.rectangle_gif
                self.rectangleButton.config(image=image1)
                image2 = self.oval_png
                self.ovalButton.config(image=image2)
                image3 = self.line_png
                self.lineButton.config(image=image3)
                image4 = self.drag_png
                self.dragButton.config(image=image4)
                image5 = self.eraser_png
                self.eraserButton.config(image=image5)
            else:
                self.rectangleButton.config(text="rectangle\nClicked")
                self.ovalButton.config(text="oval\nNotClicked")
                self.lineButton.config(text="line\nNotClicked")
                self.dragButton.config(text="drag\nNotClicked")
                self.eraserButton.config(text="eraser\nNotClicked")

            self.rectangleButton.config(relief=SUNKEN)
            self.ovalButton.config(relief=RAISED)
            self.lineButton.config(relief=RAISED)
            self.dragButton.config(relief=RAISED)
            self.eraserButton.config(relief=RAISED)

            self.ClickedRectangle = True
            self.ClickedOval = False
            self.ClickedLine = False
            self.ClickedDrag = False
            self.ClickedEraser = False

            self.canvas.bind('<ButtonPress-1>', self.canvasSelect_rectangle)
            self.canvas.bind('<B1-Motion>', self.canvasDrag_rectangle)
            self.canvas.config(cursor="tcross")

    def OnClickOval(self):
        if self.ClickedOval == True:
            if self.path != None:
                image2 = self.oval_png
                self.ovalButton.config(image=image2)
            else:
                self.ovalButton.config(text="oval\nNotClicked")
            self.ovalButton.config(relief=RAISED)
            self.ClickedOval = False
            self.canvas.config(cursor="arrow")
        else:
            if self.path != None:
                image1 = self.rectangle_png
                self.rectangleButton.config(image=image1)
                image2 = self.oval_gif
                self.ovalButton.config(image=image2)
                image3 = self.line_png
                self.lineButton.config(image=image3)
                image4 = self.drag_png
                self.dragButton.config(image=image4)
                image5 = self.eraser_png
                self.eraserButton.config(image=image5)
            else:
                self.rectangleButton.config(text="rectangle\nNotClicked")
                self.ovalButton.config(text="oval\nClicked")
                self.lineButton.config(text="line\nNotClicked")
                self.dragButton.config(text="drag\nNotClicked")
                self.eraserButton.config(text="eraser\nNotClicked")

            self.rectangleButton.config(relief=RAISED)
            self.ovalButton.config(relief=SUNKEN)
            self.lineButton.config(relief=RAISED)
            self.dragButton.config(relief=RAISED)
            self.eraserButton.config(relief=RAISED)

            self.ClickedRectangle = False
            self.ClickedOval = True
            self.ClickedLine = False
            self.ClickedDrag = False
            self.ClickedEraser = False

            self.canvas.bind('<ButtonPress-1>', self.canvasSelect_oval)
            self.canvas.bind('<B1-Motion>', self.canvasDrag_oval)
            self.canvas.config(cursor="tcross")

    def OnClickLine(self):
        if self.ClickedLine == True:
            if self.path != None:
                image3 = self.line_png
                self.lineButton.config(image=image3)
            else:
                self.lineButton.config(text="line\nNotClicked")
            self.lineButton.config(relief=RAISED)
            self.ClickedLine = False
            self.canvas.config(cursor="arrow")
        else:
            if self.path != None:
                image1 = self.rectangle_png
                self.rectangleButton.config(image=image1)
                image2 = self.oval_png
                self.ovalButton.config(image=image2)
                image3 = self.line_gif
                self.lineButton.config(image=image3)
                image4 = self.drag_png
                self.dragButton.config(image=image4)
                image5 = self.eraser_png
                self.eraserButton.config(image=image5)
            else:
                self.rectangleButton.config(text="rectangle\nNotClicked")
                self.ovalButton.config(text="oval\nNotClicked")
                self.lineButton.config(text="line\nClicked")
                self.dragButton.config(text="drag\nNotClicked")
                self.eraserButton.config(text="eraser\nNotClicked")

            self.rectangleButton.config(relief=RAISED)
            self.ovalButton.config(relief=RAISED)
            self.lineButton.config(relief=SUNKEN)
            self.dragButton.config(relief=RAISED)
            self.eraserButton.config(relief=RAISED)

            self.ClickedRectangle = False
            self.ClickedOval = False
            self.ClickedLine = True
            self.ClickedDrag = False
            self.ClickedEraser = False

            self.canvas.bind('<ButtonPress-1>', self.canvasSelect_line)
            self.canvas.bind('<B1-Motion>', self.canvasDrag_line)
            self.canvas.config(cursor="tcross")

    def OnClickDrag(self):
        if self.ClickedDrag == True:
            if self.path != None:
                image4 = self.drag_png
                self.dragButton.config(image=image4)
            else:
                self.dragButton.config(text="drag\nNotClicked")
            self.dragButton.config(relief=RAISED)
            self.ClickedDrag = False
            self.canvas.config(cursor="arrow")
        else:
            if self.path != None:
                image1 = self.rectangle_png
                self.rectangleButton.config(image=image1)
                image2 = self.oval_png
                self.ovalButton.config(image=image2)
                image3 = self.line_png
                self.lineButton.config(image=image3)
                image4 = self.drag_gif
                self.dragButton.config(image=image4)
                image5 = self.eraser_png
                self.eraserButton.config(image=image5)
            else:
                self.rectangleButton.config(text="rectangle\nNotClicked")
                self.ovalButton.config(text="oval\nNotClicked")
                self.lineButton.config(text="line\nNotClicked")
                self.dragButton.config(text="drag\nClicked")
                self.eraserButton.config(text="eraser\nNotClicked")

            self.rectangleButton.config(relief=RAISED)
            self.ovalButton.config(relief=RAISED)
            self.lineButton.config(relief=RAISED)
            self.dragButton.config(relief=SUNKEN)
            self.eraserButton.config(relief=RAISED)

            self.ClickedRectangle = False
            self.ClickedOval = False
            self.ClickedLine = False
            self.ClickedDrag = True
            self.ClickedEraser = False

            self.canvas.bind('<ButtonPress-1>', self.itemSelect)
            self.canvas.bind('<B1-Motion>', self.itemDrag)
            self.canvas.config(cursor="hand2")

    def OnClickEraser(self):
        if self.ClickedEraser == True:
            if self.path != None:
                image5 = self.eraser_png
                self.eraserButton.config(image=image5)
            else:
                self.eraserButton.config(text="eraser\nNotClicked")
            self.eraserButton.config(relief=RAISED)
            self.ClickedEraser = False
            self.canvas.config(cursor="arrow")
        else:
            if self.path != None:
                image1 = self.rectangle_png
                self.rectangleButton.config(image=image1)
                image2 = self.oval_png
                self.ovalButton.config(image=image2)
                image3 = self.line_png
                self.lineButton.config(image=image3)
                image4 = self.drag_png
                self.dragButton.config(image=image4)
                image5 = self.eraser_gif
                self.eraserButton.config(image=image5)
            else:
                self.rectangleButton.config(text="rectangle\nNotClicked")
                self.ovalButton.config(text="oval\nNotClicked")
                self.lineButton.config(text="line\nNotClicked")
                self.dragButton.config(text="drag\nNotClicked")
                self.eraserButton.config(text="eraser\nClicked")

            self.rectangleButton.config(relief=RAISED)
            self.ovalButton.config(relief=RAISED)
            self.lineButton.config(relief=RAISED)
            self.dragButton.config(relief=RAISED)
            self.eraserButton.config(relief=SUNKEN)

            self.ClickedRectangle = False
            self.ClickedOval = False
            self.ClickedLine = False
            self.ClickedDrag = False
            self.ClickedEraser = True

            self.canvas.bind('<ButtonPress-1>', self.itemEraser)
            self.canvas.config(cursor="X_cursor")

    def setFillColor(self):
        (triple, hexstr) = askcolor(title="My Color Chooser")
        if hexstr:
            self.FillColorButton.config(bg=hexstr)
            self.fillColor = hexstr

    def setBorderColor(self):
        (triple, hexstr) = askcolor(title="My Color Chooser")
        if hexstr:
            self.BorderColorButton.config(bg=hexstr)
            self.borderColor = hexstr

    def canvasSelect_rectangle(self, event):
        self.startx, self.starty = event.x, event.y
        weight = int(self.weightSpinBox.get())
        item = self.canvas.create_rectangle(self.startx, self.starty, event.x, event.y, fill=self.fillColor,
                                            outline=self.borderColor, width=weight)
        self.rectangle = item

    def canvasDrag_rectangle(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        self.canvas.coords(self.rectangle, self.startx, self.starty, event.x, event.y)

    def canvasSelect_oval(self, event):
        self.drawingCircle = True
        self.startx, self.starty = event.x, event.y
        weight = int(self.weightSpinBox.get())
        item = self.canvas.create_oval(self.startx, self.starty, event.x, event.y, fill=self.fillColor,
                                       outline=self.borderColor, width=weight)
        self.circle = item

    def canvasDrag_oval(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        self.canvas.coords(self.circle, self.startx, self.starty, event.x, event.y)

    def canvasSelect_line(self, event):
        self.startx, self.starty = event.x, event.y
        weight = int(self.weightSpinBox.get())
        item = self.canvas.create_line(self.startx, self.starty, event.x, event.y, fill=self.fillColor, width=weight)
        self.line = item

    def canvasDrag_line(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        self.canvas.coords(self.line, self.startx, self.starty, event.x, event.y)

    def itemSelect(self, event):
        """Selects this item for dragging or erasing."""
        self.dragx, self.dragy = event.x, event.y
        self.dragitem = self.canvas.find_closest(event.x, event.y)

    def itemDrag(self, event):
        """Move this item using the pixel coordinates in the event object."""
        # see how far we have moved
        dx = event.x - self.dragx
        dy = event.y - self.dragy
        self.canvas.move(self.dragitem, dx, dy)
        self.dragx, self.dragy = event.x, event.y

    def itemEraser(self, event):
        """Eraser function for selected item."""
        self.eraseritem = self.canvas.find_closest(event.x, event.y)
        self.canvas.delete(self.eraseritem)

def main():
    root = Tk()
    root.wm_title("My Paint")
    root.geometry("1010x620+150+30")
    app = MyPaint(root)
    root.mainloop()

if __name__ == '__main__':
    main()
