import socket
import time

from stem.control import Controller
from threading import Thread


def server():
    send_data = bytearray()
    def send_loop(conn):
        while True:
            time.sleep(0.1)
            if not send_data:
                conn.sendall(bytes([55]))
            else:
                conn.sendall(send_data.pop(0))
    with Controller.from_port(port=1338) as controller:
        controller.authenticate()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            ip = '127.0.0.1'
            s.bind((ip, 0))
            s.listen(1)
            port = s.getsockname()[1]
            serv = controller.create_ephemeral_hidden_service({
            1337: f'{ip}:{port}'},
            key_content = 'ED25519-V3',
            await_publication = True,
            )
            print('on', serv.service_id, 'to', ip, port)
            conn, addr = s.accept()
            with conn:
                Thread(target=send_loop, args=[conn], daemon=True).start()
                print('Connected by', addr)
                while True:
                    data = conn.recv(1)
                    if not data: break
                    data = data.strip()
                    if data != bytes([55]):
                        print(data)
                    #conn.sendall(data)

