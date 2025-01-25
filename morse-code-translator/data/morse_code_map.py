# Dictionary to map alphabets/numbers to Morse code
from utils import save_to_json_file, load_from_json_file

MORSE_CODE_JSON_FILE = "morse_code_data.json"

"""
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....',
    '7': '--...', '8': '---..', '9': '----.', ',': '--..--',
    '.': '.-.-.-', '?': '..--..', "'": '.----.', '!': '-.-.--',
    '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...',
    ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.',
    '-': '-....-', '_': '..--.-', '"': '.-..-.', '$': '...-..-',
    '@': '.--.-.', ' ': '/',  # Space between words is represented by "/"
}
"""


# Dictionary to map alphabets/numbers to Morse code
def get_morse_code_dict() -> dict:
    """
    Return the standard Morse code dictionary mapping letters and symbols to Morse code.

    Returns:
        dict: A dictionary mapping characters to their Morse code equivalent.
    """

    data = load_from_json_file(MORSE_CODE_JSON_FILE)
    return data


# Inverted dictionary for reverse translation (Morse code to text)
def get_reverse_morse_code_dict() -> dict:
    """
    Return a dictionary that maps Morse code to their corresponding characters.
    This is the reverse of the standard Morse code dictionary.

    Returns:
        dict: A dictionary mapping Morse code to characters.
    """

    morse_code_dict = get_morse_code_dict()
    # reverse_morse_code_dict = {code_definition: {code: char for char, code in morse_code.items()} for code_definition, morse_code in morse_code_dict.items()}  # One-liner dictionary comprehension for getting reversed version of Morse code dictionary

    reverse_morse_code_dict = {}

    for code_definition, morse_code in morse_code_dict.items():
        new_department = {}

        for char, code in morse_code.items():
            new_department[code] = char

        reverse_morse_code_dict[code_definition] = new_department

    return reverse_morse_code_dict


# Optional: Function to customize Morse code dictionary (if necessary)
def add_custom_morse_code(mapping: dict) -> dict:
    """
    Add custom Morse code mappings to the standard Morse code dictionary.

    Args:
        mapping (dict): A dictionary containing custom character-to-Morse mappings.

    Returns:
        dict: The updated Morse code dictionary with the custom mappings added.
    """

    morse_code_dict = load_from_json_file(MORSE_CODE_JSON_FILE)
    morse_code_dict["user_defined_morse_code"].update(mapping)
    save_to_json_file(MORSE_CODE_JSON_FILE, morse_code_dict)

    return mapping


# # Example Usage (Uncomment to test)
# if __name__ == "__main__":
#     # Standard dictionary
#     standard_dict = get_morse_code_dict()
#     print("Standard Morse Code Dict:", standard_dict)
#
#     # Reverse dictionary (Morse code to text)
#     reverse_dict = get_reverse_morse_code_dict()
#     print("Reverse Morse Code Dict:", reverse_dict)
#
#     # Add custom mappings (optional)
#     custom_mappings = {'#': '......', '%': '.-.-.-.'}
#     updated_dict = add_custom_morse_code(custom_mappings)
#     print("Updated Morse Code Dict with Custom Mappings:", updated_dict)
