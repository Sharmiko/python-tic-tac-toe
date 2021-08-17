from typing import List


class Board:

    def __init__(self, width: int = 3, height: int = 3) -> None:
        assert width == height, 'Board dimensions must be square.'
        self.width = width
        self.height = height
        self.board_data = self.setup_board()

        self.margin = 3

    def setup_board(self) -> List:
        data = []
        for _ in range(self.height):
            temp = []
            for _ in range(self.width):
                temp.append(' ')
            data.append(temp)
        return data

    def draw(self) -> None:
        char_idx = ord('A')

        board = self.margin * ' '
        for idx in range(1, self.width + 1):
            board += f'  {idx} '
        board += '\n'

        for i in range(self.height):
            board += self.margin * ' '
            board += '|---' * self.width + f'|\n{chr(char_idx)}'
            board += (self.margin - 1) * ' '
            for k in range(self.width):
                board += f'| {self.board_data[i][k]} '
            board += '|\n'
            char_idx += 1

        board += self.margin * ' '
        board += '|---' * self.width + '|\n'

        print(board)


if __name__ == '__main__':
    b = Board(3, 3)
    b.draw()
    print(b.board_data)
