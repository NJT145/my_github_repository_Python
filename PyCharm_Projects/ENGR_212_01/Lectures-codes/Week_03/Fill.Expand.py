__author__ = 'acakmak'

import Tkinter as tk

root = tk.Tk()
root.geometry('200x200+200+200')

tk.Label(root, text='Label', bg='green').pack(expand=0, fill=tk.BOTH, side =tk.TOP)
#tk.Label(root, text='Label2', bg='red').pack(expand=1, fill=tk.BOTH, side =tk.TOP)

root.mainloop()