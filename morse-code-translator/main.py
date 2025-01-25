# Entry point of the application
from morse_translator import MorseTranslator


def main():
    """Main function to run the Morse code translator application."""

    # Created an instance of the MorseTranslator class
    translator = MorseTranslator()

    print("Welcome to the Morse Code Translator!")
    print("Choose an option:")
    print("1: Translate text to Morse code")
    print("2: Translate Morse code to text")
    print("3: Add a custom Morse code")

    # Get user's choice
    choice = int(input("Enter 1, 2 or 3: ").strip())

    if choice == 1:
        # Translate text to Morse code
        text = input("Enter the text you want to translate to Morse code: ").strip()

        morse_code = translator.translate_to_morse(text)
        print(morse_code)

    elif choice == 2:
        # Translate Morse code to text
        morse_code = input("Enter the Morse code you want to translate to text: ").strip()

        decoded_text = translator.translate_from_morse(morse_code)
        print(decoded_text)

    elif choice == 3:
        num_inputs = int(input("Enter number of entries you want to add: "))

        custom_codes = translator.add_user_defined_morse_code(num_inputs)
        print(custom_codes)

    else:
        print("Invalid option. Please enter 1, 2 or 3.")


if __name__ == "__main__":
    main()

# # Main function to handle user input
# if __name__ == "__main__":
#     # Create a class instance
#     translator = MorseTranslator()
#
#     # Get input from the user
#     user_input = input("Enter the text to convert to Morse code: ")
#
#     # Convert the input to Morse code
#     morse_output = translator.translate_from_morse(morse_code=user_input)
#
#     # Output the result
#     print(f"Morse Code: {morse_output}")
