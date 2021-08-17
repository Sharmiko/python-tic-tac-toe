import atexit
from server import Server


def main() -> None:
    server = Server()
    server.run()

    atexit.register(server.close())


if __name__ == '__main__':
    main()
