# Morse Code Translator

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Rooms for Improvment](#rooms-for-improvement)
- [Contributing](#contributing)
- [License](#license)

## Overview

The **Morse Code Translator** is a Python project that allows users to translate text into Morse code and vice versa. It also supports custom Morse code definitions, enabling users to extend the existing Morse code mappings for new characters or symbols.

## Features

- Translate English text to Morse code.
- Translate Morse code back to English.
- Custom Morse code definitions for user-defined characters.
- Easy-to-use command-line interface.
- Thorough test coverage using `pytest`.

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/morse-code-translator.git
   cd morse-code-translator
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

The project includes a simple interface for translating text to and from Morse code. You can also add custom Morse code mappings for new characters.

### Translating Text to Morse Code

To translate text to Morse code, you can use the `translate_to_morse` method:

```python
from morse_translator import MorseTranslator

translator = MorseTranslator()
result = translator.translate_to_morse("HELLO 123")
print(result)  # Morse Code: .... . .-.. .-.. --- / .---- ..--- ...--
```

### Translating Morse Code to Text

To translate Morse code back to text:

```python
result = translator.translate_to_text(".... . .-.. .-.. --- / .---- ..--- ...--")
print(result)  # Translated Text: HELLO 123
```

### Adding Custom Morse Code

You can define custom Morse codes for any characters or symbols that are not part of the standard Morse code dictionary:

```python
result = translator.add_user_defined_morse_code(1)  # Define custom Morse code for one character
print(result)  # Custom Morse code added: ! -> --.-- 
```

## Running Tests

The project uses `pytest` for running tests. The test suite covers translation logic, error handling, and custom Morse code additions.

1. Install `pytest`:

   ```bash
   pip install pytest
   ```

2. Run the tests:

   ```bash
   pytest
   ```

Make sure all tests pass to ensure that the Morse code translator is working correctly.

## Rooms for Improvement
There are a few areas in the project that could be enhanced or extended to improve functionality and user experience:

1. **Recurring Inputs:** Currently, it doesn't have any `while` loop where it would ask the user to enter option again, there you can add a `while` loop in `main.py` file.

2. **Improved Input Validation:** Currently, the validation for custom Morse code input is basic. Adding more detailed input validation (e.g., checking for allowed Morse code symbols) would help ensure the integrity of the data.

3. **Handling More Edge Cases:** Currently, the system handles a range of basic inputs, but extending support to handle more complex punctuation or symbols in a more robust way could further enhance its usability.

4. **Graphical User Interface (GUI):** Implementing a graphical interface using libraries like `Tkinter` or `PyQt` would make the application more user-friendly, especially for non-technical users.

5. **Support for Batch Translation:** Add functionality to support the translation of large blocks of text or files (e.g., translating the contents of a `.txt` file to Morse code).

6. **Multilingual Support:** Although Morse code is primarily used for English, expanding the project to support other languages (e.g., by using international Morse code standards) could broaden its appeal.



## Contributing

Contributions to the Morse Code Translator project are always welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes with clear messages.
4. Create a pull request to the main repository.

Ensure that all tests pass before submitting a pull request.

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute this project as per the terms of the license.
