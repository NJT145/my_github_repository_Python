import tkinter as tk
import socket
import threading
import p1_client_gui_chat

class ClientGuiPart1:

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
        threading.Thread(target=self.start_client, args=(host_ip, host_port, selected_prot)).start()

    def start_client(self,host_ip, host_port, selected_prot):
        self.host = host_ip
        self.port = int(host_port)
        self.protocol = selected_prot
        self.client_socket = None

        if selected_prot == "tcp":
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))  # connect to the server
            p1_client_gui_chat.ClientGuiPart2(client_socket, self.host, selected_prot)
        elif selected_prot == "udp":
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client_socket.connect((self.host, self.port))
            client_socket.sendto("udp".encode("utf-8"), (self.host, self.port))
            p1_client_gui_chat.ClientGuiPart2(client_socket, self.host, selected_prot)
        else:
            print("try connection again")


ClientGuiPart1()