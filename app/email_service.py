from flask_mail import Mail, Message
from flask import current_app

def send_email(recipient, subject, body, attachment=None):
    mail = Mail(current_app)
    msg = Message(subject, recipients=[recipient])
    msg.body = body
    if attachment:
        # Assuming attachment is a BytesIO object
        msg.attach('presentation.pptx', 'application/vnd.openxmlformats-officedocument.presentationml.presentation', attachment.read())
