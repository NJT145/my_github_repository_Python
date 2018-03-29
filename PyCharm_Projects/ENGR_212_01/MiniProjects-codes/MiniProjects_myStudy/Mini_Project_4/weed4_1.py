import io
from PIL import Image, ImageTk
# Python2
import Tkinter as tk
from urllib2 import urlopen
root = tk.Tk()
root.title("display a website image")
# a little more than width and height of image
w = 520
h = 320
x = 80
y = 100
# use width x height + x_offset + y_offset (no spaces!)
root.geometry("%dx%d+%d+%d" % (w, h, x, y))
url = "http://cs.sehir.edu.tr/media/img/project/NMR_Structure-Based_Assignments_l7Fvdit.png"
image_bytes = urlopen(url).read()
# internal data file
data_stream = io.BytesIO(image_bytes)
# open as a PIL image object
pil_image = Image.open(data_stream)

tk_image = ImageTk.PhotoImage(pil_image)
cv = tk.Canvas(bg='white')
cv.pack(side='top', fill='both', expand='yes')
# put the image on the canvas with
# create_image(xpos, ypos, image, anchor)
cv.create_image(10, 10, image=tk_image, anchor='nw')
root.mainloop()