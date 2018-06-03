import tkinter as tk
from helper import *
import threading
import socket
from functools import partial
from tkinter import filedialog as fd
import os


class ClientGuiPart2:

    def __init__(self, connection, ip, selected_prot):
        self.base = tk.Tk()
        self.base.title("Chat Client")
        self.base.geometry("400x450")
        self.base.resizable(width="false", height="false")
        self.base.configure(bg="#716664")
        self.c_connection = connection
        self.c_ip = ip
        self.c_port = 5556
        self.s_port = 5555
        self.c_protocol = selected_prot
        if self.c_protocol == "udp":
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.client_socket.bind(("0.0.0.0", self.c_port))
        elif self.c_protocol == "tcp":
            self.client_socket = connection

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

        self.textBox = tk.Text(self.base, bd=0, width="29", height="5", font="Helvetica")
        self.textBox.bind("<Return>", self.removeKeyboardFocus)
        self.textBox.bind("<KeyRelease-Return>", self.onEnterButtonPressed)

        self.sendFileNameBox = tk.Label(self.base, font="Helvetica", text=u"abc", bd=0, bg="green", fg="White")

        self.fileUploadButton = tk.Button(self.base, font="Helvetica", text=u"BROWSE", width="50", height=5,
                                          bd=0, activebackground="#BDE096", justify="center",
                                          command=self.onClickUpload)

        self.sb.place(x=370, y=5, height=300)
        self.chatBox.place(x=15, y=5, height=300, width=355)

        self.sendButton.place(x=155, y=360, height=80, width=90)
        self.selectemoji.place(x=250, y=360, height=80, width=50)
        self.textBox.place(x=15, y=360, height=80, width=150)
        self.fileUploadButton.place(x=305, y=360, height=80, width=90)

        self.packSize = 1000
        self.fileToSend = None
        self.filePathToSend = None
        self.fileGetRequestWaitingToSend = False
        self.fileToGet = None
        self.fileNameToGet = None
        self.fileHashToGet = None
        self.fileSendRequestWaitingToGet = False

        threading.Thread(target=self.ReceiveData).start()
        self.base.mainloop()

    def ReceiveData(self):
        if self.c_protocol == "tcp":
            while 1:
                try:
                    data = self.client_socket.recv(1024).decode("utf-8")
                except:
                    getConnectionInfo(self.chatBox, '\n [ Your partner left.] \n')
                    break
                if data != '':
                    self.fileGetRequestWaitingToSend = isFileGetRequest(data)
                    self.fileSendRequestWaitingToGet = isFileSendRequest(data)
                    if self.fileSendRequestWaitingToGet:  # get file name from partner to download
                        self.fileNameToGet = data.split("/")[0][15:]
                        self.fileHashToGet = data.split("/")[1][8:]
                        self.getDownloadFile(self.fileNameToGet)
                    elif self.fileGetRequestWaitingToSend:  # send file to partner
                        pass  # TODO: send file # Use "self.fileToSend"
                    else:
                        data1 = receiveEmoji(data)
                        displayRemoteMessage(self.chatBox, data1)
                else:
                    getConnectionInfo(self.chatBox, '\n [ Your partner left. ] \n')
                    self.client_socket.close()
                    break
        else:
            while 1:
                try:
                    data, address = self.client_socket.recvfrom(1024)
                    data = data.decode("utf-8")
                    print(data)
                except:
                    getConnectionInfo(self.chatBox, '\n [ Your partner left.] \n')
                    break
                if data != '':
                    self.fileGetRequestWaitingToSend = isFileGetRequest(data)
                    self.fileSendRequestWaitingToGet = isFileSendRequest(data)
                    if self.fileSendRequestWaitingToGet:  # get file name from partner to download
                        self.fileNameToGet = data.split("/")[0][15:]
                        self.fileHashToGet = data.split("/")[1][8:]
                        self.getDownloadFile(self.fileNameToGet)
                    elif self.fileGetRequestWaitingToSend:  # send file to partner
                        pass  # TODO: send file # Use "self.fileToSend"
                    else:
                        data1 = receiveEmoji(data)
                        displayRemoteMessage(self.chatBox, data1)
                else:
                    getConnectionInfo(self.chatBox, '\n [ Your partner left. ] \n')
                    break

    def onClick(self):
        messageText = messageFilter(self.textBox.get("0.0", END))
        displayLocalMessage(self.chatBox, messageText)
        self.chatBox.yview(END)
        self.textBox.delete("0.0", END)
        if self.c_protocol == "tcp":
            self.client_socket.sendall(sendEmoji(messageText).encode("utf-8"))
            if self.filePathToSend != None:  # send request from you to partner
                dir_path, fileName = os.path.split(self.filePathToSend)
                self.client_socket.sendall(fileSendRequest(fileName, md5Checksum(self.filePathToSend)).encode("utf-8"))

        else:
            self.client_socket.sendto(sendEmoji(messageText).encode("utf-8"), (self.c_ip, self.s_port))
            if self.filePathToSend != None:  # send request from you to partner
                dir_path, fileName = os.path.split(self.filePathToSend)
                self.client_socket.sendto(fileSendRequest(fileName, md5Checksum(self.filePathToSend)).encode("utf-8"),
                                          (self.c_ip, self.c_port))

    def onEnterButtonPressed(self, event):
        self.textBox.config(state="normal")
        self.onClick()

    def removeKeyboardFocus(self, event):
        self.textBox.config(state="disabled")

    def onEmoji(self):

        self.base1 = tk.Tk()
        self.base1.title("Emojis")
        self.base1.geometry("100x150")
        emojilist = getEmojis()
        self.button_list = [i for i in range(len(emojilist))]
        for k, j in emojilist.items():
            print(k)
            self.button_list[k] = tk.Button(self.base1, font="Helvetica", text=j, bd=0, activebackground="#BDE096",
                                            justify="left", command=partial(self.addEmoji, k))
            self.button_list[k].pack(side="left")

    def addEmoji(self, ind):
        emo = getEmoji(ind)
        self.textBox.insert('end', emo)

    def onClickUpload(self):
        browse = fd.askopenfilename()
        dir_path, filename = os.path.split(browse)
        self.filePathToSend = browse
        self.fileToSend = fileBit_sliceAndDice(browse, self.packSize)
        self.sendFileNameBox = tk.Label(self.base, font="Helvetica", text=u"sendFileNameBox", bd=0, bg="green",
                                        fg="White")
        self.cancelFileButton = tk.Button(self.base, font="Helvetica", text=u"cancle", width="100", height=5,
                                          bd=0, activebackground="#BDE096", justify="center", bg="red", fg="White",
                                          command=self.onClickCancel)
        self.sendFileNameBox.place(x=15, y=310, height=20, width=150)
        self.cancelFileButton.place(x=290, y=310, height=20, width=100)
        self.sendFileNameBox.config(text=filename)

    def onClickCancel(self):
        self.sendFileNameBox.destroy()
        self.cancelFileButton.destroy()

    def getDownloadFile(self, filename):
        self.downloadFileNameBox = tk.Label(self.base, font="Helvetica", text=u"downloadFileNameBox", bd=0, bg="green",
                                            fg="White")
        self.downloadFileButton = tk.Button(self.base, font="Helvetica", text=u"Download", width="100", height=5,
                                            bd=0, activebackground="#BDE096", justify="center", bg="red", fg="White",
                                            command=self.onClickDownload)
        self.downloadFileNameBox.place(x=15, y=335, height=20, width=150)
        self.downloadFileButton.place(x=290, y=335, height=20, width=100)

        self.downloadFileNameBox.config(text=filename)

    def cleanDownload(self):
        self.downloadFileNameBox.destroy()
        self.downloadFileButton.destroy()

    def onClickDownload(self):
        # send a "get" request from you to partner
        if self.c_protocol == "tcp":
            self.client_socket.sendall(fileGetRequest(self.fileNameToGet, self.fileHashToGet).encode("utf-8"))
        else:
            self.client_socket.sendto(fileGetRequest(self.fileNameToGet, self.fileHashToGet).encode("utf-8"),
                                      (self.c_ip, self.s_port))
        self.downloadStatus = tk.Label(self.base, font="Helvetica", text=u"status", bd=1, bg="gray", fg="Black",
                                       relief=SUNKEN)

        self.downloadStatus.place(x=180, y=335, height=20, width=100)
        # TODO: file download loop

    def cleanDownloadStatus(self):
        self.downloadStatus.destroy()
