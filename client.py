import types
import socket
import selectors


from conf import HOST, PORT


class Client:

    def __init__(self) -> None:
        self.sel = selectors.DefaultSelector()

    def run(self) -> None:
        self.connect()

        try:
            while True:
                events = self.sel.select(timeout=1)
                if events:
                    for key, mask in events:
                        # serve connections
                        pass

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
        data = types.SimpleNamespace(
            recv_total=0,
            outb=b''
        )
        self.sel.register(fileobj=sock, events=events, data=data)
