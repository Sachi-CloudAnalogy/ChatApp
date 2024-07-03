import socket
import threading
import streamlit as st

HOST = '127.0.0.1'
PORT = 8000

# Creating a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect(username):
    try:
        client.connect((HOST, PORT))
        st.success("Successfully connected to server")
        client.sendall(username.encode())
    except Exception as e:
        st.error(f"Unable to connect to server {HOST}:{PORT}")
        st.error(str(e))

def send_message(message):
    try:
        client.sendall(message.encode())
    except Exception as e:
        st.error(f"Error sending message: {str(e)}")

def listen_for_messages_from_server():
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                username, content = message.split(">")
                st.text(f"[{username}] {content}")
            else:
                st.error("Message received from client is empty")
        except Exception as e:
            st.error(f"Error receiving message: {str(e)}")
            break

# Streamlit UI components
st.title("Messenger Client")

username = st.text_input("Enter username:")
if st.button("Join"):
    if username.strip() != '':
        # threading.Thread(target=connect, args=(username.strip(),)).start()
        connect(username.strip())
        st.text(f"Joined as: {username.strip()}")
        st.text("Chat Messages:")
        #threading.Thread(target=listen_for_messages_from_server).start()
        listen_for_messages_from_server()
    else:
        st.error("Username cannot be empty")

message = st.text_input("Type your message:")
if st.button("Send"):
    if message.strip() != '':
        send_message(f"{username.strip()}>{message.strip()}")
    else:
        st.error("Message cannot be empty")
