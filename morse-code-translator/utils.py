# Utility functions (e.g., validation, file handling)
import json


def load_from_json_file(file_name: str) -> dict:
    """
    Load and return the content from the given file.

    Args:
        file_name (str): The name of the file to load the data from.

    Returns:
        str: The content of the file.
    """

    try:
        with open(f"data/{file_name}", "r") as file:
            data = json.load(file)
            return data

    except OSError as e:
        raise OSError(f"Error reading from file {file_name}: {e}")


def save_to_json_file(file_name: str, data: dict) -> None:
    """
    Save the given data to a file.

    Args:
        file_name (str): The name of the file to save the data to.
        data (str): The content to be written to the file.
    """

    try:
        file_path = f"data/{file_name}"

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

        print(f"Data successfully saved to {file_name}")

    except OSError as e:
        raise OSError(f"Error saving to file {file_name}: {e}")


def is_valid_text(text: str, morse_dict: dict) -> bool:
    """
    Check if the input text contains only valid characters for Morse code translation.

    Args:
        text (str): The text to validate.
        morse_dict (dict): The Morse code dictionary to validate against.

    Returns:
        bool: True if valid, False otherwise.
    """

    valid_chars = set(morse_dict.keys())
    text = text.upper()

    for char in text:
        if char not in valid_chars:
            return False

    return True
    # return all(char in morse_dict for char in text.upper())


def is_valid_morse_code(morse_code: str, reversed_dict: dict) -> bool:
    """
    Check if the input Morse code is valid.

    Args:
        morse_code (str): The Morse code to validate.
        reversed_dict (dict): The reverse Morse code dictionary to validate against.

    Returns:
        bool: True if valid, False otherwise.
    """

    valid_code = set(reversed_dict.keys())
    morse_code = morse_code.split()

    for code in morse_code:
        if code not in valid_code:
            return False

    return True
    # return all(code in reversed_dict for code in morse_code.split())


def clean_text(text: str) -> str:
    """
    Clean the input text by stripping extra spaces and unwanted characters.

    This can be customized based on the type of input you'd like to clean.

    Args:
        text (str): The text to be cleaned.

    Returns:
        str: The cleaned text.
    """
    # Remove leading/trailing spaces and replace multiple spaces with single spaces
    cleaned_text = ' '.join(text.split())

    # Additional cleaning logic can be added here, e.g., removing non-printable characters.
    return cleaned_text


# Example Usage (Uncomment for testing)
# if __name__ == "__main__":
#     # Test saving to file
#     morse_code = ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
#     save_to_file("morse_code.txt", morse_code)

#     # Test loading from file
#     loaded_text = load_from_file("morse_code.txt")
#     print(f"Loaded Text: {loaded_text}")

#     # Test text cleaning
#     raw_text = "    Hello    World!    "
#     cleaned = clean_text(raw_text)
#     print(f"Cleaned Text: '{cleaned}'")
