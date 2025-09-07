from celery import shared_task
from common.utils.send_mail import generate_email_message, send_email

@shared_task
def send_notification_email(email, code=None):
    html_message = generate_email_message(code)
    send_email(email, html_message)