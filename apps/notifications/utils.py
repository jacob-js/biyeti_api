from exponent_server_sdk import (
    PushClient,
    PushMessage,
    PushServerError
)
from requests.exceptions import HTTPError


def send_push_message(token, title, message, extra=None):
    """
    Send a push message to a user.
    """
    try:
        PushClient().publish(
            PushMessage(to=token,
                        body=message,
                        data=extra,
                        title=title,
                        sound="default"
                    )
        )
    except PushServerError:
        pass
    except (ConnectionError, HTTPError):
        send_push_message(token, title, message, extra)
