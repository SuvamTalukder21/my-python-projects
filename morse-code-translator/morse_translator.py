# Core module to handle the text-to-morse translation logic
import data.morse_code_map as morse_code_map
import utils


class MorseTranslator:
    def __init__(self):
        """Initialize the MorseTranslator class with a Morse code dictionary."""

        self.morse_code_dict = morse_code_map.get_morse_code_dict()
        self.reverse_morse_code_dict = morse_code_map.get_reverse_morse_code_dict()

    def translate_to_morse(self, text: str) -> str:
        """
        Translate the input text into Morse code.

        Args:
            text (str): The text to be translated into Morse code.

        Returns:
            str: The translated Morse code.
        """

        # Validate input text using pre-defined and user-defined Morse codes
        valid_characters = {**self.morse_code_dict["pre_defined_morse_code"], **self.morse_code_dict.get("user_defined_morse_code", {})}

        if utils.is_valid_text(text, valid_characters):
            text = text.upper()  # Convert to uppercase for consistency
            morse_code = [valid_characters[char] for char in text if char in valid_characters]

            return f"Morse Code: {' '.join(morse_code)}"
            # return f"Morse Code: {' '.join(self.morse_code_dict["pre_defined_morse_code"][char] for char in text.upper() if char in self.morse_code_dict["pre_defined_morse_code"])}"  # Another one liner logic for this function

        else:
            return "Invalid input. Please use letters, numbers, spaces, and supported punctuation."

    def translate_from_morse(self, morse_code: str) -> str:
        """
        Translate the input morse to text
        Translate input Morse code to text.

        Args:
            morse_code (str): The Morse code to translate.

        Returns:
            str: Translated text.
        """

        # Merge both pre-defined and user-defined Morse codes for reverse lookup
        combined_reverse_morse_code = {**self.reverse_morse_code_dict["pre_defined_morse_code"], **self.reverse_morse_code_dict.get("user_defined_morse_code", {})}

        # Validate the Morse code input using both dictionaries
        if utils.is_valid_morse_code(morse_code, combined_reverse_morse_code):
            words = morse_code.split(" / ")  # Words are separated by " / "
            decoded_message = []

            for word in words:
                decoded_word = ''.join([combined_reverse_morse_code[char] for char in word.split() if char in combined_reverse_morse_code])
                decoded_message.append(decoded_word)

            return f"Decoded Text: {' '.join(decoded_message)}"
            # return f"Decoded Text: {''.join(self.reverse_morse_code_dict[code] for code in morse_code.split() if code in self.reverse_morse_code_dict)}"  # Another one liner logic for this function

        else:
            return "Invalid Morse code. Please enter valid Morse code symbols like dot(.), hyphen(-), slash(/), and spaces."

    def add_user_defined_morse_code(self, num_entries: int) -> str:
        """
        Allow the user to add multiple custom character-to-Morse code mappings.

        Args:
            num_entries (int): The number of custom entries the user wants to add.

        Returns:
            str: A summary of all custom Morse codes added, or any error messages.
        """

        user_dict = {}
        result_messages = []

        for i in range(num_entries):
            user_char = input("Enter the character you want to define Morse code for: ").strip().upper()
            user_morse = input(f"Enter the Morse code for '{user_char}': ").strip()

            if utils.is_valid_text(user_char, self.morse_code_dict["pre_defined_morse_code"]) and utils.is_valid_morse_code(user_morse, self.reverse_morse_code_dict["pre_defined_morse_code"]):
                result_messages.append(f"Your entered character '{user_char}' or Morse code '{user_morse}' is predefined. Please enter a different value.")

            else:
                if len(user_char) == 1:
                    user_dict[user_char] = user_morse

                    custom_code = morse_code_map.add_custom_morse_code(user_dict)
                    char = list(custom_code.keys())[0]
                    morse_code = custom_code[char]

                    result_messages.append(f"Custom Morse code added: {char} -> {morse_code}")

                else:
                    result_messages.append("Please enter a single character for custom Morse code.")

        return "\n".join(result_messages) if result_messages else "No custom Morse codes were added."



# # Example Usage (Uncomment for testing)
# if __name__ == "__main__":
#     translator = MorseTranslator()
#     text = "HELLO WORLD"
#     morse = translator.translate_to_morse(text)
#     print(morse)
#
#     morse = ".... . .-.. .-.. --- / .-- --- .-. .-.. -.. -.-.--"
#     text = translator.translate_from_morse(morse)
#     print(text)
#
#     # custom_mappings = {'#': '......', '%': '.-.-.-.'}
#     print(translator.add_user_defined_morse_code(2))
