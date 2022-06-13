import jwt, datetime
from rest_framework import permissions
from apps.users.models import User
from apps.agents.models import Agent
from globals.config import private_key

def create_token(user_id):
    """
    Providing a user_id, this function create a token that will be used to authenticate the user
    """
    return jwt.encode({
        'user_id': user_id, 
        'exp': datetime.datetime.now() + datetime.timedelta(days=7),
        'iat': datetime.datetime.now()
    }, private_key )

def create_signup_token(code: int, data) -> str:
    """
    Providing a verification code and user data, this function create a token that will be used to create a user
    """
    return jwt.encode({
        'code': code,
        'user_data': data,
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=15) - datetime.timedelta(hours=2),
        'iat': datetime.datetime.now(),
    }, private_key )

class DecodeSignupToken(permissions.BasePermission):
    """
    Decode signup Token
    """
    message = { "error": "Code de vérification incorrect" }

    def has_permission(self, request, view):
        try:
            token = request.headers['signuptoken']
            decoded = jwt.decode(token, private_key, algorithms=['HS256'])
            input_code = request.data.get('code')
            if str(input_code) == str(decoded['code']):
                request.user_data = decoded['user_data']
                return True
            return False
        except:
            return False

def create_verification_token(code: int, extra: dict or None = None) -> str:
    """
    Providing a code, this function create a token that will be used to verify the user
    """
    return jwt.encode({
        'code': code, 
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=15) - datetime.timedelta(hours=2),
        'iat': datetime.datetime.now(),
        **(extra or {})
    }, private_key )

class DecodeVerificationToken(permissions.BasePermission):
    """
    This class is used to verify the code sent by the user if is match with the code in the token
    """
    message = { 'error': "Code de vérification incorrecte" }
    def has_permission(self, request, view):
        try:
            token = request.headers['verificationtoken']
            if not token:
                print('no token')
                return False
            decoded_token: dict = jwt.decode(token, private_key, algorithms=['HS256'])
            reset_pwd = decoded_token.get('reset_pwd', None)

            # if the token is for reseting the password
            if reset_pwd:
                if request.method == 'PUT':
                    request.user_id = decoded_token['user_id']
                    return True
            sent_code = decoded_token['code']
            return str(sent_code) == str(request.data['code'])
        except:
            return False

class VerifyToken(permissions.BasePermission):
    """
    This class is used to verify the token sent by the user in order to authenticate him
    """
    message = {'error': "Erreur d'authentification"}
    
    def has_permission(self, request, view):
        try:
            token = request.headers['authtoken']
            if not token:
                return False
            else:
                try:
                    payload = jwt.decode(token, private_key, algorithms=['HS256'])
                    user = User.objects.get(id=payload.get('user_id'), is_active=True)
                    if user is None:
                        return False
                    request.user = user
                    return True
                except:
                    return False
        except:
            return False

class CanUserChangeEntrys(permissions.BasePermission):
    """
    This class is used to check if user is authenticated before changing the data in the database
    """
    message = {'error': "Erreur d'authentification"}
    
    def has_permission(self, request, view):
        if request.method in ('POST', 'PUT', 'DELETE'):
            try:
                token = request.headers['authtoken']
                if not token:
                    return False
                else:
                    try:
                        payload = jwt.decode(token, private_key, algorithms=['HS256'])
                        user = User.objects.get(id=payload.get('user_id'), is_active=True)
                        if user is None:
                            return False
                        request.user = user
                        return True
                    except:
                        return False
            except:
                return False
        else:
            return True

class VerifyAdmin(permissions.BasePermission):
    """
    This class is used to verify if the user is an admin
    """
    message = {'error': "Vous n'avez pas les droits pour effectuer cette action"}

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAdminEditingData(permissions.BasePermission):
    """
    This class is used to verify if the user is an admin before changing the data in the database
    """
    message = {'error': "Vous n'avez pas les droits pour effectuer cette action"}
    
    def has_permission(self, request, view):
        if request.method in ('POST', 'PUT', 'DELETE'):
            return request.user.is_superuser
        else:
            return True


class CheckIsAgent(permissions.BasePermission):
    """
    This class is used to verify if the authenticated user is an agent before accessing the api
    """
    message = {'error': "Vous n'avez pas les droits pour effectuer cette action"}

    def has_permission(self, request, view):
        event_id = request.data.get('event_id') or request.query_params.get('event_id') or request.data['event']
        try:
            agent = Agent.objects.get(user=request.user.id, event=event_id)
            request.agent = agent
            return True
        except:
            return False

class CheckIsAgentEditingData(permissions.BasePermission):
    """
    This class is used to verify if the user is an agent before changing the data in the database
    """
    message = {'error': "Vous n'avez pas les droits pour effectuer cette action"}

    def has_permission(self, request, view):
        if request.method in ('POST', 'PUT', 'DELETE'):
            try:
                event_id = request.data.get('event_id') or request.query_params.get('event_id') or request.data['event']
                agent = Agent.objects.get(user=request.user.id, event=event_id)
                request.agent = agent
                return True
            except:
                return False
        else:
            return True

class CheckIsEventAdmin(permissions.BasePermission):
    """
    This class is used to verify if the authenticated user is an event admin before accessing the api
    """
    message = {'error': "Vous n'avez pas les droits pour effectuer cette action"}

    def has_permission(self, request, view):
        return request.agent.role == 'admin'

class CheckIsEventAdminEditingData(permissions.BasePermission):
    """
    This class is used to verify if the authenticated user is an event admin before changing the data in the database
    """
    message = {'error': "Vous n'avez pas les droits pour effectuer cette action"}

    def has_permission(self, request, view):
        if request.method in ('POST', 'PUT', 'DELETE'):
            return request.agent.role == 'admin'
        return True
