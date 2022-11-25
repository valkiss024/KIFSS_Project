import random
import string
import os

from flask_mail import Message
from dashboard import mail


def generate_password(length):
    """Method to generate a random password for a given length"""
    password = "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return password


def send_notification(recipients, subject, message):
    """Method to send email notifications"""
    msg = Message(
        subject=subject,
        sender=os.environ.get('MAIL_USERNAME'),
        recipients=recipients
    )
    msg.body = message
    mail.send(msg)
