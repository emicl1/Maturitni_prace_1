

from random import randint


data_old= 100
data = 0

while True:
    data = randint(0, 100)
    if data_old >= data:
        print("left")
        data_old = data
    elif data_old <= data:
        print("right")
        data_old = data



