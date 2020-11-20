import socket
import os
from socket import AF_INET, SOCK_STREAM
import sys
import _thread
import time

if len(sys.argv) != 2:
    print("Usage:\npython3 TCPserver_thread.py buffer_size\nExample:\npython3 TCPserver_thread.py 32")
    exit()

BUFFER_SIZE = int(sys.argv[1])

HOST = "127.0.0.1"
PORT = 12345

# function that handles a client
def handle_client(client_socket):
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
        
        time.sleep(0.3)
        # inform the client about the file size 
        client_socket.send(str(filesize).encode())
        time.sleep(0.3)

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

    # create thread to handle the client and go back to waiting for the next connection
    _thread.start_new_thread(handle_client, (client_socket,))

# close the socket
server_socket.close()


