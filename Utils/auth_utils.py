from apps.agents.models import Agent
import jwt, datetime
from apps.users.models import User
from globals.config import private_key
from rest_framework import permissions

def create_token(user_id):
    return jwt.encode({
        'user_id': user_id, 
        'exp': datetime.datetime.now() + datetime.timedelta(days=7),
        'iat': datetime.datetime.now()
    }, private_key )

class VerifyToken(permissions.BasePermission):
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

class VerifyAdmin(permissions.BasePermission):
    message = {'error': "Vous n'avez pas les droits pour effectuer cette action"}

    def has_permission(self, request, view):
        return request.user.is_superuser

class checkIsAgent(permissions.BasePermission):
    message = {'error': "Vous n'avez pas les droits pour effectuer cette action"}

    def has_permission(self, request, view):
        try:
            agent = Agent.objects.get(id=request.user.id)
            request.agent = agent
            return True
        except:
            return request.user.is_superuser