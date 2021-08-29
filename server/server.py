import time
import socket
import select
from typing import Dict, List

from conf import HOST, PORT
from game.menu import Menu
from base.message import MessageMixin


class Server(MessageMixin):

    menu = Menu()

    def __init__(self) -> None:
        self.sock: socket.socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM
        )
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((HOST, PORT))
        self.sock.listen()
        self.sock.setblocking(False)

        # keep track of connected clients
        self.clients: List[socket.socket] = [self.sock]
        self.sessions: Dict[socket.socket] = {}
        self.num_connections = 0

        self.is_updated = False

    def close(self):
        self.sock.close()
        self.num_connections -= 1
        self.update_menu()

    def serve_connection(self, conn: socket.socket) -> None:
        try:
            data = self.read_message(conn)
            if data:
                if conn not in self.sessions and 'input_message' in data:
                    username = data['input_message']
                    del data['input_message']
                    self.menu.update(player=username)
                    self.sessions[conn] = username
                if 'input_message' in data:
                    res = self.menu.handle_input(data['input_message'])
                    conn.send(self.create_message({
                        'message': res
                    }))
                else:
                    conn.send(self.create_message({
                        'message': self.menu.get_menu(),
                        'requires_input': True
                    }))
        except (BlockingIOError, OSError):
            time.sleep(0.1)
        except ConnectionResetError:
            conn.close()

    def update_menu(self) -> None:
        self.menu.players_online = self.num_connections

    def run(self) -> None:
        try:
            while True:
                read_sockets, _, exception_sockets = select.select(
                    self.clients, [], self.clients
                )
                for notified in read_sockets:
                    if notified == self.sock:
                        conn, addr = self.sock.accept()
                        self.connect(conn=conn, addr=addr)
                    else:
                        self.serve_connection(conn=notified)

                for notified in exception_sockets:
                    self.clients.remove(notified)
                    if notified in self.sessions:
                        del self.sessions[notified]

        except KeyboardInterrupt:
            self.close()

    def connect(self, conn: socket.socket, addr) -> None:
        conn.setblocking(False)
        print('Accepted from', addr)
        self.clients.append(conn)
        self.num_connections += 1
        self.update_menu()
        conn.send(self.create_message({
            'message': 'Enter user name: ',
            'requires_input': True
        }))