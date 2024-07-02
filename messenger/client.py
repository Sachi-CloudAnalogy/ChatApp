import socket
import threading

HOST = "127.0.0.1"
PORT = 1234

def listen_for_messages_from_server(client):
    while 1:
        message = client.recv(2048).decode("utf-8")

def communicate_to_server(client):
    username = input("Enter Username: ")
    if username != "":
        client.sendall(username.encode())
    else:
        print("Username cannot be empty")
        exit(0)    


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")
    except:
        print(f"Unable to connect to server {HOST} {PORT}")

    communicate_to_server(client)


if __name__ == "__main__":
    main()

