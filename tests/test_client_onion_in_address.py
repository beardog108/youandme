import unittest
import socket
from threading import Thread
import sys
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

class Address:
    address = ""

def fake_server():
    with Controller.from_port(port=int(control_port)) as controller:
        controller.authenticate()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            ip = '127.0.0.1'
            s.bind((ip, 0))
            s.listen(1)
            port = s.getsockname()[1]
            serv = controller.create_ephemeral_hidden_service(
                    {1337: '127.0.0.1:' + str(port)},
                    key_content='ED25519-V3',
                    await_publication=True,
                )
            Address.address = serv.service_id + '.onion'
            conn, addr = s.accept()
            while True:
                conn.send(chr(116).encode('utf-8'))
                data = conn.recv(1)


class TestClient(unittest.TestCase):

    def test_client(self):
        Thread(target=fake_server, daemon=True).start()
        send_data = bytearray()
        recv_data = bytearray()
        while Address.address == "":
            time.sleep(1)
        print(Address.address)
        Thread(target=client.client, args=[0.01, Address.address, int(socks_port), send_data, recv_data, Connection], daemon=True).start()
        start = time.time()
        try:
            while True:
                try:
                    if chr(recv_data.pop(0)) in "t"*100:
                        break
                except IndexError:
                    self.assertLess((time.time() - start), 20)
                    time.sleep(0.01)
        except KeyboardInterrupt:
            raise

unittest.main()