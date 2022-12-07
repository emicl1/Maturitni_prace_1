import socket
from json import loads

PORT = 8880
HOST = "0.0.0.0"
IP = "192.168.0.177"

def client(queue):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    while True:
        print("Sending")
        while True:
            msg = "send"
            s.sendall(msg.encode("utf-8"))
            data = s.recv(1024)
            data = data.decode("utf-8")
            data = loads(data)
            queue.put(data)
























