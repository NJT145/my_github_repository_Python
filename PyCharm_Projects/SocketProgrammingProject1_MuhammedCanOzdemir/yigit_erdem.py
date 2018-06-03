# -*- coding: utf-8 -*-
### server
import socket,time
from tkinter import *
from tkinter import filedialog

class mp1:
    def __init__(self,root):
        self.root=root
        self.cport=5001 # client port for udp
        self.sport=5000 # tcp server port
        self.uport=5002 # udp server port
        self.gui()

    def gui(self):
        self.label1=Label(text='Enter the IP address of the destination')
        self.label2=Label(text='Choose the protocol (TCP or UDP)')

        self.entry1=Entry(width=15)
        self.entry2=Entry(width=30)

        self.var=IntVar()
        self.radiobutton1=Radiobutton(text='TCP',variable=self.var,value=0)
        self.radiobutton2=Radiobutton(text='UDP',variable=self.var,value=1)
        self.var.set(1)

        self.text1=Text(height=10,width=50)

        self.listbox1=Listbox(height=10,width=5)

        self.button1=Button(text='Send',width=10,command=self.tcp_udp)
        self.button2=Button(text='Select a file',width=10,command=self.select)

        self.label1.grid(row=0,column=0,columnspan=2,pady=10)
        self.label2.grid(row=1,column=0,columnspan=2,pady=10)
        self.entry1.grid(row=0,column=2,columnspan=2,pady=10)
        self.entry2.grid(row=3,column=0,pady=10)
        self.radiobutton1.grid(row=1,column=2,pady=10)
        self.radiobutton2.grid(row=1,column=3,pady=10)
        self.text1.grid(row=2,column=0,columnspan=2,pady=10)
        self.listbox1.grid(row=2,column=2,columnspan=2,pady=10)
        self.button1.grid(row=3,column=2,pady=10)
        self.button2.grid(row=3,column=1,pady=10)
        self.entry1.insert(END,'127.0.0.1') # write default connection ip

    def tcp_udp(self):# get and redirect connection types
        type=self.var.get()
        if type:
            self.send_udp()
        else:
            self.send_tcp()

    def send_tcp(self):
        host = self.entry1.get() # get host ip
        filename=self.entry2.get() # get filepath
        self.tcp_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create connection for tcp connection
        self.tcp_conn.connect((host, self.sport)) # send connection request to specified ip and port
        message = self.text1.get(0.0,END).replace('\n','') # get message
        if message != '':
            self.tcp_conn.send('message'.encode('utf-8')) # send type data to server
            ready = self.tcp_conn.recv(1024).decode('utf-8') # get data from server that server is ready to receive the message
            if ready =='ready':
                self.tcp_conn.send(message.encode('utf-8')) # send message data to server
                data = self.tcp_conn.recv(1024).decode('utf-8') # get data from server that sent to server
                print('sended: '+data)
        elif filename:
            self.tcp_conn.send('file'.encode('utf-8'))# send type data to server
            ready = self.tcp_conn.recv(1024).decode('utf-8')# get data from server that server is ready to receive the file
            if ready =='ready':
                self.tcp_conn.send(filename.split('/')[-1].encode('utf-8')) # get filename from filepath and send to server
                data = self.tcp_conn.recv(1024).decode('utf-8')# get data that file created and ready to receive file data
                if data=='file created':
                    file=open(filename,'rb') # read file as bytes
                    i=0 # id of package
                    while True:
                        part=file.read(1000) # read file next 1000 bytes each time
                        if part!=bytes('','utf-8'):# if data is not empty
                            num=str(i)+'olala' # olala is for unify the file data
                            message=bytes(str(num),'utf-8')+part # create package with id of package and data
                            self.tcp_conn.send(message) # send the package to server
                            i+=1 # increase id of package
                            okey=self.tcp_conn.recv(1024).decode('utf-8') # get feedback from server that package is received
                            if okey=='ok':
                                continue
                        else: # when file data is empty break the loop
                            break
                    self.tcp_conn.send(str(i).encode('utf-8')) # send the number of packages to server
                self.tcp_conn.send('end'.encode('utf-8')) # send file transfer is finish
        self.tcp_conn.close() # close the server connection

    def send_udp(self):
        host = self.entry1.get()# get host ip
        filename = self.entry2.get()  # get filepath
        try:
            self.udp_conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # if none, create socket for udp connection
            self.udp_conn.bind((host, self.cport)) # bind the socket specified ip and port
        except OSError:
            pass # use existing socket

        message = self.text1.get(0.0,END).replace('\n','') # get message
        if message:
            self.udp_conn.sendto('message'.encode('utf-8'),(host,self.uport)) # send type data to server
            data, addr = self.udp_conn.recvfrom(1024)# get data from server that server is ready to receive the message
            if 'message'==data.decode('utf-8'):
                while True: # try to send until it is reach to server
                    self.udp_conn.sendto(message.encode('utf-8'), addr) # send message to server
                    data, addr = self.udp_conn.recvfrom(1024) #get feedback from server that message is received
                    data = data.decode('utf-8')
                    print('Received from server: ' + data)
                    if data: # if data is reach break the loop
                        break
        elif filename:
            self.udp_conn.sendto(('file:'+filename.split('/')[-1]).encode('utf-8'),(host,self.uport))  # send type data to server
            data, addr = self.udp_conn.recvfrom(1024) # get data from server that server is ready to receive the file
            if 'file:' in data.decode('utf-8'):
                file=open(filename,'rb') # read file as bytes
                i = 0 # if of packages
                start = time.time()
                while True:
                    part = file.read(1000)# read file next 1000 bytes each time
                    if part != bytes('', 'utf-8'):# if data is not empty
                        num = str(i) + 'olala' # olala is for unify the file data
                        message = bytes(str(num), 'utf-8') + part # create package with id of package and data
                        self.udp_conn.sendto(message,addr) # send the package to server
                        i += 1 # increase id of package
                        #okey,addr=self.udp_conn.recvfrom(1024) # get feedback from server that package is received
                        #if okey==b'ok':
                            #continue
                    else: # when file data is empty break the loop
                        break
                time.sleep(1)
                self.udp_conn.sendto(str(i).encode('utf-8'),addr) # send the number of packages to server
                end=time.time()
                print('number of data: '+str(i)+' sent in '+str(end-start)[:5]+' second')


    def select(self): # file selection
        filename=filedialog.askopenfilename() # select a file as filepath
        self.entry2.delete(0,END) # if any, delete existing filename
        self.entry2.insert(END,filename) # write filepath to the entry

    def emojis_select(self):
        pass

    def emojis_decode(self):
        pass

    def emojis_encode(self):
        pass


root = Tk()
root.title("Send Message")
app=mp1(root)
root.mainloop()
