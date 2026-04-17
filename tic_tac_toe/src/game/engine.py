from src.utils.constants import GAME_ONGOING, GAME_WIN, GAME_DRAW


class GameEngine:
    """
    Handles game rules, win checking, and game state management
    """
    def __init__(self, board):
        self.board = board

    def check_winner(self, symbol):
        """
        Check the board for a winner or draw
        Returns: (bool) True if win detected
        """
        # Check rows, columns, and diagonals for a win
        size = self.board.size
        grid = self.board.grid

        # Check rows and columns
        for i in range(size):
            if all(grid[i][j] == symbol for j in range(size)):
                return True
            if all(grid[j][i] == symbol for j in range(size)):
                return True

        # Check diagonals
        if all(grid[i][i] == symbol for i in range(size)):
            return True

        # Check anti-diagonal
        if all(grid[i][size - 1 - i] == symbol for i in range(size)):
            return True

        return False

    def get_game_status(self, last_symbol_played):
        """
        Determine current game status
        Returns: GAME_ONGOING, GAME_WIN, or GAME_DRAW
        """
        if self.check_winner(last_symbol_played):
            return GAME_WIN
        elif self.board.is_full():
            return GAME_DRAW
        else:
            return GAME_ONGOING

    # def is_move_valid(self, row, col):
    #     """Validate if move can be made at position"""
    #     return self.board.is_position_valid(row, col)

    # def reset_game(self):
    #     """Reset the game state and board"""
    #     self.board.reset()
