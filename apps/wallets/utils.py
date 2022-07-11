from Utils.email_utils import send_simple_mail


def send_request_transfer_email():
    """
    Function to send email to the admin when an event admin request to be paid his money
    """
    title = "Money transfer request"
    receiver = "mercihabam@gmail.com"
    html_text = """
    <p>
        Hello dear
    </p>
    <p>
        You have a new transfer request, please go check this one into the admin panel
    </p>
    <p>
        Cheers </b>
        <div style="font-weight: bold">Biyeti Assistant</div>
    </p>
    """
    return send_simple_mail(title, to_email=receiver, html_message=html_text)
