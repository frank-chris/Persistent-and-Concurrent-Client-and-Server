##############################################################
#
# Non-persistent TCP Client Script to be used in Mininet questions 
# written for Assignment - 4 
# 
# Author: Chris Francis, 18110041
#
# Usage: python3 TCPclient_mn.py (buffer size) (server_ip_address) (filename)
# 
# Example: python3 TCPclient_mn.py 32768 127.0.0.1 Bible.txt
#
##############################################################

import socket
import os
from socket import AF_INET, SOCK_STREAM
import time
import sys
import math

# if proper arguments are not provided
if len(sys.argv) != 4:
    print("Usage:\npython3 TCPclient_mn.py buffer_size server_ip_address file_name\nExample:\npython3 TCPclient_mn.py 32768 127.0.0.1 Bible.txt")
    exit()

# buffer size in bytes
BUFFER_SIZE = int(sys.argv[1])

# server IP address
HOST = sys.argv[2]

# port number
PORT = 12345

# create the client socket
client_socket = socket.socket(AF_INET, SOCK_STREAM)

# name of the file to receieve
filename = sys.argv[3]

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
    client_socket.send("<EXIT>".encode())
    client_socket.close()
    exit()
else:
    print("File found.")

# reply that the file availability message was received
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

# inform server that client is closing
client_socket.send("<EXIT>".encode())

# close the client socket
client_socket.close()

# end timer
end_time = time.time()

# get the file size
filesize = os.path.getsize(newfilename)

# print received message
print("\n" + str(filename)  + "(" + str(filesize) + " Bytes)" + " received. Saved as " + newfilename + ". Elapsed time: " + str(end_time-start_time) + " seconds")
