from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags

def generate_email_message(code:int | None = None) -> str:
    """
    Generates an email message.

    """
    if code:
        html_message = f"""
        <div style="font-family: sans-serif; max-width: 500px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
            <h2 style="color: #333;">OTP code to change the password.</h2>
            <p>Your password recovery code:</p>
            <div style="font-size: 24px; font-weight: bold; color: #0057b7; margin: 20px 0;">{code}</div>
            <p>If you did not submit this request, please ignore this message.</p>
        </div>
        """
    else:
        html_message = f"""
        <div style="font-family: sans-serif; max-width: 500px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
            <h2 style="color: #333;">This account is not registered</h2>
            <p>You or someone else is trying to change your password when you don't already have an account.</p>
            <p>If you did not submit this request, please ignore this message.</p>
        </div>
        """
    return html_message

def send_email(email:str, html_message:str) -> None:
    """
    Sends an email notification.

    """
    txt_plain_message = strip_tags(html_message)
    send_mail(
        subject='Request to Reset the passowrd',
        message=txt_plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        html_message=html_message,
    )
