import os
import socket
import selectors


class Message:

    def __init__(
        self,
        selector: selectors.DefaultSelector,
        sock: socket.socket,
        addr,
        request
    ) -> None:
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self.request = request

        self._recv_buffer = b''
        self._send_buffer = b''
        self._request_queued = False
        self._json_header_len = None
        self._json_header = None
        self.response = None

    def process_events(self, mask: int) -> None:
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            pass

    def read(self):
        recv_data = self.sock.recv(1024)
        if recv_data:
            print(recv_data.decode(), sep='', end='\r', flush=True)
