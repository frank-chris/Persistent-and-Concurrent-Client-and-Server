##############################################################
#
# UDP Client Script written for Assignment - 3 and used 
# in Q1 of Assignment - 4 
# 
# Author: Chris Francis, 18110041
#
# Usage: python3 UDPclient.py (buffer size) (filename)
# 
# Example : python3 UDPclient.py 32768 Bible.txt
#
##############################################################

import socket
import os
from socket import AF_INET, SOCK_DGRAM
import time
import sys

# buffer size in bytes
BUFFER_SIZE = int(sys.argv[1])

# server IP address
HOST = "127.0.0.1"

# port number
PORT = 12345

# create the client socket
client_socket = socket.socket(AF_INET, SOCK_DGRAM)

# name of the file to receive
filename = sys.argv[2]

# create the name with which the file is to be saved
newfilename = filename.split('.')[0] + "UDP" + str(os.getpid()) + "." + filename.split('.')[1]

# start timer
start_time = time.time()

# send the filename to the server
client_socket.sendto(str(filename).encode(), (HOST, PORT))

try:
    # 3 seconds time out
    client_socket.settimeout(3)
    # receive the message from server indicating whether requested file is available or not
    availability, address = client_socket.recvfrom(1024)
    availability = availability.decode()
    if availability == "<NOTFOUND>":
        print("File not available.")
        client_socket.close()
        exit()
    else:
        print("File found.")
except socket.timeout:
    print("\nTime out: Closing socket")
    # close the client socket
    client_socket.close()
    exit()

# start receiving the file and writing into a file
print("Receiving " + str(filename), end ="...")
with open(newfilename, "wb") as f:
    while True:
        try:
            # 3 seconds time out
            client_socket.settimeout(3)
            bytes_read, address = client_socket.recvfrom(BUFFER_SIZE)
            if not bytes_read:    
                # nothing is received means that file transmitting is done
                break
            # write to the file
            f.write(bytes_read)
            end_time = time.time()
        except socket.timeout:
            print("\nTime out: Closing socket")
            break

close_time = time.time()

# close the client socket
client_socket.close()    

close_connection_time = time.time() - close_time

# get the file size
filesize = os.path.getsize(newfilename)

# print received message
print("\n" + str(filename)  + "(" + str(filesize) + " Bytes)" + " received. Saved as " + newfilename)

# print elapsed time
print("Elapsed time: " + str((end_time-start_time)+close_connection_time))