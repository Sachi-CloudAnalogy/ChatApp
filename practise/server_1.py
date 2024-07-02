import socket

HOST = '192.168.56.162'
PORT = 9000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     #af_net -- means we'll be using ipv4
server.bind((HOST, PORT))
server.listen(5)

print(f"Server started at {HOST}:{PORT} and waiting for connection...")

try:
    while True:
        communication_socket, address = server.accept()
        print(f"Connected to {address}")
        
        try:
            message = communication_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Message from client is: {message}")
                communication_socket.send("got the message!!".encode('utf-8'))
            else:
                print("Received empty message, closing connection.")
        except Exception as e:
            print(f"An error occurred while receiving/sending data: {e}")
        finally:
            communication_socket.close()
            print(f"Connection with {address} ended!")
except KeyboardInterrupt:
    print("Server is shutting down...")
finally:
    server.close()
    print("Server closed.")
