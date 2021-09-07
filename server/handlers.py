import socket


class ActionHandler:

    def handle_input(self, inp: str, conn: socket.socket):
        if inp not in ['F', 'L', 'H', 'I', 'S', 'M']:
            return 'Invalid input.'
        return self._handle_input(inp=inp, conn=conn)

    def _handle_input(self, inp: str, conn: socket.socket):
        if inp == 'F':
            self._find_match(conn)
        elif inp == 'L':
            return self._list_players()
        elif inp == 'M':
            return self.menu.get_menu()
        else:
            return 'Action not supported yet.'

    def _find_match(self, conn: socket.socket) -> None:
        if self.queue.qsize() > 0:
            pair = self.queue.get()
            print('Found pair')
            print(self.sessions[pair])
            print(self.sessions[conn])
        else:
            self.queue.put(conn)

    def _list_players(self) -> str:
        text = self.menu.list_players()
        text += '\nAction:\nM - Return to menu\n'
        return text
