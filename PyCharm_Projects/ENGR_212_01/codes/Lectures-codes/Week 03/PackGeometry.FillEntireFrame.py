from Tkinter import *

root = Tk()

listbox = Listbox(root)
listbox.pack(fill=BOTH, expand=True)
for i in range(20):
    listbox.insert(END, str(i))

mainloop()