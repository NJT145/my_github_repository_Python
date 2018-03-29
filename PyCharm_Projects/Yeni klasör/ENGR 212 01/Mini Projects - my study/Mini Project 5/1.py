import Tkinter as tk
from tkFont import Font

class Pad(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.toolbar = tk.Frame(self, bg="#eee")
        self.toolbar.pack(side="top", fill="x")

        self.bold_btn = tk.Button(self.toolbar, text="Bold", command=self.make_bold)
        self.bold_btn.pack(side="left")

        self.clear_btn = tk.Button(self.toolbar, text="Clear", command=self.clear)
        self.clear_btn.pack(side="left")

        # Creates a bold font
        self.bold_font = Font(family="Helvetica", size=14, weight="bold")

        self.text = tk.Text(self)
        self.text.insert("end", "Select part of text and then click 'Bold'...")
        self.text.focus()
        self.text.pack(fill="both", expand=True)

        # configuring a tag called BOLD
        self.text.tag_configure("BOLD", font=self.bold_font)

    def make_bold(self):
        # tk.TclError exception is raised if not text is selected
        try:
            self.text.tag_add("BOLD", "sel.first", "sel.last")
        except tk.TclError:
            pass

    def clear(self):
        self.text.tag_remove("BOLD",  "1.0", 'end')


def demo():
    root = tk.Tk()
    Pad(root).pack(expand=1, fill="both")
    root.mainloop()


if __name__ == "__main__":
    demo()