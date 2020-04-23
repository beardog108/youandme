#!/usr/bin/env python3
import sys
import socket
from time import time, sleep
from threading import Thread
import tempfile
import argparse

from stem.control import Controller

try:
    from youandme.tor import launch_tor
except ModuleNotFoundError:
    pass

from youandme.server import server
from youandme.client import client

class _Address:
    address = ""

def _get_open_port():
    # taken from (but modified) https://stackoverflow.com/a/2838309 by https://stackoverflow.com/users/133374/albert ccy-by-sa-3 https://creativecommons.org/licenses/by-sa/3.0/
    # changes from source: import moved to top of file, bind specifically to localhost
    # vulnerable to race condition
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1",0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port

def connector(host, send_data, recv_data, address="", control_port=1337, socks_port=1338):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', socks_port))
    if result != 0:
        try:
            launch_tor(control_port=control_port, socks_port=socks_port)
        except OSError:
            with tempfile.TemporaryDirectory() as tmpdirname:
                launch_tor(control_port=control_port, socks_port=socks_port, data_dir=tmpdirname)
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
            break
PORT_MESSAGE = "Specify any free ports above 1023"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='End-to-end encrpyted instant messaging with metadata privacy and perfect forward secrecy')
    parser.add_argument('connection', choices=['host', 'conn'])
    parser.add_argument('--socks-port', help='Socks proxy port (will use random if not given)', default=0, type=int)
    parser.add_argument('--control-port', help='Tor control port (will use random if not given)', default=0, type=int)
    parser.add_argument('--address', help='Address to connect to. No port.', default='')
    args = parser.parse_args()

    if args.socks_port == 0: args.socks_port = _get_open_port()
    if args.control_port == 0: args.control_port = _get_open_port()
    send_data = bytearray()
    recv_data = bytearray()
    if args.connection == 'conn':
        if not args.address:
            print("Must specify address if connecting (--address)", file=sys.stderr)
            sys.exit(3)
        Thread(target=connector,
               args=[False, send_data, recv_data],
               kwargs={'address':  args.address,
                       'socks_port': args.socks_port,
                        'control_port': args.control_port}, daemon=True).start()
        chat('conn', send_data, recv_data)
    else:
        Thread(target=connector, args=[True, send_data, recv_data],
               kwargs={'socks_port': args.socks_port,
                        'control_port': args.control_port}, daemon=True).start()
        chat('host', send_data, recv_data)