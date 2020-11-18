import socket
import os
from socket import AF_INET, SOCK_DGRAM
import time
import sys

if len(sys.argv) != 2:
    print("Usage:\npython3 UDPclient_persistent.py buffer_size")
    exit()

BUFFER_SIZE = int(sys.argv[1])

HOST = "127.0.0.1"
PORT = 12345

# create the client socket
client_socket = socket.socket(AF_INET, SOCK_DGRAM)

while True:
    # ask user for the name of the file to receieve
    filename = input("Which file do you want to receive?\n(Enter '<EXIT>' to close the socket and exit)\n")
  
    if ("." not in filename) and (filename != "<EXIT>"):
        print("Invalid filename")
        continue

    # send the filename to the server
    client_socket.sendto(str(filename).encode(), (HOST, PORT))

    # exit the loop
    if filename == "<EXIT>":
        print("Closing the socket and exiting")
        time.sleep(2)
        break

    # create the name with which the file is to be saved
    newfilename = filename.split('.')[0] + "UDP" + str(os.getpid()) + "." + filename.split('.')[1]

    try:
        # 3 seconds time out
        client_socket.settimeout(3)
        # receive the message from server indicating whether requested file is available or not
        availability, address = client_socket.recvfrom(1024)
        availability = availability.decode()
        if availability == "<NOTFOUND>":
            print("File not available.")
            continue
        else:
            print("File found.")
    except socket.timeout:
        print("\nTime out: Closing socket")
        # close the client socket
        client_socket.close()
        exit()

    start_time = time.time()

    # start receiving the file and writing into a file
    print("Receiving " + str(filename), end ="...")
    with open(newfilename, "wb") as f:
        while True:
            try:
                # 3 seconds time out
                client_socket.settimeout(3)
                bytes_read, address = client_socket.recvfrom(BUFFER_SIZE)
                if bytes_read == "<FIN>".encode():    
                    # file transmitting is done
                    break
                # write to the file
                f.write(bytes_read)
            except socket.timeout:
                print("\nTime out: Closing socket")
                break

    end_time = time.time()

    # get the file size
    filesize = os.path.getsize(newfilename)

    # print received message
    print("\n" + str(filename)  + "(" + str(filesize) + " Bytes)" + " received in " + str(end_time-start_time) + " seconds. Saved as " + newfilename)

# close the client socket
client_socket.close()