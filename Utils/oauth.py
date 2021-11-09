from google.oauth2 import id_token
from google.auth.transport import requests

class Google:

    @staticmethod
    def validate(auth_token):
        try:
            id_info = id_token.verify_oauth2_token(auth_token, requests.Request())
            if 'email' in id_info:
                return id_info
        except:
            return "le jeton est invalid"