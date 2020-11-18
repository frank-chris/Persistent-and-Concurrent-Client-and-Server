import socket
import os
from socket import AF_INET, SOCK_DGRAM
import sys

BUFFER_SIZE = int(sys.argv[1])

HOST = "127.0.0.1"
PORT = 12345

# creating server socket
server_socket = socket.socket(AF_INET, SOCK_DGRAM)

# bind the socket to our local address
server_socket.bind((HOST, PORT))

# print that server is ready
print("[*] Ready to receive as " + str(HOST) + " : " + str(PORT))


# receive the filename to be sent to client
received, client_address = server_socket.recvfrom(1024)
filename = received.decode()
filename = os.path.basename(filename)

# check if requested file is available or not and inform client
try:
    filesize = os.path.getsize(filename)
    print("File is available.")
    server_socket.sendto("<FOUND>".encode(), client_address)
except FileNotFoundError:
    print("File not available.")
    server_socket.sendto("<NOTFOUND>".encode(), client_address)
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
        server_socket.sendto(bytes_read, client_address)

# print sent message
print("\n" + str(filename)  + "(" + str(filesize) + " Bytes)" + " sent.")

# close the socket
server_socket.close()


