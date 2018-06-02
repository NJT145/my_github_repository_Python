#!/usr/bin/env python
import socket,threading

def tcp():
    host = "127.0.0.1" #server ip
    port = 5000 #server port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#create socket for tcp connection
    server.bind((host, port)) # server binded given ip and port
    server.listen(5) # server wait client connection request
    print("[*] Listening on %s:%d" % (host, port))
    def handle_client(client_socket):
        mf = client_socket.recv(1024).decode('utf-8') # client send type that which kind of data will send (message or file)
        print(mf)
        client.send('ready'.encode('utf-8'))# server give feedback server is ready to get data
        if mf =='message':
            request = client_socket.recv(1024).decode('utf-8') # server get message data
            print("[*] Received: %s" % request)
            client_socket.send(request.encode('utf-8')) # server give feedback which message is received
        elif mf == 'file':
            request = client_socket.recv(1024).decode('utf-8') # server get filename
            print(request)
            new_file=open(request,'wb') # open new file byte mode has sent filename
            client_socket.send('file created'.encode('utf-8')) # server give feedback file created and ready to receive file datas
            while True: # until end of file get datas
                part=client.recv(1024) # get each data package of file
                print(part)
                if part!=''.encode('utf-8'): # if data is not empty
                    if b'olala' in part: # if data has identifier that belongs the file
                        new_file.write(part.split(b'olala')[1]) # write data to new file
                        client.send('ok'.encode('utf-8')) # server give feedback to client the data is received and ready to next package
                    else:
                        number=int(part)# number of package info received at the end
                        print('number of data: '+str(number))
                        client.send('ok'.encode('utf-8')) # server give feedback that last data received
                        break # end the recursion
                else:
                    break
            new_file.close() # close and save new file
        client.close() # close the client server connection


    while True:
        client, addr = server.accept() # accept client request
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

tcp()