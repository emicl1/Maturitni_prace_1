import socket
import time
from multiprocessing import Process, Queue
PORT = 8880
HOST = "0.0.0.0"
IP = "192.168.0.177"

queue = Queue()

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
            queue.put(data)
            print(data)
























