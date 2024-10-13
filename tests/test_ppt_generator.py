import io
import pytest
from app import create_app  # Ensure this points to the app package
from app.routes import validate_input  # Update this as per your route definitions
from app.ppt_generator import create_ppt_from_text
from unittest.mock import patch, Mock

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SESSION_SIZE_LIMIT'] = 4096  # Set a limit for the tests
    with app.test_client() as client:
        yield client

def test_create_ppt_from_text():
    # This test now checks the core file generator's functionality
    title = "Title"
    content = "Content"
    ppt = create_ppt_from_text(title, content)
    assert ppt.slides[0].shapes.title.text == "Title"
    assert ppt.slides[0].shapes.placeholders[1].text == "Content"

def test_generate_ppt_with_multiline_content(client):
    # Input text with multiple lines
    text_input = "Slide Title\nFirst line of content.\nSecond line of content."

    # Simulate a POST request to generate PowerPoint
    response = client.post('/', data={'text_input': text_input})

    # Ensure the response is successful
    assert response.status_code == 200
    assert b"Your PowerPoint is ready!" in response.data

def test_input_too_large(client):
    # Generate a large input string
    large_title = "Title" + "A" * 4000
    large_content = "Content" + "B" * 4000

    # Simulate a POST request with the large input
    response = client.post('/', data={
        'text_input': f"{large_title}\n{large_content}",
    })

    # Check if the response contains the expected message
    assert b"Your input is too large. Please reduce the text length." in response.data

def test_download_file(client):
    # Simulate storing title and content in the session
    with client.session_transaction() as sess:
        sess['title'] = "Test Title"
        sess['content'] = "Test content for the PowerPoint."

    # Trigger the download route
    response = client.get('/download')

    # Check that the response is a valid file download
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=output.pptx'
    assert response.content_type == 'application/vnd.openxmlformats-officedocument.presentationml.presentation'

def generate_mock_pptx():
    """Generate a minimal .pptx file and return as a BytesIO object."""
    ppt = create_ppt_from_text("Slide Title", "This is the content.")
    ppt_io = io.BytesIO()
    ppt.save(ppt_io)
    ppt_io.seek(0)  # Reset the file pointer to the start
    return ppt_io

def test_email_functionality(client):
    # Generate a mock .pptx file
    mock_attachment = generate_mock_pptx()

    # Mock the send_email function where it is used in routes
    with patch('app.routes.send_email') as mock_send_email:
        # Set up the mock to return None (or whatever is appropriate)
        mock_send_email.return_value = None

        # Post data to the application
        response = client.post('/', data={
            'text_input': "Slide Title\nThis is the content.",
            'email_input': 'test@example.com'
        })

        # Ensure the response is successful
        assert response.status_code == 200
        assert b"PowerPoint has been sent to your email!" in response.data

        # Check that send_email was called with the correct arguments
        mock_send_email.assert_called_once()
        args, kwargs = mock_send_email.call_args
        assert args[0] == 'test@example.com'
        assert args[1] == "Your PowerPoint Presentation"
        assert args[2] == "Here is your generated presentation."

        # Compare the contents of the mock attachment with the actual sent attachment
        sent_attachment = args[3]
        assert isinstance(sent_attachment, io.BytesIO)
        assert sent_attachment.getvalue() == mock_attachment.getvalue()  # Compare actual .pptx contents

def test_validate_input_text_only():
    is_valid, result = validate_input("Some text input", None)
    assert is_valid
    assert result == "Some text input"

def test_validate_input_file_only():
    file_content = io.BytesIO(b"File content")
    is_valid, result = validate_input(None, file_content)
    assert is_valid
    assert result == "File content"

def test_validate_input_both_empty():
    is_valid, result = validate_input("", None)
    assert not is_valid
    assert result == "Please enter text or upload a file."

def test_validate_input_invalid_file():
    invalid_file = io.BytesIO(b"\x80\x81\x82")  # Simulate a corrupted file
    is_valid, result = validate_input(None, invalid_file)
    assert not is_valid
    assert "Error reading uploaded file" in result
