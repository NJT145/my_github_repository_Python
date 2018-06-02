#!/usr/bin/env python
import socket,threading


def udp():
    host = '127.0.0.1' # server ip
    port = 5002 # server port
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # create socket for udp connection
    server.bind((host, port)) # server binded given ip and port
    print ('Server Started')
    while True: # wait the data sent by a client
        type, addr = server.recvfrom(1024) # get the type data (message or file) by a client and address of client
        type = type.decode('utf-8') # decode the data bytes to string
        print("type: " + type)
        server.sendto(type.encode('utf-8'), addr) #server give feedback to the client the type data is received
        if type=='message':
            data, addr = server.recvfrom(1024) # server get message from a client and address of client
            data = data.decode('utf-8')
            print("message From: " + str(addr))
            print("message: " + data)
            server.sendto(data.encode('utf-8'), addr) # server give feedback which message is received
        elif 'file:' in type:
            file=open(type.split('file:')[-1],'wb') # get filename from type data and create new file byte mode has sent filename
            file_list=[] # create a list to save file datas
            while True:
                part,addr=server.recvfrom(1024) # get data package that sent a client and address of client
                if b'olala' in part: # if data has identifier that belongs the file
                    index,data=part.split(b'olala') # end split sent data index of file data and file data
                    file_list.append((int(index),data)) # append index and data to the list
                    #server.sendto(b'ok',addr) # server give feedback to the client the file data is received
                    file.write(part.split(b'olala')[-1]) # write the data to the new file
                else:
                    number=int(part)# number of package info received at the end
                    print('number of data: '+str(number))
                    server.sendto(b'end',addr) # server give feedback to the client the end data is received
                    break #end the recursion when all file datas sent
            if len(file_list)==number: # check all file is received or not
                print('all_data is received')
            else:
                print(str(float(len(file_list))*100/number)[:5]+'% of data received')
            file.close() # save and close the file
            print('file created')

udp()