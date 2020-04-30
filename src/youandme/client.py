from threading import Thread
from time import sleep

import socks

from .commands import garbage_character


def client(delay: int, hs_id: str, socks_port, send_data: bytearray, recv_data: bytearray, connection: "Connection"):
    s = socks.socksocket() # Same API as socket.socket in the standard lib

    s.set_proxy(socks.SOCKS5, "127.0.0.1", socks_port, rdns=True)

    if not hs_id.endswith('.onion'):
        hs_id += '.onion'

    def send_loop():
        while True:
            to_send = None
            if send_data:
                char = send_data.pop(0)
                to_send = char
            else:
                to_send = garbage_character
            try:
                s.send(chr(to_send).encode('utf-8'))
            except TypeError:
                try:
                    if to_send is not None:
                        s.send(to_send)
                except BrokenPipeError:
                    # lost connection
                    connection.connected = False
            except BrokenPipeError:
                connection.connected = False
            sleep(delay)

    # Can be treated identical to a regular socket object
    s.connect((hs_id, 1337))
    Thread(target=send_loop, daemon=True).start()
    while True:
        data = s.recv(1)
        if data != garbage_character:
            try:
                recv_data.append(data)
            except TypeError:
                if data:
                    recv_data.append(ord(data))
