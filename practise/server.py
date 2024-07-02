import socket

HOST = '192.168.56.162'
# can run it on localhost
PORT = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen(5)

while True:
    communication_socket, address = server.accept()
    print(f"Connected to {address}")
    message = communication_socket.recv(1024).decode('utf-8')
    print(f"Message from client is: {message}")
    communication_socket.send(f"got the message!!".encode('utf-8'))
    communication_socket.close()
    print(f"Connection with {address} ended!")
