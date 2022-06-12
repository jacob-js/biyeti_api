from django.core.mail import send_mail

def send_simple_mail(subject: str, message: str, to_email: str, from_email: str = "BOOKIT"):
    """
    Send a simple email
    """
    return send_mail(subject, message, from_email, [to_email])