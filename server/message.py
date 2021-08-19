import socket
import selectors
from game.menu import Menu


class Message:

    def __init__(
        self,
        selector: selectors.DefaultSelector,
        sock: socket.socket,
        addr
    ) -> None:
        self.selector = selector
        self.sock = sock
        self.addr = addr

        self.menu = Menu()

        self._recv_buffer = b''
        self._send_buffer = b''
        self._json_header_len = None
        self.json_header = None
        self.request = None
        self.response_created = None

    def process_events(self, mask: int) -> None:
        if mask & selectors.EVENT_READ:
            pass
        if mask & selectors.EVENT_WRITE:
            self.write()

    def write(self):
        self.sock.sendall(self.menu.get_menu())
