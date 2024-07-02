import socket

HOST = '192.168.56.162'       
PORT = 9000

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))
message = "Hey, start sending messages!!"

try:
    while True:
        socket.send(message.encode('utf-8'))
        print(socket.recv(1024).decode('utf-8'))
        more = input("More messages to send ? ")
        if more.lower() == 'y':
            message = input("Enter message here")
        else:
            break
except KeyboardInterrupt:
    print("Ended by user")
finally:
    socket.close()                
    print("Connection closed.")
     
 