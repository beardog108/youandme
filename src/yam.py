import sys
import socket
from time import time, sleep
from threading import Thread

from getch import getch
from stem.control import Controller

try:
    from youandme.tor import launch_tor
except ModuleNotFoundError:
    pass

from youandme.server import server
from youandme.client import client

class _Address:
    address = ""


def connector(host, send_data, recv_data, address="", control_port=1337, socks_port=1338):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', socks_port))
    if result != 0:
        launch_tor(control_port=control_port, socks_port=socks_port)
    if host:
        with Controller.from_port(port=control_port) as controller:
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
                _Address.address = serv.service_id
                conn, addr = s.accept()
                server(0.01, controller, conn, send_data, recv_data)
    else:
        if not address.endswith('.onion'):
            address += '.onion'
        client(0.01, address, socks_port, send_data, recv_data)


def chat(mode, send_data, recv_data):
    display_buffer = []
    if mode == 'host':
        while _Address.address == "":
            sleep(0.01)
        print(_Address.address)
    def display_new():
        while True:
            try:
                char = chr(recv_data.pop(0))
                display_buffer.append(char)
                if char == "\n" or char == "\r\n" or len(display_buffer) > 100:
                    #print("\033[1;33m", char, "\033[0m", end="\n")
                    while len(display_buffer) != 0:
                        #print("\033[1;33m", display_buffer.pop(0), "\033[0m", end='')
                        print("\033[1;33m" + display_buffer.pop(0) + "\033[0m", end="")

            except IndexError:
                pass
            sleep(0.1)
    Thread(target=display_new, daemon=True).start()
    def make_message():
        while True:
            new = input("\033[0m").encode('utf-8')
            for b in new:
                send_data.append(b)
            send_data.append(ord(b"\n"))
    Thread(target=make_message, daemon=True).start()
    while True:
        try:
            if send_data is None:
                print("Well crap, we lost connection.")
                break
            sleep(1)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'chat':
            send_data = bytearray()
            recv_data = bytearray()
            if sys.argv[2] == 'host':
                Thread(target=connector, args=[True, send_data, recv_data], kwargs={'socks_port': int(input("socks")), 'control_port': int(input('control port'))}, daemon=True).start()
            elif sys.argv[2].startswith('conn'):
                Thread(target=connector, args=[False, send_data, recv_data], kwargs={'address':  sys.argv[3], 'socks_port': int(input("socks")), 'control_port': int(input('control port'))}, daemon=True).start()
            else:
                print('Must specify host or conn')
                sys.exit(1)
            chat(sys.argv[2], send_data, recv_data)
