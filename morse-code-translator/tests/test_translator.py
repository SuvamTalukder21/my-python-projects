# Unit tests for translation functionality
import pytest
from morse_translator import MorseTranslator


@pytest.fixture
def mock_morse_translator(monkeypatch):
    """Fixture to create and mock MorseTranslator with predefined Morse code dictionaries."""
    def mock_get_morse_code_dict():
        return {
            "pre_defined_morse_code": {
                'A': '.-', 'B': '-...', 'C': '-.-.', '1': '.----', '2': '..---', '.': '.-.-.-', ' ': '/'
            },
            "user_defined_morse_code": {}
        }

    def mock_get_reverse_morse_code_dict():
        return {
            "pre_defined_morse_code": {
                '.-': 'A', '-...': 'B', '-.-.': 'C', '.----': '1', '..---': '2', '.-.-.-': '.', '/': ' '
            },
            "user_defined_morse_code": {}
        }

    monkeypatch.setattr('data.morse_code_map.get_morse_code_dict', mock_get_morse_code_dict)
    monkeypatch.setattr('data.morse_code_map.get_reverse_morse_code_dict', mock_get_reverse_morse_code_dict)

    return MorseTranslator()


# Test for translating valid text to Morse code
def test_translate_to_morse_valid_input(mock_morse_translator):
    result = mock_morse_translator.translate_to_morse("ABC 12.")
    expected = "Morse Code: .- -... -.-. / .---- ..--- .-.-.-"
    assert result == expected


# Test for handling invalid characters when translating to Morse
def test_translate_to_morse_invalid_input(mock_morse_translator):
    result = mock_morse_translator.translate_to_morse("Z")  # 'Z' is not in the mocked dictionary
    expected = "Invalid input. Please use letters, numbers, spaces, and supported punctuation."
    assert result == expected


# Test for handling empty string when translating to Morse
def test_translate_to_morse_empty_input(mock_morse_translator):
    result = mock_morse_translator.translate_to_morse("")
    expected = "Morse Code: "
    assert result == expected


# Test for translating valid Morse code to text
def test_translate_from_morse_valid_input(mock_morse_translator):
    result = mock_morse_translator.translate_from_morse(".- -... -.-.")
    expected = "Decoded Text: ABC"
    assert result == expected


# Test for handling invalid Morse code input
def test_translate_from_morse_invalid_input(mock_morse_translator):
    result = mock_morse_translator.translate_from_morse(".- --.-")
    expected = "Invalid Morse code. Please enter valid Morse code symbols like dot(.), hyphen(-), slash(/), and spaces."
    assert result == expected


# Test for handling empty Morse code input
def test_translate_from_morse_empty_input(mock_morse_translator):
    result = mock_morse_translator.translate_from_morse("")
    expected = "Decoded Text: "
    assert result == expected


# Test for mixed valid/invalid Morse code translation
def test_translate_from_morse_mixed_input(mock_morse_translator):
    result = mock_morse_translator.translate_from_morse(".- -... --.-")
    expected = "Invalid Morse code. Please enter valid Morse code symbols like dot(.), hyphen(-), slash(/), and spaces."
    assert result == expected


# Mock add_custom_morse_code in morse_code_map to test custom Morse code addition
@pytest.fixture
def mock_custom_code(monkeypatch):
    """Mock the custom Morse code addition function."""

    def mock_add_custom_morse_code(mapping):
        # Simulating custom Morse code addition
        return mapping

    monkeypatch.setattr('data.morse_code_map.add_custom_morse_code', mock_add_custom_morse_code)


# Test for adding valid custom Morse code
def test_add_custom_morse_code_valid(mock_morse_translator, mock_custom_code, monkeypatch):
    # Mock user input for character '!' and Morse code '--.--'
    input_values = iter(['!', '--.--'])  # Created an iterator for sequential inputs

    # Mock `input` to return values from the iterator in sequence
    monkeypatch.setattr('builtins.input', lambda _: next(input_values))

    result = mock_morse_translator.add_user_defined_morse_code(1)

    expected_message = "Custom Morse code added: ! -> --.--"
    assert result == expected_message


# Test for handling duplicate custom Morse code
def test_add_custom_morse_code_duplicate(mock_morse_translator, mock_custom_code, monkeypatch):
    # Mock user input for predefined character 'A' and Morse code '.-'
    input_values = iter(['A', '.-'])  # Created an iterator for sequential inputs

    # Mock `input` to return values from the iterator in sequence
    monkeypatch.setattr('builtins.input', lambda _: next(input_values))

    result = mock_morse_translator.add_user_defined_morse_code(1)
    expected_message = "Your entered character 'A' or Morse code '.-' is predefined. Please enter a different value."
    assert expected_message in result


# Test for handling invalid custom character input
def test_add_custom_morse_code_invalid_character(mock_morse_translator, mock_custom_code, monkeypatch):
    # Mock user input for multiple characters
    input_values = iter(['AB', '----'])  # Created an iterator for sequential inputs

    # Mock `input` to return values from the iterator in sequence
    monkeypatch.setattr('builtins.input', lambda _: next(input_values))

    result = mock_morse_translator.add_user_defined_morse_code(1)
    assert "Please enter a single character for custom Morse code." in result
