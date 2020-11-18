import socket
import os
from socket import AF_INET, SOCK_STREAM
import sys

BUFFER_SIZE = int(sys.argv[1])

HOST = "127.0.0.1"
PORT = 12345

# creating server socket
server_socket = socket.socket(AF_INET, SOCK_STREAM)

# bind the socket to our local address
server_socket.bind((HOST, PORT))

# disable Nagle's Algorithm if user wants to
if (sys.argv[2] == "Y" or sys.argv[2] == "y"):
    server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)

# disable Delayed ACK if user wants to
if (sys.argv[3] == "Y" or sys.argv[3] == "y"):
    server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, True)

# enabling our server to accept connections
server_socket.listen(4)
print("[*] Listening as " + str(HOST) + " : " + str(PORT))

# accept connection
client_socket, address = server_socket.accept() 
print("[+] " + str(address) + " is connected.")

# receive the filename to be sent to client
received = client_socket.recv(1024).decode()
filename = received
filename = os.path.basename(filename)

# check if requested file is available or not and inform client
try:
    filesize = os.path.getsize(filename)
    print("File is available.")
    client_socket.send("<FOUND>".encode())
except FileNotFoundError:
    print("File not available.")
    client_socket.send("<NOTFOUND>".encode())
    server_socket.close()
    exit()

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


