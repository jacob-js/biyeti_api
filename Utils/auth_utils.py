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

def create_reset_pwd_token(code: int) -> str:
    return jwt.encode({
        'code': code, 
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=30),
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

class CanUserChangeEntrys(permissions.BasePermission):
    message = {'error': "Erreur d'authentification"}
    
    def has_permission(self, request, view):
        if request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE':
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
    message = {'error': "Vous n'avez pas les droits pour effectuer cette action"}

    def has_permission(self, request, view):
        return request.user.is_superuser


class isAdminEditingData(permissions.BasePermission):
    message = {'error': "Vous n'avez pas les droits pour effectuer cette action"}
    
    def has_permission(self, request, view):
        if request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE':
            return request.user.is_superuser
        else:
            return True


class checkIsAgent(permissions.BasePermission):
    message = {'error': "Vous n'avez pas les droits pour effectuer cette action"}

    def has_permission(self, request, view):
        event_id = request.data.get('event_id') or request.query_params.get('event_id') or request.data['event']
        try:
            agent = Agent.objects.get(user=request.user.id, event=event_id)
            request.agent = agent
            return True
        except Exception as e:
            return False

class checkIsAgentEditingData(permissions.BasePermission):
    message = {'error': "Vous n'avez pas les droits pour effectuer cette action"}

    def has_permission(self, request, view):
        if request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE':
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
    message = {'error': "Vous n'avez pas les droits pour effectuer cette action"}

    def has_permission(self, request, view):
        return request.agent.role == 'admin'

class CheckIsEventAdminEditingData(permissions.BasePermission):
    message = {'error': "Vous n'avez pas les droits pour effectuer cette action"}

    def has_permission(self, request, view):
        if request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE':
            return request.agent.role == 'admin'
        else:
            return True