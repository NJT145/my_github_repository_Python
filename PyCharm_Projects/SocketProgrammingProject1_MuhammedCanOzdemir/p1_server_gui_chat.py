import tkinter as tk
from helper import *
import threading
import socket
from functools import partial
from tkinter import filedialog as fd
import os


class ServerGuiPart2:

    def __init__(self, connection, ip, selected_prot):
        self.base = tk.Tk()
        self.base.title("Chat Server")
        self.base.geometry("400x450")
        self.base.resizable(width="false", height="false")
        self.base.resizable(width="false", height="false")
        self.base.configure(bg="#716664")
        self.s_connection = connection
        self.s_ip = ip
        self.s_port = 5555
        self.c_port = 5556
        self.s_protocol = selected_prot
        if self.s_protocol == "udp":
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(("0.0.0.0", self.s_port))
        elif self.s_protocol == "tcp":
            self.server_socket = connection

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
        self.maxPackID = 10 ** 10
        self.fileToSend = None
        self.filePathToSend = None
        self.fileGetRequestWaitingToSend = False
        self.fileToGet = None
        self.fileNameToGet = None
        self.fileHashToGet = None
        self.fileSendRequestWaitingToGet = False
        self.errorMssgReceived = False
        self.fileToDownload_Info = {}
        self.packages = []
        self.currentPackID = 0
        self.currentPackageID = 0

        threading.Thread(target=self.ReceiveData).start()
        self.base.mainloop()

    def ReceiveData(self):
        if self.s_protocol == "tcp":
            while 1:
                try:
                    data = self.server_socket.recv(1024).decode("utf-8")
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
                        dir_path, fileName = os.path.split(self.filePathToSend)
                        # check file name
                        fileNameOk = data.split("/")[0][14:].startswith(fileName)
                        # check hash key
                        hashKeyOk = data.split("/")[1][8:].startswith(md5Checksum(self.filePathToSend))
                        if fileNameOk and hashKeyOk:
                            checksumMssg = checksumPack(md5Checksum(self.filePathToSend), len(self.fileToSend),
                                                        self.maxPackID, sys.getsizeof(self.fileToSend[-1]))
                            self.server_socket.sendall(checksumMssg.encode("utf-8"))
                            for packID, packPart in enumerate(self.fileToSend):
                                mssg = sendPackageMssg(packIndexStr(packID, self.maxPackID), packPart)
                                self.server_socket.sendall(mssg)
                        else:
                            #self.server_socket.sendall(errorMssg.encode("utf-8"))
                            pass  # TODO: send error message
                    elif isPackageMssg(data): # get package #TODO: check for corrupted packages
                        pack = getPackageMssg(data)
                        self.writePacks(pack)
                    elif isChecksumMssg(data): # get file info
                        self.fileToDownload_Info = getChecksumPack(data)
                        #TODO: check file hash at the end
                    elif isPackageMssg(data): # get package
                        pack = getPackageMssg(data)
                        if pack not in self.packages:
                            self.packages.append(pack)
                        #TODO: write file to somewhere
                    elif isChecksumMssg(data): # get file info
                        self.fileToDownload_Info = getChecksumPack(data)
                        #TODO: check file hash at the end
                    else:
                        data1 = receiveEmoji(data)
                        displayRemoteMessage(self.chatBox, data1)
                else:
                    getConnectionInfo(self.chatBox, '\n [ Your partner left. ] \n')
                    self.server_socket.close()
                    break
        else:
            while 1:
                try:
                    data, address = self.server_socket.recvfrom(1024)
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
                        dir_path, fileName = os.path.split(self.filePathToSend)
                        # check file name
                        fileNameOk = data.split("/")[0][14:].startswith(fileName)
                        # check hash key
                        hashKeyOk = data.split("/")[1][8:].startswith(md5Checksum(self.filePathToSend))
                        if fileNameOk and hashKeyOk:
                            checksumMssg = checksumPack(md5Checksum(self.filePathToSend), len(self.fileToSend),
                                                        self.maxPackID, sys.getsizeof(self.fileToSend[-1]))
                            self.server_socket.sendto(checksumMssg.encode("utf-8"), (self.s_ip, self.c_port))
                            for packID, packPart in enumerate(self.fileToSend):
                                mssg = sendPackageMssg(packIndexStr(packID, self.maxPackID), packPart)
                                self.server_socket.sendto(mssg, (self.s_ip, self.c_port))
                        else:
                            #self.server_socket.sendto(errorMssg.encode("utf-8"), (self.s_ip, self.c_port))
                            pass  # TODO: send error message
                    elif isPackageMssg(data): # get package #TODO: check for corrupted packages
                        pack = getPackageMssg(data)
                        self.writePacks(pack)
                    elif isChecksumMssg(data): # get file info
                        self.fileToDownload_Info = getChecksumPack(data)
                        #TODO: check file hash at the end
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
        if self.s_protocol == "tcp":
            self.server_socket.sendall(sendEmoji(messageText).encode("utf-8"))
            if self.filePathToSend != None:  # send request from you to partner
                dir_path, fileName = os.path.split(self.filePathToSend)
                self.server_socket.sendall(fileSendRequest(fileName, md5Checksum(self.filePathToSend)).encode("utf-8"))
                self.cancelFileButton.destroy()
        else:
            self.server_socket.sendto(sendEmoji(messageText).encode("utf-8"), (self.s_ip, self.c_port))
            if self.filePathToSend != None:  # send request from you to partner
                dir_path, fileName = os.path.split(self.filePathToSend)
                self.server_socket.sendto(fileSendRequest(fileName, md5Checksum(self.filePathToSend)).encode("utf-8"),
                                          (self.s_ip, self.c_port))
                self.cancelFileButton.destroy()

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
            tk.Button(self.base1, font="Helvetica", text=j, bd=0, activebackground="#BDE096", justify="left",
                      command=partial(self.addEmoji, k)).pack(side="left")

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

        # self.getDownloadFile(filename)

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
        self.writeTo = fd.asksaveasfilename()
        # send a "get" request from you to partner
        if self.s_protocol == "tcp":
            self.server_socket.sendall(fileGetRequest(self.fileNameToGet, self.fileHashToGet).encode("utf-8"))
        else:
            self.server_socket.sendto(fileGetRequest(self.fileNameToGet, self.fileHashToGet).encode("utf-8"),
                                      (self.s_ip, self.s_port))

        self.downloadStatus = tk.Label(self.base, font="Helvetica", text=u"status", bd=1, bg="gray", fg="Black",
                                       relief=SUNKEN)
        self.downloadStatus.place(x=180, y=335, height=20, width=100)
        # TODO: file download loop --> done


    def cleanDownloadStatus(self):
        self.downloadStatus.destroy()

    def writePacks(self, pack):
        if pack not in self.packages:
            self.packages.append(pack)
        self.packages.sort()
        if self.packages[self.currentPackageID][0] == self.currentPackID:
            writeFile(self.writeTo, self.packages[self.currentPackageID][1])
            self.currentPackageID += 1
            self.currentPackID += 1
        elif self.packages[self.currentPackageID][0] > self.currentPackID:
            self.currentPackID += 1
            self.writePacks(pack)
        else:
            raise errorMessage("package error")
