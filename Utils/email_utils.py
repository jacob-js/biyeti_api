from django.core.mail import send_mail

def send_simple_mail(
    subject: str, to_email: str, message=None, from_email: str = 'Bookit App <info@bweteta.com>', html_message: str = None
):
    """
    Send a simple email
    """
    return send_mail(subject, message, from_email, [to_email], html_message=html_message)

def send_verification_code_email(user: dict, code: str):
    """
    Send a verification code email
    """
    subject = 'Code de vérification'
    html_message = f"""
        <p>Bonjour {user.get("firstname")} {user.get("lastname")},</p>
        Votre code de vérification est : <h2>{code}</h2> expire dans 15 minutes.
    """
    return send_simple_mail(subject, None, user.get("email"), html_message=html_message)
