import socket
import os
from socket import AF_INET, SOCK_STREAM
import sys

if len(sys.argv) != 4:
    print("Usage:\npython3 TCPserver_persistent.py buffer_size disable_nagle?(y/n) disable_delayed_ack?(y/n)\nExample:\npython3 TCPserver_persistent.py 32 y y")
    exit()

BUFFER_SIZE = int(sys.argv[1])

HOST = "127.0.0.1"
PORT = 12345

# list of active children
active_child_processes = []

# function to clear dead child processes
def clear_child_processes():
    while active_child_processes:
        pid, stat = os.waitpid(0, os.WNOHANG)
        if not pid:
            break
        active_child_processes.remove(pid)

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
        
        client_socket.send("<FIN>".encode())

        # print sent message
        print("\n" + str(filename)  + "(" + str(filesize) + " Bytes)" + " sent.")

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

while True:
    print("[*] Listening as " + str(HOST) + " : " + str(PORT))

    # accept connection
    client_socket, address = server_socket.accept() 
    print("[+] " + str(address) + " is connected.")

    # clean exited child processes
    clear_child_processes()

    # create child process
    child_pid = os.fork()

    if child_pid:
        # parent process - add to list and wait for connection
        active_child_processes.append(child_pid)
    else:
        # child process - handle the client
        handle_client(client_socket)

# close the socket
server_socket.close()


