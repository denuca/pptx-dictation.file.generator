import logging
from core.file_generator.validation import validate_input  # Import from the core library
from core.file_generator.pptx import create_ppt, add_title_slide  # Import from the core library

def create_ppt_from_text(title, content):
    try:
        is_valid, error_message = validate_input(title, content)
        if not is_valid:
            raise ValueError(error_message)

        ppt = create_ppt()
        add_title_slide(ppt, title, content)
        return ppt
    except Exception as e:
        logging.error(f"Error creating PowerPoint: {e}")
        raise  # Re-raise the exception after logging
