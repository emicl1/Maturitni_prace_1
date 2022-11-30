

from client import client

while True:
    for data in client():
        print(data)