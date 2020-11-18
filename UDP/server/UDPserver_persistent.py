import socket
import os
from socket import AF_INET, SOCK_DGRAM
import sys

if len(sys.argv) != 2:
    print("Usage:\npython3 UDPserver_persistent.py buffer_size")
    exit()

BUFFER_SIZE = int(sys.argv[1])

HOST = "127.0.0.1"
PORT = 12345

# creating server socket
server_socket = socket.socket(AF_INET, SOCK_DGRAM)

# bind the socket to our local address
server_socket.bind((HOST, PORT))

while True:
    # print that server is ready
    print("[*] Ready to receive as " + str(HOST) + " : " + str(PORT))

    while True:
        # receive the filename to be sent to client
        received, client_address = server_socket.recvfrom(1024)
        filename = received.decode()

        # exit the loop
        if filename == "<EXIT>":
            print("Client exited.")
            break

        filename = os.path.basename(filename)

        # check if requested file is available or not and inform client
        try:
            filesize = os.path.getsize(filename)
            print("File is available.")
            server_socket.sendto("<FOUND>".encode(), client_address)
        except FileNotFoundError:
            print("File not available.")
            server_socket.sendto("<NOTFOUND>".encode(), client_address)
            continue

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

        server_socket.sendto("<FIN>".encode(), client_address)

        # print sent message
        print("\n" + str(filename)  + "(" + str(filesize) + " Bytes)" + " sent.")

# close the socket
server_socket.close()


