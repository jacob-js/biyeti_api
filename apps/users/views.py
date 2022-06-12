import datetime
from random import randint
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import permission_classes, api_view
from Utils.auth_utils import DecodeVerificationToken, VerifyAdmin, VerifyToken, create_verification_token, create_token
from Utils.email_utils import send_simple_mail

from Utils.helpers import sendRes
from Utils.pagination import Pagination
from Utils.sms import send_sms
from .models import User
from .serializers import GoogleAuthSerializer, LoginSerializer, UserSerializer

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
            user = User.objects.filter(Q(email=request.data['identifier']) | Q(phone_number=request.data['identifier'])).first()
            if user is not None:
                if user.check_password(request.data['password']):
                    ser = UserSerializer(user)
                    token = create_token(ser.data.get('id'))
                    return sendRes(status.HTTP_200_OK, data={'token': token, 'user': ser.data})
            return sendRes(status.HTTP_401_UNAUTHORIZED, "Email ou mot de passe incorrect")
        except Exception as e:
            print(e.__str__())
            return sendRes(status.HTTP_401_UNAUTHORIZED, "Email ou mot de passe incorrect")

class GoogleLoginView(APIView):
    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.filter(email=serializer.validated_data.get('email'), is_active=True).first()
            if user is not None:
                ser = UserSerializer(user)
                token = create_token(ser.data.get('id'))
                return sendRes(status.HTTP_200_OK, data={'token': token, 'user': ser.data})
            user = User.objects.create_user(password=str(datetime.datetime.utcnow()), **serializer.validated_data)
            ser = UserSerializer(user)
            token = create_token(ser.data.get('id'))
            return sendRes(status.HTTP_202_ACCEPTED, msg='User created successfully', data={'token': token, 'user': ser.data})
        except Exception as e:
            return sendRes(status.HTTP_500_INTERNAL_SERVER_ERROR, error=e.__str__())

class GetLogedUser(APIView):
    permission_classes = [VerifyToken]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return sendRes(status.HTTP_200_OK, data=serializer.data)


class UserAdminView(viewsets.ViewSet):
    permission_classes = [VerifyToken, VerifyAdmin]
    serializer_class = UserSerializer

    def list(self, request):
        users = User.objects.filter(is_active=True).order_by('-created_at')
        paginator = Pagination()
        results = paginator.paginate_queryset(users, request)
        serializer = self.serializer_class(results, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(id=pk, is_active=True)
        except User.DoesNotExist:
            print('retrieve', request.method)
            return sendRes(status.HTTP_404_NOT_FOUND, "Utilisateur introuvable")

        serializer = self.serializer_class(user)
        return sendRes(status.HTTP_200_OK, data=serializer.data)

    def destroy(self, request, pk=None):
        try:
            print('delete')
            user = User.objects.get(id=pk, is_active=True)
        except User.DoesNotExist:
            print('delete', request.method)
            return sendRes(status.HTTP_404_NOT_FOUND, "Utilisateur introuvable")
        user.is_active = False
        user.save()
        serializer = self.serializer_class(user)
        return sendRes(status.HTTP_200_OK, data=serializer.data, msg="Utilisateur supprimé")

class ProfileView(APIView):
    permission_classes = [VerifyToken]
    serializer_class = UserSerializer

    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id, is_active=True)
            serializer = UserSerializer(user)
            return sendRes(status.HTTP_200_OK, data=serializer.data)
        except User.DoesNotExist:
            return sendRes(status.HTTP_404_NOT_FOUND, "Utilisateur introuvable")

    def put(self, request):
        try:
            user = User.objects.get(id=request.user.id, is_active=True)
            serializer = UserSerializer(user)
            serializer.update(user, request.data)
            return sendRes(status.HTTP_200_OK, data=serializer.data, msg="Modification enregistrée")
        except User.DoesNotExist:
            return sendRes(status.HTTP_404_NOT_FOUND, "Utilisateur introuvable")

class PasswordResetView(APIView):

    def get(self, request, phone):
        code = randint(1000, 10000)
        try:
            send_sms(phone, 'Votre code de confirmation est: {}'.format(code))
            token = create_verification_token(code)
            return sendRes(200, data={'token': token}, msg='Code de confirmation envoyé')
        except Exception as exception:
            return sendRes(500, error=exception.__str__())

@api_view(['GET'])
def send_verification_code_view(_, identifier):
    """
    send verification code view
    """
    code = randint(1000, 10000)
    try:
        token = create_verification_token(code)
        send_simple_mail("Code de vérification", f'Votre code de vérification est: {code}', identifier)
        return sendRes(200, data={'token': token}, msg='Code de vérification envoyé')
    except Exception as exception:
        return sendRes(500, error=exception.__str__())

@api_view(['POST'])
@permission_classes([DecodeVerificationToken])
def verify_verification_code_view(_):
    """
    verify verification code view
    """
    return sendRes(200, msg='Code de vérification validé')
