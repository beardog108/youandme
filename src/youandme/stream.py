from base64 import b85encode, b85decode
from time import sleep

from youandme.commands import terminator

_b85alphabet = (b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                b"abcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~")


def decoded_recv_stream(raw_stream: bytearray, delay_seconds: int, max_buffer_size=) -> bytes:
    while True:
        for byte in raw_stream:
            if byte == terminator:
                yield b85decode(raw_stream[:len(raw_stream) - 1])
                raw_stream.clear()
                continue
            if byte not in _b85alphabet:
                raise ValueError('Not valid base85 encoding')
        sleep(delay_seconds)
