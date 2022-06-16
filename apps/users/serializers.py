import re
import cloudinary.uploader
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.db.models import Q

from Utils.oauth import Google
from Utils.imageUploader import cloudPhoto
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    User serializer class
    """
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Cet email existe déjà"
            )
        ]
    )
    phone_number= serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Ce numéro de téléphone existe déjà"
            )
        ]
    )
    class Meta: # pylint: disable=missing-class-docstring, too-few-public-methods
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': { 'write_only': True },
            'created_at': { 'read_only': True },
            'auth_provider': { 'read_only': True }
        }

    def validate(self, attrs: dict):
        pwd = attrs.get('password')
        if not re.match("^.*(?=.{8,})(?=.*\d)(?=.*[A-Za-z]).*$", pwd):
            raise serializers.ValidationError(
                { 
                    'password': 'Le mot de passe doit contenir au moins 8 caracteres inclus les chiffres et les lettres' 
                }
            )

        return attrs

    def create(self, validated_data: dict):
        password = validated_data.pop('password')
        validated_data.setdefault('is_active', True)
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        try:
            user = User.objects.get(~Q(id=instance.id), email=validated_data.get('email'))
            if user:
                raise serializers.ValidationError({ 'email': 'Cet email existe déjà' })
        except User.DoesNotExist:
            instance.email = validated_data.get('email', instance.email)
        try:
            user = User.objects.get(~Q(id=instance.id), phone_number=validated_data.get('phone_number'))
            if user:
                raise serializers.ValidationError({ 'email': 'Ce numéro de téléphone existe déjà' })
        except User.DoesNotExist:
            instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        except Exception: # pylint: disable=broad-except
            # if no phone number, do nothing
            pass

        # try processing avatar
        try:
            avatar = validated_data.pop('avatar', None)
            if avatar:
                res = cloudinary.uploader.upload(avatar)
                instance.avatar = res['url']
        except KeyError:
            # if no avatar, do nothing
            pass
        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.auth_provider = validated_data.get('gender', instance.auth_provider)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.city = validated_data.get('city', instance.city)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer): # pylint: disable=abstract-method
    """
    Login serializer, required fields: (identifier, password)
    """
    identifier = serializers.CharField()
    password = serializers.CharField()

class GoogleAuthSerializer(serializers.Serializer): # pylint: disable=abstract-method
    """
    Google login serializer
    """
    auth_token = serializers.CharField()

    def validate(self, attrs):
        user_data = Google.validate(attrs.get('auth_token'))
        try:
            user_data['sub']
        except Exception as exeception: # pylint: disable=broad-except
            raise serializers.ValidationError( 'le jeton est invalid' ) from exeception
        attrs.setdefault('email', user_data['email'])
        attrs.setdefault('firstname', user_data['given_name'])
        attrs.setdefault('lastname', user_data['family_name'])
        attrs.setdefault('auth_provider', 'google')
        attrs.__delitem__('auth_token')

        return attrs

class UpdatePwdSerializer(serializers.Serializer): # pylint: disable=abstract-method
    """
    Update password serializer
    """
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if not re.match("^.*(?=.{8,})(?=.*\d)(?=.*[A-Za-z]).*$", password):
            raise serializers.ValidationError({
                'error': 'Le mot de passe doit contenir au moins 8 caracteres inclus les chiffres et les lettres'
            })
        if password != confirm_password:
            raise serializers.ValidationError({
                'error': 'Les mots de passe ne correspondent pas'
            })

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance
