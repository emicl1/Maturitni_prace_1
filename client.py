import socket
from json import loads

PORT = 8880
HOST = "0.0.0.0"
IP = "192.168.0.177"


"""s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
while True:
    print("Sending")
    while True:
        msg = input("Enter message: ")
        if msg == "close":
            s.shutdown(socket.SHUT_RDWR)
            s.close()
            break
        if msg == "send":
            try:
                s.sendall(msg.encode("utf-8"))
                data = s.recv(1024)
                print(data)
            except:
                print("Connection lost")
                break
        else:
            continue
"""

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
























