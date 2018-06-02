import tkinter as tk
from helper import *
import threading
import socket
from functools import partial
from tkinter import filedialog as fd
import os

class ServerGuiPart2:

    def __init__(self):
        self.base = tk.Tk()
        self.base.title("Chat Server")
        self.base.geometry("400x450")
        self.base.resizable(width="false", height="false")
        self.base.resizable(width="false", height="false")
        self.base.configure(bg="#716664")

        self.sendFileNameBox = None
        self.sendFileButton = None

        self.chatBox = tk.Text(self.base, bd=0, height="8", width="40", font="Helvetica", )
        self.chatBox.config(state="disabled")
        self.sb = tk.Scrollbar(self.base, command=self.chatBox.yview)
        self.chatBox['yscrollcommand'] = self.sb.set
        self.sendButton = tk.Button(self.base, font="Helvetica", text=u"SEND", width="50", height=5,
                            bd=0, activebackground="#BDE096", justify="center",
                            command=self.onClick)
        self.selectemoji = tk.Button(self.base, font="Helvetica", text="\uD83D\uDE01", width="50", height=5,
                                    bd=0, activebackground="#BDE096", justify="center",
                                    command=self.onEmoji)

        self.textBox = tk.Text(self.base, bd=0,  width="29", height="5", font="Helvetica")
        self.textBox.bind("<Return>", self.removeKeyboardFocus)
        self.textBox.bind("<KeyRelease-Return>", self.onEnterButtonPressed)

        self.sendFileNameBox = tk.Label(self.base, font="Helvetica", text=u"abc", bd=0,bg="green",fg="White")
        self.sendFileNameBox2 = tk.Label(self.base, font="Helvetica", text=u"abc", bd=0,bg="green",fg="White")



        self.button3 = tk.Button(self.base, font="Helvetica", text=u"cancle", width="50", height=5,
                            bd=0, activebackground="#BDE096", justify="center",bg="green",fg="White")


        self.fileUploadButton = tk.Button(self.base, font="Helvetica", text=u"BROWSE", width="50", height=5,
                                          bd=0, activebackground="#BDE096", justify="center",
                                          command=self.onClickUpload)

        self.sb.place(x=370, y=5, height=300)
        self.chatBox.place(x=15, y=5, height=300, width=355)

        self.sendFileNameBox2.place(x=15, y=335, height=20, width=100)


        self.button3.place(x=200, y=335, height=20, width=100)


        self.sendButton.place(x=155, y=360, height=80, width=90)
        self.selectemoji.place(x=250, y=360, height=80, width=50)
        self.textBox.place(x=15, y=360, height=80, width=150)
        self.fileUploadButton.place(x=305, y=360, height=80, width=90)

        self.base.mainloop()


    def ReceiveData(self):
        pass

    def onClick(self):
        pass

    def onEnterButtonPressed(self, event):
        pass

    def removeKeyboardFocus(self, event):
        pass

    def onEmoji(self):
        pass

    def addEmoji(self, ind):
        pass

    def onClickUpload(self):
        browse = fd.askopenfilename()
        self.sendFileNameBox = tk.Label(self.base, font="Helvetica", text=u"abc", bd=0, bg="green", fg="White")
        self.sendFileNameBox.place(x=15, y=310, height=20, width=280)
        self.sendFileButton = tk.Button(self.base, font="Helvetica", text=u"cancle", width="50", height=5,
                            bd=0, activebackground="#BDE096", justify="center",bg="red",fg="White",command=self.onClickCancel)
        self.sendFileButton.place(x=310, y=310, height=20, width=60)
        dir_path, filename = os.path.split(browse)
        self.sendFileNameBox.config(text=filename)

    def onClickCancel(self):
        self.sendFileNameBox.destroy()
        self.sendFileButton.destroy()



ServerGuiPart2()