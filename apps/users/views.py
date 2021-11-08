from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from Utils.auth_utils import VerifyToken, create_token

from Utils.helpers import sendRes
from .models import User
from .serializers import LoginSerializer, UserSerializer

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        token = create_token(serializer.data.get('id'))
        return sendRes(status=status.HTTP_201_CREATED, data={ 'token': token, 'user': serializer.data }, msg='User created successfully')

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=request.data['email'])
            if user is not None:
                if user.check_password(request.data['password']):
                    ser = UserSerializer(user)
                    token = create_token(ser.data.get('id'))
                    return sendRes(status.HTTP_200_OK, data={'token': token, 'user': ser.data})
            return sendRes(status.HTTP_401_UNAUTHORIZED, "Email ou mot de passe incorrect")
        except:
            return sendRes(status.HTTP_401_UNAUTHORIZED, "Email ou mot de passe incorrect")

class GetLogedUser(APIView):
    permission_classes = [VerifyToken]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return sendRes(status.HTTP_200_OK, data=serializer.data)