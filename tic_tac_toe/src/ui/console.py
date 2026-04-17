from src.utils.constants import PLAYER_X, PLAYER_O, EMPTY


class ConsoleUI:
    """
    Handles console-based user interface for Tic Tac Toe
    """

    @staticmethod
    def clear_screen():
        """Clear console screen (platform independent)."""
        print("\n" * 100)

    @staticmethod
    def show_welcome_message():
        """Display welcome message and instructions to the players."""
        print("Welcome to Tic Tac Toe!")
        print("Players take turns placing their marks (X and O) on the board.")
        print("The first player to get three in a row wins!")
        print("To make a move, enter the row and column numbers (e.g., '1 2').")
        print("Let's start the game!")

    @staticmethod
    def show_board(board):
        """Display the current state of the board in the console"""
        # print(board.display())
        board.display()

    @staticmethod
    def show_turn(player_name, player_symbol):
        """Display whose turn it is. Prompt the current player for their move."""
        # print(f"It's {player_name}'s turn ({player_symbol}).")
        # return input(f"Player {player_name}, enter your move (row and column): ")
        print(f"It's {player_name}'s turn ({player_symbol}).")
        # return input("Enter your move (row and column): ")

    @staticmethod
    def show_winner(winner_name, winner_symbol):
        """Display winner announcement. Announce the winner of the game."""
        # print(f"Player {winner_name} wins! Congratulations!")
        print(f"Player {winner_name} ({winner_symbol}) wins! Congratulations!")

    @staticmethod
    def show_draw():
        """Display draw announcement. Announce a draw."""
        # print("The game is a draw!")
        print("It's a draw! Well played both!")

    @staticmethod
    # def show_score(self, player1_name, player1_score, player2_name, player2_score):
    #     """Display the current scores of both players."""
    #     print(f"Score - {player1_name}: {player1_score}, {player2_name}: {player2_score}")
    def show_score(players):
        """Display the current scores of both players."""
        print(f"Score - {players[0].name}: {players[0].score}, {players[1].name}: {players[1].score}")

    @staticmethod
    def show_invalid_move(message):
        """Display error message for invalid move. Notify the player of an invalid move."""
        # print("Invalid move! Please try again.")
        print(f"Invalid move! {message} Please try again.")

    # @staticmethod
    # def display_goodbye_message():
    #     """Display a goodbye message to the players"""
    #     print("Thanks for playing Tic Tac Toe! Goodbye!")

    # @staticmethod
    # def display_current_player(player):
    #     """Display the current player's turn"""
    #     print(f"It's Player {player}'s turn.")

    # @staticmethod
    # def display_board_full():
    #     """Notify that the board is full"""
    #     print("The board is full. No more moves can be made.")

    # @staticmethod
    # def display_reset_message():
    #     """Notify that the board has been reset"""
    #     print("The board has been reset for a new game.")

    #         moves = []
#         for r in range(self.size):
#             for c in range(self.size):
#                 if self.grid[r][c] == EMPTY:
#                     moves.append((r, c))
#         return moves


if __name__ == "__main__":
    # Example usage
    ui = ConsoleUI()
    ui.show_welcome_message()
    ui.show_turn("Alice", PLAYER_X)
    ui.show_invalid_move("Position already taken.")
    ui.show_winner("Bob", PLAYER_O)
    ui.show_draw()
    ui.show_score([type('Player', (object,), {'name': 'Alice', 'score': 2})(),
                   type('Player', (object,), {'name': 'Bob', 'score': 3})()])

    board = type('Board', (object,), {'display': lambda self: " X | O | \n-----------\n   | X | O\n-----------\n O |   | X"})()
    ui.show_board(board)
    ui.clear_screen()
    ui.show_board(board)
