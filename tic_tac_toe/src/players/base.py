from abc import ABC, abstractmethod


class BasePlayer(ABC):
    """Abstract base class for a game player."""
    def __init__(self, symbol, name):
        self.symbol = symbol
        self.name = name
        self.score = 0

    @abstractmethod
    def make_move(self, board):
        # """Decide on the next move based on the current game state."""
        """
        Get move from player
        Returns: (row, col) tuple
        """
        # if self.symbol not in ['X', 'O']:
        #     raise ValueError("Invalid player symbol")
        #
        # for row in range(len(board)):
        #     for col in range(len(board[row])):
        #         if board[row][col] == ' ':
        #             return (row, col)
        #
        # raise ValueError("No valid moves available")

        pass

    def increment_score(self):
        """Increment the player's score by one."""
        self.score += 1

    def reset_score(self):
        """Reset the player's internal state for a new game."""
        self.score = 0


if __name__ == "__main__":
    # Example usage
    player = BasePlayer('X', 'Player 1')
    print(f"Player: {player.name}, Symbol: {player.symbol}, Score: {player.score}")
    player.increment_score()
    print(f"After increment, Score: {player.score}")
    player.reset_score()
    print(f"After reset, Score: {player.score}")
