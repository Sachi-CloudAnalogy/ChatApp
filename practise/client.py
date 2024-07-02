import socket

HOST = '192.168.56.162'       #search at myip.is for internet but for running locally on your system write same as server.
# host of the server
PORT = 8000

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))

socket.send("Hello World!".encode('utf-8'))
print(socket.recv(1024).decode('utf-8'))
 