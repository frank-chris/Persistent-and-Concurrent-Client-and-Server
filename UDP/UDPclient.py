import socket
import os
from socket import AF_INET, SOCK_DGRAM
import time
import sys

BUFFER_SIZE = int(sys.argv[1])

HOST = "127.0.0.1"
PORT = 12345

# create the client socket
client_socket = socket.socket(AF_INET, SOCK_DGRAM)

# ask user for the name of the file to receieve
filename = input("Which file do you want to receive? ")

# create the name with which the file is to be saved
newfilename = filename.split('.')[0] + "UDP" + str(os.getpid()) + "." + filename.split('.')[1]

# start timer
start_time = time.time()
flag = 0

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
            # end timer
            end_time = time.time()
            flag = 1
            if not bytes_read:    
                # nothing is received means that file transmitting is done
                break
            # write to the file
            f.write(bytes_read)
        except socket.timeout:
            print("\nTime out: Closing socket")
            break

# close the client socket
client_socket.close()

# end timer
if (flag == 0):
    end_time = time.time()

# get the file size
filesize = os.path.getsize(newfilename)

# print received message
print("\n" + str(filename)  + "(" + str(filesize) + " Bytes)" + " received. Saved as " + newfilename)

# print elapsed time
print("Elapsed time: " + str(end_time-start_time))