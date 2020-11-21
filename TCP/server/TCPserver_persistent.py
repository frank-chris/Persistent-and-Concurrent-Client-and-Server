import socket
import os
from socket import AF_INET, SOCK_STREAM
import sys
import time

if len(sys.argv) != 2:
    print("Usage:\npython3 TCPserver_persistent.py buffer_size\nExample:\npython3 TCPserver_persistent.py 32768")
    exit()

BUFFER_SIZE = int(sys.argv[1])

HOST = "127.0.0.1"
PORT = 12345

# creating server socket
server_socket = socket.socket(AF_INET, SOCK_STREAM)

# bind the socket to our local address
server_socket.bind((HOST, PORT))

# enabling our server to accept connections
server_socket.listen(4)

while True:
    print("[*] Listening as " + str(HOST) + " : " + str(PORT))

    # accept connection
    client_socket, address = server_socket.accept() 
    print("[+] " + str(address) + " is connected.")

    while True:
        # receive the filename to be sent to client
        received = client_socket.recv(1024).decode()
        filename = received

        # exit the loop
        if filename == "<EXIT>":
            print("Closing the connection.")
            break

        filename = os.path.basename(filename)

        # check if requested file is available or not and inform client
        try:
            filesize = os.path.getsize(filename)
            print("File is available.")
            client_socket.send("<FOUND>".encode())
        except FileNotFoundError:
            print("File not available.")
            client_socket.send("<NOTFOUND>".encode())
            continue

        # inform the client about the file size 
        client_socket.send(str(filesize).encode())
        
        filesize_status = client_socket.recv(1024).decode()

        # start sending file
        print("Sending " + str(filename) + "(" + str(filesize) + " Bytes)", end ="...")
        with open(filename, "rb") as f:
            while True:
                # read from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # sendall ensures transmission even in busy networks
                client_socket.sendall(bytes_read)

        # print sent message
        print("\n" + str(filename)  + "(" + str(filesize) + " Bytes)" + " sent.")

# close the socket
server_socket.close()


