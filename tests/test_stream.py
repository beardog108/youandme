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
            self.assertNotIn(terminator, message)
            break


    def test_stream_send(self):
        send_data = bytearray()
        recv_data = bytearray()
        data = "hello world"
        data_bytes = data.encode('utf-8')
        encoded = b85encode(data_bytes)

        stream.encode_and_send(send_data, data)
        for i in send_data:
            if i != terminator:
                self.assertIn(chr(i).encode('utf-8'), encoded)

        self.assertEqual(data_bytes, b85decode(send_data[:len(send_data) - 1]))


    def test_stream_send_has_terminator(self):
        send_data = bytearray()
        recv_data = bytearray()
        data = "hello world"
        data_bytes = data.encode('utf-8')
        encoded = b85encode(data_bytes)

        stream.encode_and_send(send_data, data)

        self.assertEqual(send_data.pop(), terminator)



unittest.main()