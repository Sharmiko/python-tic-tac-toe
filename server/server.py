import socket
import selectors
from typing import Dict

from conf import HOST, PORT
from server.message import Message


class Server:

    def __init__(self) -> None:
        self.sock: socket.socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM
        )
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((HOST, PORT))
        self.sock.listen()
        self.sock.setblocking(False)

        self.sel = selectors.DefaultSelector()
        self.sel.register(self.sock, selectors.EVENT_READ, data=None)

        # keep track of connected clients
        self.sessions: Dict[socket.socket] = {}
        self.num_connections = 0

        self.is_updated = False

    def close(self):
        self.sel.close()
        self.sock.close()

    def run(self) -> None:
        try:
            while True:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    # handle new connection
                    if key.data is None:
                        self.connect(sock=key.fileobj)
                    # serve existing connection
                    else:
                        message = key.data
                        message.process_events(mask)
        except KeyboardInterrupt:
            self.close()

    def connect(self, sock: socket.socket) -> None:
        conn, addr = sock.accept()
        print('Accepted from', addr)
        conn.setblocking(False)
        message = Message(selector=self.sel, sock=conn, addr=addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(fileobj=conn, events=events, data=message)


