from typing import Optional


class Menu:

    def __init__(self):
        self.players_online = 0
        self.open_lobbies = 0
        self.games_in_progress = 0
        self.players = []

    def update(
        self,
        players_online: Optional[int] = None,
        open_lobbies: Optional[int] = None,
        games_in_progress: Optional[int] = None,
        player: Optional[str] = None
    ) -> None:
        if players_online:
            self.players_online = players_online

        if open_lobbies:
            self.open_lobbies = open_lobbies

        if games_in_progress:
            self.games_in_progress = games_in_progress

        if player:
            self.players.append(player)

    def remove_user(self, user_name: str) -> None:
        self.players.remove(user_name)
        self.players_online -= 1

    def handle_input(self, inp: str):
        if inp not in ['A', 'L', 'H', 'I', 'S', 'M']:
            return 'Invalid input.'
        return self._handle_input(inp)

    def _handle_input(self, inp: str):
        if inp == 'A':
            pass

        elif inp == 'L':
            text = self.list_players()
            text += '\nAction:\nM - Return to menu'
            return text
        elif inp == 'M':
            return self.get_menu()
        else:
            return 'Action not supported yet.'

    def list_players(self) -> str:
        text = ''
        for row in self.players[:5]:
            text += f'{row}\n'
        return text + '...\n'

    def get_menu(self) -> list:
        text = []
        text.append('Welcome to Tic-Tac-Toe.\n')
        text.append('-' * 40 + '\n')

        text.append(
            f'Players Online: {self.players_online} (Including you).\n'
        )
        text.append(f'Open Lobbies: {self.open_lobbies}\n')
        text.append(f'Games in progress: {self.games_in_progress}\n')
        text.append('-' * 40 + '\n')

        text.append('Actions:\n')
        text.append('F - Find online match.\n')
        text.append('L - List players online.\n')
        text.append('H - Host online match.\n')
        text.append('I - Invite player to match.\n')
        text.append('S - Display your statistics.\n')

        return text
