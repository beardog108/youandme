from base64 import b85encode, b85decode
from time import sleep
import sys
from typing import Union

from youandme.commands import terminator

_b85alphabet = bytearray(b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                b"abcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~")


def decoded_recv_stream(raw_stream: bytearray, delay_seconds: int) -> bytes:
    while True:
        for byte in raw_stream:
            if byte == terminator:
                raw_stream.pop()
                yield b85decode(raw_stream)
                raw_stream.clear()
                continue
        sleep(delay_seconds)


def encode_and_send(send_stream: bytearray, data: Union[bytes, str]):
    try:
        data = data.encode('utf-8')
    except AttributeError:
        pass
    encoded = b85encode(data)
    for c in encoded:
        send_stream.append(c)

    send_stream.append(terminator)

