import socket
import time
from threading import Thread
import typing

if typing.TYPE_CHECKING:
    from stem.control import Controller

from.commands import garbage_character
from.commands import WELCOME_MESSAGE


def server(delay: int, controller: 'Controller', socket_conn, send_data: bytearray, recv_data: bytearray, connection: "Connection"):
    def send_loop():
        while True:
            time.sleep(delay)
            try:
                if not send_data:
                    socket_conn.sendall(garbage_character)
                else:
                    char = send_data.pop(0)
                    try:
                        socket_conn.sendall(ord(char))
                    except TypeError:
                        try:
                            socket_conn.sendall(char)
                        except TypeError:
                            socket_conn.sendall(chr(char).encode('utf-8'))
            except OSError:
                connection.connected = False
    first_rec = True
    with socket_conn:
        Thread(target=send_loop, daemon=True).start()
        while True:
            try:
                data = socket_conn.recv(1)
            except ConnectionResetError:
                connection.connected = False
                break
            if not data: break
            if first_rec:
                for i in WELCOME_MESSAGE:
                    send_data.append(ord(i))
                first_rec = False
            if data != garbage_character and data:
                for i in data:
                    recv_data.append(i)
