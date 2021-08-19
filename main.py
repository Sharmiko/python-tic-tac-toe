import sys
import atexit
from server.server import Server
from client.client import Client


def main() -> None:

    args = sys.argv
    if len(args) != 2:
        raise Exception('Socket type must be specified.')

    type_ = args[1]
    if type_ == 'server':
        server = Server()
        server.run()
        atexit.register(server.close)
    elif type_ == 'client':
        client = Client()
        client.run()
    else:
        raise ValueError(
            'Incorrect socket type specified. Must be "server" or "client"'
        )


if __name__ == '__main__':
    main()
