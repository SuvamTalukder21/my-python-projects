from src.players.base import BasePlayer as Player
from src.game.board import Board
from typing import Tuple


class HumanPlayer(Player):
    """
    Human player that gets moves from user input
    """

    def __init__(self, symbol: str, name: str = "Human"):
        super().__init__(symbol, name)

    def make_move(self, board: Board) -> Tuple[int, int]:
        """
        Prompt user for row and column input
        Handle input validation and conversion
        """
        # while True:
        #     try:
        #         move = input(f"{self.name} ({self.symbol}), enter your move (row and column): ")
        #         row, col = map(int, move.split())
        #         if board.is_valid_move(row, col):
        #             return row, col
        #         else:
        #             print("Invalid move. Try again.")
        #     except (ValueError, IndexError):
        #         print("Invalid input format. Please enter row and column numbers separated by a space.")

        while True:
            print("Available positions:")
            board.display()

            move_inp = input(f"{self.name} ({self.symbol}), enter your move (row and column): ")

            try:
                row, col = map(int, move_inp.split())

                # Convert to 0-index
                row -= 1
                col -= 1

                if board.is_valid_move(row, col):
                    return (row, col)
                else:
                    print("Invalid move. Try again.")

            except (ValueError, IndexError):
                print("Invalid input format. Please enter row and column numbers.")

    @staticmethod
    def format_position_input(self, position: str) -> Tuple[int, int]:
        """
        Convert user input position (1-9) to (row, col)
        """
        # note: kept for compatibility but not used by tests
        pos = int(position)
        row = pos // 3
        col = pos % 3
        return (row, col)


if __name__ == "__main__":
    board = Board()
    # player = HumanPlayer('X', 'Alice')
    # move = player.make_move(board)
    # print(f"Player {player.name} chose move: {move}")
