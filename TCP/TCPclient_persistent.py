#############################################################################
#
# Persistent TCP Client Script written for Assignment - 4 
# 
# Author: Chris Francis, 18110041
#
# Usage: python3 TCPclient_persistent.py (buffer size) (filename) [filename ...]
# 
# Example: python3 TCPclient_persistent.py 32768 Bible.txt Ramayana.txt
#
#############################################################################

import socket
import os
from socket import AF_INET, SOCK_STREAM
import time
import sys
import math

# if proper arguments are not provided
if (len(sys.argv) <= 2) or not((sys.argv[1]).isnumeric()):
    print("Usage:\npython3 TCPclient_persistent.py buffer_size file_name [file_name ...]\nExample:\npython3 TCPclient_persistent.py 32 Bible.txt Ramayana.txt")
    exit()

# buffer size in bytes
BUFFER_SIZE = int(sys.argv[1])

# server IP address
HOST = "127.0.0.1"

# port number
PORT = 12345

# create the client socket
client_socket = socket.socket(AF_INET, SOCK_STREAM)

start_time = time.time()

# establishing connection
print("[+] Connecting to " + str(HOST) + " : " + str(PORT))
client_socket.connect((HOST, PORT))

end_time = time.time()

print("[+] Connected(took " + str(end_time-start_time) + " seconds).")

# loop through filenames
for filename in sys.argv[2:]:
    if ("." not in filename) and (filename != "<EXIT>"):
        print("Invalid filename")
        continue
    
    # create the name with which the file will be saved
    newfilename = filename.split('.')[0] + "TCP" + str(os.getpid()) + "." + filename.split('.')[1]

    start_time = time.time()

    # send the filename to the server
    client_socket.send((str(filename)).encode())

    # receive the message from server indicating whether requested file is available or not
    availability = client_socket.recv(1024).decode()
    if availability == "<NOTFOUND>":
        print("File not available.")
        continue
    else:
        print("File found.")

    # reply that file availability was received
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
                # file transmitting is done
                break
            # write to the file
            f.write(bytes_read)

    end_time = time.time()

    # get the file size
    filesize = os.path.getsize(newfilename)

    # print received message
    print("\n" + str(filename)  + "(" + str(filesize) + " Bytes)" + " received in " + str(end_time-start_time) + " seconds. Saved as " + newfilename)

# inform server that client is closing
client_socket.send("<EXIT>".encode())

# close the client socket
client_socket.close()