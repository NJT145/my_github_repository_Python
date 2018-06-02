import tkinter as tk
import socket
import threading
import p1_server_gui_chat

class ServerGuiPart1:
    def __init__(self):

        self.parent = tk.Tk()
        self.parent.tk.call('encoding', 'system', 'utf-8')
        self.parent.geometry('450x300')
        self.label = tk.Label(self.parent, text="Project 1", fg="black", font=("Times", 20, "bold italic")) \
            .grid(column=2, row=0, sticky="SE", padx=10)
        self.label2 = tk.Label(self.parent, text="Enter Destination IP: ", fg="black", font=("Times", 12)) \
            .grid(column=0, row=1)
        self.destinationIP = tk.Entry(self.parent)
        self.destinationIP.grid(column=2, row=1)
        self.var_protocol = tk.StringVar()
        self.label3 = tk.Label(self.parent, text="Protocol: ", fg="black", font=("Times", 12)) \
            .grid(column=0, row=2)
        self.protocol_type1 = tk.Radiobutton(self.parent, text="TCP", variable=self.var_protocol, value="tcp") \
            .grid(column=2, row=2)
        self.protocol_type2 = tk.Radiobutton(self.parent, text="UDP", variable=self.var_protocol, value="udp") \
            .grid(column=3, row=2)
        self.remaining=0
        self.submit_button = tk.Button(self.parent, text=u'Start Connection',command=self.countdown, width=20)
        self.submit_button.grid(row=3,column=2)
        self.parent.mainloop()

    def countdown(self):
        self.label11 = tk.Label(self.parent, text="Waiting to Connection Partner ", fg="red",
                                font=("Times", 12)).grid(column=2, row=4)
        host_ip = self.destinationIP.get()
        host_port = 5555
        selected_prot = self.var_protocol.get()
        threading.Thread(target=self.start_connection, args=(host_ip, host_port, selected_prot)).start()

    def start_connection(self,host, port, protocol):
        self.host = host
        self.port = port
        self.protocol = protocol
        self.server_socket = None

        if self.protocol == "tcp":
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(("0.0.0.0", int(self.port)))
            self.server_socket.listen(1)
            self.label11 = tk.Label(self.parent, text="Waiting to Connection Partner ", fg="red",
                                    font=("Times", 12)).grid(column=2, row=4)
            while True:
                conn, address = self.server_socket.accept()
                self.label11 = tk.Label(self.parent, text="--------------------------------------").grid(column=2,
                                                                                                         row=4)
                p1_server_gui_chat.ServerGuiPart2(conn,address, self.protocol)

        elif self.protocol == "udp":
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(("0.0.0.0", int(self.port)))
            while True:
                message, addr = self.server_socket.recvfrom(1024)
                self.label11 = tk.Label(self.parent, text="--------------------------------------").grid(column=2,
                                                                                                         row=4)
                print(addr)
                if message.decode("utf-8") == "udp":
                    p1_server_gui_chat.ServerGuiPart2("", self.host, self.protocol)
        else:
            print("try connection again")


ServerGuiPart1()