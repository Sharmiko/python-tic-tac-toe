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

    def list_players(self) -> str:
        text = ''
        for row in self.players[:5]:
            text += f'{row}\n'
        return text + '...\n'

    def get_menu(self) -> str:
        text = ''
        text += 'Welcome to Tic-Tac-Toe.\n'
        text += '-' * 40 + '\n'

        text += f'Players Online: {self.players_online} (Including you).\n'
        text += f'Open Lobbies: {self.open_lobbies}\n'
        text += f'Games in progress: {self.games_in_progress}\n'
        text += '-' * 40 + '\n'

        text += 'Actions:\n'
        text += 'F - Find online match.\n'
        text += 'L - List players online.\n'
        text += 'H - Host online match.\n'
        text += 'I - Invite player to match.\n'
        text += 'S - Display your statistics.\n'

        return text
