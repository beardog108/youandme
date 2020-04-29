import unittest
import socket
from threading import Thread
import sys
import time
from base64 import b85decode, b85encode
from stem.control import Controller
from youandme import stream
from youandme.commands import terminator


def add_encoded_to_bytes_array_valid(message, array: bytearray):
    for m in b85encode(message.encode('utf-8')):
        array.append(m)
    array.append(terminator)

class TestStream(unittest.TestCase):

    def test_stream_get(self):
        send_data = bytearray()
        recv_data = bytearray()

        data = "hello world"
        #stream.decoded_recv_stream(recv_data, data)
        add_encoded_to_bytes_array_valid(data, recv_data)

        c = 0
        for message in stream.decoded_recv_stream(recv_data, 1):
            self.assertEqual(message.decode('utf-8'), data)
            break



unittest.main()