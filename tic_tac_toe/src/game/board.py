from src.utils.constants import EMPTY, PLAYER_X, PLAYER_O, BOARD_SIZE


class Board:
    """
    Represents the Tic Tac Toe board and handles board operations
    """
    def __init__(self, size=BOARD_SIZE):
        self.size = size
        self.grid = self.create_empty_board()

    def create_empty_board(self):
        """Initialize an empty board"""
        return [[EMPTY for _ in range(self.size)] for _ in range(self.size)]

    def display(self):
        """Convert board state to string for display"""
        # Builds visual representation like:
        #  X | O |
        # -----------
        #    | X | O
        # -----------
        #  O |   | X

        # print(f"Current Board: {self.size}x{self.size}")
        for r in range(self.size):
            row_display = " | ".join(self.grid[r])
            print(f" {row_display} ")
            if r < self.size - 1:
                print("-" * (self.size * 4 - 1))
        # return

    def make_move(self, row, col, player):
        """Place a player's mark on the board at the specified position"""
        # """Place symbol at position if valid"""
        if self.grid[row][col] == EMPTY:
            self.grid[row][col] = player
            return True
        return False

    def is_valid_move(self, row, col):
        """Check if the specified position is valid and empty"""
        return 0 <= row < self.size and 0 <= col < self.size and self.grid[row][col] == EMPTY

    def is_full(self):
        """Check if board has no empty positions"""
        return all(cell != EMPTY for row in self.grid for cell in row)

    def reset(self):
        """Clear the board for a new game"""
        self.grid = [[EMPTY for _ in range(3)] for _ in range(3)]

    # def get_empty_positions(self):
    #     empty_positions = []
    #     for r in range(self.size):
    #         for c in range(self.size):
    #             if self.grid[r][c] == EMPTY:
    #                 empty_positions.append((r, c))
    #     return empty_positions

    def get_available_moves(self):
        """Return a list of available moves (empty positions)"""
        moves = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == EMPTY:
                    moves.append((r, c))
        return moves


if __name__ == "__main__":
    board = Board()
    board.display()
    board.make_move(0, 0, PLAYER_X)
    board.make_move(1, 1, PLAYER_O)
    board.display()
