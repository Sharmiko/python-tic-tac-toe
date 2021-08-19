import socket
import selectors


from conf import HOST, PORT
from client.message import Message


class Client:

    def __init__(self) -> None:
        self.sel = selectors.DefaultSelector()

    def __close(self) -> None:
        self.sel.close()

    def run(self) -> None:
        self.connect()

        try:
            while True:
                events = self.sel.select(timeout=1)
                if events:
                    for key, mask in events:
                        message = key.data
                        message.process_events(mask)
                if not self.sel.get_map():
                    break
        except KeyboardInterrupt:
            print('Exiting')
        finally:
            self.sel.close()

    def connect(self) -> None:
        addr = (HOST, PORT)
        print('Starting connection to', addr)

        sock = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM
        )
        sock.setblocking(False)
        sock.connect_ex(addr)

        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = Message(selector=self.sel, sock=sock, addr=addr, request={
            'Test': None
        })
        self.sel.register(fileobj=sock, events=events, data=message)
