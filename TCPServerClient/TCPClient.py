import socket
import datetime


print('The client started at', str(datetime.datetime.now()))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.connect(('192.168.100.2', 50000))
    server.sendall(b'Hello TCP')

    print(server.recv(1024).decode())
