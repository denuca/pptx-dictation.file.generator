import logging

logger = logging.getLogger(__name__)

def validate_input(text_input, file_input):
    """
    Validates that either text input or file input is provided.
    Args:
        text_input (str): The text input from the form.
        file_input (FileStorage): The uploaded file input from the form.

    Returns:
        tuple: (bool, str) where bool indicates if the input is valid and str contains either text content or an error message.
    """
    if not text_input and not file_input:
        return False, "Please enter text or upload a file."

    if file_input:
        try:
            text_input = file_input.read().decode('utf-8')
        except Exception as e:
            return False, f"Error reading uploaded file: {e}"

    return True, text_input

def load_text_file(file_path):
    """Reads the text file and returns a list of lines."""
    with open(file_path, 'r') as file:
        return file.readlines()
