import sys
import time
import socket
import struct
from typing import Dict


from conf import HOST, PORT
from base.message import MessageMixin
from utils.utils import print_flush, std_input


class Client(MessageMixin):

    def __init__(self) -> None:
        addr = (HOST, PORT)
        print('Starting connection to', addr)

        self.sock = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM
        )
        self.sock.connect_ex(addr)
        self.sock.setblocking(False)

    def __del__(self) -> None:
        self.sock.close()

    def write(self) -> None:
        inp = std_input()
        self.sock.send(self.create_message({
            'input_message': inp
        }))

    def run(self) -> None:
        while True:
            try:
                data = self.read_message(self.sock)
                if data:
                    print_flush(data['message'])
                    if data.get('requires_input', False):
                        self.write()
                else:
                    sys.exit(-1)
            except BlockingIOError:
                continue
            except KeyboardInterrupt:
                print('Exiting')
