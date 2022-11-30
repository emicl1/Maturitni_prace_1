"""
Tento script je psán v micropythnu a slouží k ovládání serveru
"""
# ESP-32 Server side
import socket
import network
from machine import Pin, I2C, SoftI2C
import ADXL345  # https://github.com/DFRobot/micropython-dflib/tree/master/ADXL345
import time
from json import dumps

PORT = 8880
HOST = "0.0.0.0"
IP = "192.168.0.177"


def do_connect(ssid, password):
    """
    Connects to wifi and after successfull connection will synchronize the time over NTP.
    """
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print(f'Network config: {wlan.ifconfig()}')


if __name__ == '__main__':
    do_connect("Gottvaldova", "ivana1234")
    i2c = SoftI2C(scl=Pin(17), sda=Pin(16), freq=10000)
    adx = ADXL345.ADXL345(i2c)
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.bind((HOST, PORT))
    soc.listen(100)
    while True:
        print("wating for request")
        conn, address = soc.accept()
        while True:
            data = conn.recv(2048)
            data = data.decode("utf-8")
            print(data)
            if data == None:
                conn.close()
                soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                break
            if data == "send":
                x = adx.xValue
                y = adx.yValue
                z = adx.zValue
                data = dumps((x, y, z))
                conn.sendall(data.encode("utf-8"))
            elif data == "close":
                print("close")
                conn.close()
                soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                break

    # do_connect("Gottvaldova ", "ivana1234")























