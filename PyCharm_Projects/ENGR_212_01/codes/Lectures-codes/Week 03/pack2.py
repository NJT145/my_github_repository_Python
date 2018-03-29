from Tkinter import *

root = Tk()

Label(root, text="Red Sun", bg="red", fg="white").pack(fill=BOTH, expand=False)
Label(root, text="Green Grass", bg="green", fg="black").pack(fill=BOTH, expand=False)
Label(root, text="Blue Sky", bg="blue", fg="white").pack(fill=BOTH, expand=False)

mainloop()