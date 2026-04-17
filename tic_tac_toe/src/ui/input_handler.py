from src.utils.constants import PLAYER_HUMAN, PLAYER_CPU


class InputHandler:
    """
    Handles all user input with validation for Tic Tac Toe
    """

    # @staticmethod
    # def get_player_type(player_number):
    #     """Prompt for player type (human or CPU) and return the selected type."""
    #     while True:
    #         player_type = input(f"Select type for Player {player_number} (human/cpu): ").strip().lower()
    #         if player_type in [PLAYER_HUMAN, PLAYER_CPU]:
    #             return player_type
    #         else:
    #             print("Invalid input! Please enter 'human' or 'cpu'.")
    #
    # @staticmethod
    # def get_move_input(player_name):
    #     """Prompt the player for their move input and return the row and column as integers."""
    #     while True:
    #         move_input = input(f"{player_name}, enter your move (row and column): ").strip()
    #         try:
    #             row, col = map(int, move_input.split())
    #             return row, col
    #         except ValueError:
    #             print("Invalid input! Please enter two numbers separated by a space (e.g., '1 2').")

    @staticmethod
    def get_menu_choice(options):
        # """Prompt the user to select an option from the menu and return the selected option."""
        """
        Get validated menu selection
        Returns: choice index
        """
        while True:
            print("Menu Options:")
            for idx, option in enumerate(options, start=1):
                print(f"{idx}. {option}")
            choice = input("Select an option by entering the corresponding number: ").strip()
            if choice.isdigit():
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(options):
                    return choice_idx
            print("Invalid selection! Please enter a valid option number.")

    @staticmethod
    def get_player_config():
        """
        Get game configuration from user
        Returns: dictionary with game settings
        """
        # Ask for:
        # - Player 1 type (human/AI)
        # - Player 2 type (human/AI)
        # - AI difficulty if applicable
        # - Board size (optional)

        config = {'players': [{}, {}], 'board_size': 3}
        print("Configure Players:")
        for i in range(2):
            while True:
                player_type = input(f"Select type for Player {i + 1} (human/cpu): ").strip().lower()
                if player_type in [PLAYER_HUMAN, PLAYER_CPU]:
                    config['players'][i]['type'] = player_type
                    # print(f"Configuring Player {i} as {'Human' if player_type == PLAYER_HUMAN else 'CPU'}.")

                    # If CPU, ask for difficulty level
                    if player_type == PLAYER_CPU:
                        while True:
                            difficulty = input(f"Select difficulty for Player {i + 1} (easy/medium/hard): ").strip().lower()
                            if difficulty in ['easy', 'medium', 'hard']:
                                config['players'][i]['difficulty'] = difficulty
                                break
                            else:
                                print("Invalid input! Please enter 'easy', 'medium', or 'hard'.")

                    # Ask for player name
                        # Set default name as "AI" for CPU player
                        default_name = "AI"
                        name_input = input(f"Enter name for Player {i + 1} (default {default_name}): ").strip()
                        config['players'][i]['name'] = name_input if name_input else default_name
                    else:
                        # For human players, ask for name (no default)
                        name = input(f"Enter name for Player {i + 1}: ").strip()
                        config['players'][i]['name'] = name if name else f'Player {i + 1}'

                    # Ask for player symbol
                    symbol = input(f"Enter symbol for {config['players'][i]['name']} (default {'X' if i == 0 else 'O'}): ").strip()
                    if not symbol:
                        symbol = 'X' if i == 0 else 'O'
                    config['players'][i]['symbol'] = symbol

                    # Additional configurations can be added here
                    # e.g., board size, winning length, etc.
                    break
                else:
                    print("Invalid input! Please enter 'human' or 'cpu'.")
        return config

    @staticmethod
    def get_move_input(player_name):
        """
        Prompt the player for their move input and return the row and column as integers. Get and validate position input.
        Returns: (row, col)
        """
        while True:
            move_input = input(f"{player_name}, enter your move (row and column): ").strip()
            try:
                row, col = map(int, move_input.split())
                return row, col
            except ValueError:
                print("Invalid input! Please enter two numbers separated by a space (e.g., '1 2').")

    @staticmethod
    def get_play_again_choice():
        """
        Prompt the user to decide whether to play again. Ask if player wants to play again.
        Returns: True if yes, False if no
        """
        while True:
            choice = input("Do you want to play again? (y/n): ").strip().lower()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                print("Invalid input! Please enter 'y' for yes or 'n' for no.")
