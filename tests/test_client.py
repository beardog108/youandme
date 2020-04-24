import unittest
import socket
from threading import Thread
import time
import stem
import stem.process
from stem.control import Controller
from youandme import client

class Connection:
    connected = True

def get_open_port():
    # taken from (but modified) https://stackoverflow.com/a/2838309 by https://stackoverflow.com/users/133374/albert ccy-by-sa-3 https://creativecommons.org/licenses/by-sa/3.0/
    # changes from source: import moved to top of file, bind specifically to localhost
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1",0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port

control_port = str(get_open_port())
socks_port = str(get_open_port())
assert control_port != socks_port

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