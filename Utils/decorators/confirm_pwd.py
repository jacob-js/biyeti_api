from rest_framework import status
from Utils.helpers import sendRes


def check_pwd(view):
    """
    Check if the password is correct
    """
    def wrapper(request, *args, **kwargs):
        pwd = request.data.get('password', None)
        if(pwd is None):
            return sendRes(status.HTTP_400_BAD_REQUEST, error="Le mot de passe est obligatoire")
        if request.user.check_password(request.data['password']):
            return view(request, *args, **kwargs)
        return sendRes(status.HTTP_401_UNAUTHORIZED, "Le mot de passe est incorrect")
    return wrapper
    