# tic_tac_toe/
# │
# ├── src/                 # Source code directory
# │   ├── __init__.py
# │   │
# │   ├── game/           # Game logic components
# │   │   ├── __init__.py
# │   │   ├── board.py        # Board class (state, display, moves)
# │   │   ├── engine.py       # Game rules, win checking
# │   │   └── validator.py    # Move validation
# │   │
# │   ├── players/        # Player implementations
# │   │   ├── __init__.py
# │   │   ├── base.py         # Abstract player class
# │   │   ├── human.py        # Human player with input
# │   │   └── cpu.py           # Computer opponent logic
# │   │
# │   ├── ui/             # User interface layer
# │   │   ├── __init__.py
# │   │   ├── console.py      # Text display functions
# │   │   └── input_handler.py # User input processing
# │   │
# │   └── utils/          # Utility functions
# │       ├── __init__.py
# │       ├── constants.py    # Game constants (X, O, EMPTY)
# │       └── helpers.py      # Common helper functions
# │
# ├── tests/              # Test directory
# │   ├── __init__.py
# │   ├── test_board.py
# │   ├── test_engine.py
# │   └── test_players.py
# │
# ├── requirements.txt    # Dependencies (optional for this project)
# ├── README.md           # Project documentation
# └── main.py             # Launch script (optional)
from src.game.board import Board
from src.game.engine import GameEngine
from src.players.cpu import CPUPlayer
from src.players.human import HumanPlayer
from src.ui.console import ConsoleUI
from src.ui.input_handler import InputHandler
from src.utils.constants import PLAYER_HUMAN, PLAYER_X, PLAYER_O, GAME_WIN, GAME_DRAW


class TicTacToe:
    """
    Main game controller that orchestrates the Tic Tac Toe game
    """

    def __init__(self):
        # print("Tic Tac Toe game initialized.")
        self.board = None
        self.engine = None
        self.players = []
        self.current_player_index = 0
        self.ui = ConsoleUI()
        self.input_handler = InputHandler()

    def setup(self):
        """Initialize game with user configuration"""
        # 1. Get configuration from user
        config = self.input_handler.get_player_config()
        # 2. Initialize board, engine, and players based on config
        # 2. Create board
        config_size = config.get('board_size', 3)
        self.board = Board(size=config_size)
        # 3. Create engine
        self.engine = GameEngine(self.board)
        # 4. Create players
        for i in range(2):
            player_type = config['players'][i]['type']
            if player_type == PLAYER_HUMAN:
                # player = HumanPlayer(name=f"Player {i + 1}", symbol=PLAYER_X if i == 0 else PLAYER_O)
                player = HumanPlayer(symbol=config["players"][i]["symbol"], name=config["players"][i]["name"])
            else:
                # player = CPUPlayer(name=f"CPU {i + 1}", symbol=PLAYER_X if i == 0 else PLAYER_O, difficulty=config['players'][i].get('difficulty', 'easy'))
                player = CPUPlayer(symbol=config["players"][i]["symbol"], name=config["players"][i]["name"], difficulty=config['players'][i].get('difficulty', 'easy'))
                player.engine = self.engine  # Provide engine reference for AI decision making
            self.players.append(player)

    # def start_game(self):
    #     print("Starting the Tic Tac Toe game...")
    #     # Here you would typically initialize the game components and start the game loop

    # def run(self):
    #     """Main game loop"""
    #     self.ui.show_welcome_message()
    #     self.setup()
    #
    #     game_over = False
    #     while not game_over:
    #         current_player = self.players[self.current_player_index]
    #         self.ui.show_turn(current_player.name, current_player.symbol)
    #         self.board.display()
    #
    #         # Get move from current player
    #         row, col = current_player.get_move(self.board)
    #
    #         # Validate and make move
    #         if self.engine.validate_move(row, col):
    #             self.board.make_move(row, col, current_player.symbol)
    #
    #             # Check for win/draw
    #             if self.engine.check_winner(current_player.symbol):
    #                 self.board.display()
    #                 self.ui.show_winner(current_player.name, current_player.symbol)
    #                 current_player.score += 1
    #                 game_over = True
    #             elif self.engine.check_draw():
    #                 self.board.display()
    #                 self.ui.show_draw()
    #                 game_over = True
    #             else:
    #                 # Switch to other player
    #                 self.current_player_index = 1 - self.current_player_index
    #         else:
    #             self.ui.show_invalid_move("That position is already taken or out of bounds.")
    #
    #     # Show final scores
    #     self.ui.show_score(self.players)

    def run(self):
        """Main game loop"""
        self.ui.show_welcome_message()
        self.setup()

        while True:
            self.play_round()
            self.ui.show_score(self.players)

            if not self.ask_play_again():
                print("Thanks for playing!")
                break

    def play_round(self):
        """Play a single round of Tic Tac Toe"""
        self.board.reset()
        self.current_player_index = 0

        while True:
            current_player = self.players[self.current_player_index]

            # Display current board and scores
            # self.ui.clear_screen()
            self.ui.show_board(self.board)
            self.ui.show_score(self.players)
            self.ui.show_turn(current_player.name, current_player.symbol)
            # self.board.display()

            move = current_player.make_move(self.board)
            # if move is None:
            #     print("No moves left! It's a draw.")
            #     return

            row, col = move

            # Get move from current player
            # row, col = current_player.make_move(self.board)
            # row, col = self.input_handler.get_move_input(current_player)

            # Validate and make move
            if self.board.is_valid_move(row, col):
                self.board.make_move(row, col, current_player.symbol)

                # # Check for win/draw
                # if self.engine.check_winner(current_player.symbol):
                #     self.board.display()
                #     self.ui.show_winner(current_player.name, current_player.symbol)
                #     current_player.score += 1
                #     break
                # elif self.engine.check_draw():
                #     self.board.display()
                #     self.ui.show_draw()
                #     break
                # else:
                #     # Switch to other player
                #     self.current_player_index = 1 - self.current_player_index

                # Check game status
                status = self.engine.get_game_status(current_player.symbol)

                if status == GAME_WIN:
                    # self.ui.show_board(self.board)
                    # self.ui.show_winner(current_player.name, current_player.symbol)
                    # current_player.score += 1
                    self.handle_win(current_player)
                    break

                elif status == GAME_DRAW:
                    self.handle_draw()
                    break

                # Switch player
                self.current_player_index = 1 - self.current_player_index
            else:
                self.ui.show_invalid_move("That position is already taken or out of bounds.")

    def handle_win(self, winner):
        """Process the win scenario"""
        winner.increment_score()
        self.ui.show_winner(winner.name, winner.symbol)

    def handle_draw(self):
        """Process the win scenario"""
        self.ui.show_board(self.board)
        self.ui.show_draw()

    def ask_play_again(self):
        """Ask players if they want to play again."""
        return self.input_handler.get_play_again_choice()


if __name__ == "__main__":
    """Start the game"""
    game = TicTacToe()
    game.run()
