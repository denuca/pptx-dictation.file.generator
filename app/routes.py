# app/routes.py
import os
import io
from flask import Blueprint, request, session, send_file, render_template, redirect, url_for, session
from app.ppt_generator import create_ppt_from_text, create_ppt_dictation_from_text  # Adjust import if necessary
from app.email_service import send_email  # Optional
from io import BytesIO

index = Blueprint('index', __name__)

# Session and streaming size limits
SESSION_SIZE_LIMIT = int(os.getenv('SESSION_SIZE_LIMIT', 3500))  # Fallback to 3500 bytes if not set
STREAMING_SIZE_LIMIT = int(os.getenv('STREAMING_SIZE_LIMIT', 1024 * 1024))  # Default 1 MB streaming limit

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


@index.route('/', methods=['GET', 'POST'])
def index_route():
    """
    Handles both GET and POST requests for the homepage. Validates inputs, generates PowerPoint, and sends email or provides download option.
    """
    if request.method == 'POST':
        # Retrieve inputs from the form
        text_input = request.form.get('text_input', '').strip()
        file_input = request.files.get('file_input')

        # Validate the inputs
        is_valid, result = validate_input(text_input, file_input)
        if not is_valid:
            return render_template('index.html', message=result, result="fail")

        text_input = result

        # Process the input to extract title and content
        lines = text_input.splitlines()
        title = lines[0].strip() if lines else ""
        content = "\n".join(line.strip() for line in lines[1:])

        # Check session size limit before storing
        session_data = f"{title}\n{content}"
        if len(session_data.encode('utf-8')) > SESSION_SIZE_LIMIT:
            return render_template('index.html', message="Your input is too large. Please reduce the text length.", result="fail")

        # Store title and content in the session
        session['title'] = title
        session['content'] = content

        # Generate PowerPoint
        #ppt = create_ppt_from_text(title, content)
        print(f"create_ppt_dictation_from_text start")
        ppt = create_ppt_dictation_from_text(title, content)
        print(f"create_ppt_dictation_from_text end")
        ppt_io = io.BytesIO()
        ppt.save(ppt_io)
        ppt_io.seek(0)

        # Check if the PowerPoint exceeds the streaming size limit
        ppt_size = ppt_io.tell()
        if ppt_size > STREAMING_SIZE_LIMIT:
            return render_template('index.html', message="The generated PowerPoint is too large to download directly.", result="fail")

        # Handle email sending or file download
        email_input = request.form.get('email_input', None)
        print("Email input received:", email_input)

        if email_input:
            ppt_io.seek(0)  # Reset IO stream to the beginning

            send_email(email_input, "Your PowerPoint Presentation", "Here is your generated presentation.", ppt_io)
            return render_template('index.html', message="PowerPoint has been sent to your email!", result="success")

        # Provide download URL if no email is provided
        return render_template('index.html', message="Your PowerPoint is ready!", download_url=True, result="success")

    return render_template('index.html')


@index.route('/download')
def download_file():
    """
    Allows the user to download the generated PowerPoint file from session data.
    """
    title = session.get('title', None)
    content = session.get('content', None)

    if not title or not content:
        return "No PowerPoint available for download. Please generate one first.", 400

    # Check if the session data exceeds the streaming limit
    session_data = f"{title}\n{content}"
    if len(session_data.encode('utf-8')) > STREAMING_SIZE_LIMIT:
        return "The generated PowerPoint is too large to download directly. Please reduce the content size or check back later for a link.", 200

    # Generate PowerPoint from session data
    #ppt = create_ppt_from_text(title, content)
    ppt = create_ppt_dictation_from_text(title, content)
    ppt_io = io.BytesIO()
    ppt.save(ppt_io)
    ppt_io.seek(0)

    return send_file(ppt_io, download_name="dictation-output.pptx", as_attachment=True)
