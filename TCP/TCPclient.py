import socket
import os
from socket import AF_INET, SOCK_STREAM
import time
import sys
import math

BUFFER_SIZE = int(sys.argv[1])

HOST = "127.0.0.1"
PORT = 12345

# create the client socket
client_socket = socket.socket(AF_INET, SOCK_STREAM)

# disable Nagle's Algorithm if user wants to
if (sys.argv[2] == "Y" or sys.argv[2] == "y"):
    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)

# disable Delayed ACK if user wants to
if (sys.argv[3] == "Y" or sys.argv[3] == "y"):
    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, True)

# ask user for the name of the file to receieve
filename = sys.argv[4]

# create the name with which the file will be saved
newfilename = filename.split('.')[0] + "TCP" + str(os.getpid()) + "." + filename.split('.')[1]

# start timer
start_time = time.time()

# establishing connection
print("[+] Connecting to " + str(HOST) + " : " + str(PORT))
client_socket.connect((HOST, PORT))
print("[+] Connected.")

# send the filename to the server
client_socket.send((str(filename)).encode())

# receive the message from server indicating whether requested file is available or not
availability = client_socket.recv(1024).decode()
if availability == "<NOTFOUND>":
    print("File not available.")
    client_socket.close()
    exit()
else:
    print("File found.")

client_socket.send("<AVAILABILITYRECVD".encode())

# receive expected file size
expected_filesize = int(client_socket.recv(1024).decode())

# reply that client received the size
client_socket.send("<FILESIZERECVD".encode())

# start receiving the file and writing into a file
print("Receiving " + str(filename), end ="...")
with open(newfilename, "wb") as f:
    for _ in range(math.ceil(expected_filesize/BUFFER_SIZE)):
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:    
            # nothing is received means that file transmitting is done
            break
        # write to the file
        f.write(bytes_read)

client_socket.send("<EXIT>".encode())

# close the client socket
client_socket.close()

# end timer
end_time = time.time()

# get the file size
filesize = os.path.getsize(newfilename)

# print received message
print("\n" + str(filename)  + "(" + str(filesize) + " Bytes)" + " received. Saved as " + newfilename + ". Elapsed time: " + str(end_time-start_time) + " seconds")
