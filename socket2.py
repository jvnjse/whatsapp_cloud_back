# client.py
import socket

HOST = "127.0.0.1"  # Server IP address
PORT = 8080  # Server port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = s.recv(1024)

print("Received", repr(data))
