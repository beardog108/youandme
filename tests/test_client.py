import unittest
import socket
from threading import Thread
import time
import stem
import stem.process
from stem.control import Controller
from youandme import client

control_port = str(1353)
socks_port = str(1354)

stem.process.launch_tor_with_config(
config = {
    'ControlPort':  control_port,
    'SocksPort': socks_port,
    'Log': [
    'NOTICE stdout'
    ],
}, take_ownership=True)

def send_test_data(ip, port):
    time.sleep(2)
    s = socket.socket()
    s.connect(('127.0.0.1', port))
    while True:
        s.send(b"test")
        for c in b"test2":
            try:
                s.send(chr(c).encode('utf8'))
            except TypeError:
                print(c)
    s.close()

class TestClient(unittest.TestCase):

    def test_client(self):
        send_data = bytearray()
        recv_data = bytearray()
        #client(1, )

unittest.main()