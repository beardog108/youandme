import socket
import time
from.commands import garbage_character

from threading import Thread


def server(delay: int, controller, conn, send_data: bytearray, recv_data: bytearray):
    def send_loop():
        while True:
            time.sleep(delay)
            try:
                if not send_data:
                    conn.sendall(garbage_character)
                else:
                    char = send_data.pop(0)
                    try:
                        conn.sendall(ord(char))
                    except TypeError:
                        try:
                            conn.sendall(char)
                        except TypeError:
                            conn.sendall(chr(char).encode('utf-8'))
            except OSError:
                pass
    first_rec = True
    WELCOME_MESSAGE = "Connection established\n"
    with conn:
        Thread(target=send_loop, daemon=True).start()
        while True:
            try:
                data = conn.recv(1)
            except ConnectionResetError:
                break
            if not data: break
            if first_rec:
                for i in WELCOME_MESSAGE:
                    send_data.append(ord(i))
                first_rec = False
            if data != garbage_character and data:
                for i in data:
                    recv_data.append(i)
