import unittest
import socket
from threading import Thread
import tempfile
import time
import stem
import stem.process
from stem.control import Controller
from youandme import server

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

with tempfile.TemporaryDirectory() as tmpdirname:
    stem.process.launch_tor_with_config(
    config = {
        'ControlPort':  control_port,
        'SocksPort': socks_port,
        'DataDirectory': tmpdirname

    }, take_ownership=True, init_msg_handler=lambda i: print(i))

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

class TestServer(unittest.TestCase):

    def test_server(self):
        send_data = bytearray()
        recv_data = bytearray()
        with Controller.from_port(port=int(control_port)) as controller:
            controller.authenticate()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                ip = '127.0.0.1'
                s.bind((ip, 0))
                s.listen(1)
                port = s.getsockname()[1]
                print(port)
                serv = controller.create_ephemeral_hidden_service(
                    {1337: f'{ip}:{port}'},
                    key_content='ED25519-V3',
                    await_publication=True,
                )
                Thread(target=send_test_data, args=[ip, port], daemon=True).start()
                conn, addr = s.accept()
                Thread(target=server.server, args=[0.1, controller, conn, send_data, recv_data, Connection], daemon=True).start()
                time.sleep(1)
                max_iters = 10000000
                c = 0
                tested = False
                filler_rec = False
                while True:
                    c += 1
                    if c >= max_iters:
                        break
                    try:
                        char = chr(recv_data.pop(0)).encode('utf8')
                        if char != b'\n':
                            tested = True
                            self.assertIn(char, b"testtest2")
                    except IndexError:
                        pass
                    else:
                        pass
                    if send_data:
                        print(send_data)
                if not tested:
                    raise ValueError('not tested')

unittest.main()