
import platform

req_version = "2.7"
cur_version = platform.python_version()

if cur_version >= req_version and cur_version < "3.0":
   print("Current python version: "+cur_version)
   import Tkinter as tk
   import ttk as ttk
   import tkFileDialog as tkFileDialog
   import tkMessageBox as tkMessageBox

   #import myApp
   #myApp.run()

elif cur_version > "3.0":
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.filedialog as tkFileDialog
    import tkinter.messagebox as tkMessageBox

    # import myApp
    # myApp.run()

    print("Current Python interpreter can not open this program.\n" +
          "This program can only work with Python versions between 2.7 and 3.0 .")

else:
    print("Current Python interpreter can not open this program.\n" +
          "This program can only work with Python versions between 2.7 and 3.0 .")



class SlidingPuzzle(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.pack(fill=tk.BOTH, expand=True)



def run():
    root = tk.Tk()
    root.wm_title("Sliding Puzzle")
    root.geometry("600x400+400+150")
    app = SlidingPuzzle(root)
    root.mainloop()
"""
if __name__ == '__main__':
    run()
"""