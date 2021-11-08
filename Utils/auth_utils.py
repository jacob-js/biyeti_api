import jwt, datetime
from apps.users.models import User
from globals.config import private_key
from rest_framework import permissions

def create_token(user_id):
    return jwt.encode({
        'user_id': user_id, 
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
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
                    user = User.objects.get(id=payload.get('user_id'))
                    if user is None:
                        return False
                    request.user = user
                    return True
                except:
                    return False
        except:
            return False