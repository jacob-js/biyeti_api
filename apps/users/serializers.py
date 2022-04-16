import re
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator

from Utils.oauth import Google
from .models import User
from globals import config
from django.db.models import Q
import cloudinary.uploader

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.filter(is_active=True), message="Cet email existe déjà")]
    )
    phone_number= serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.filter(is_active=True), message="Ce numéro de téléphone existe déjà")]
    )
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': { 'write_only': True },
            'created_at': { 'read_only': True },
            'auth_provider': { 'read_only': True }
        }

    def validate(self, attrs: dict):
        pwd = attrs.get('password')
        if len(pwd) != 4:
            raise serializers.ValidationError({ 'password': 'le mot de passe doit contenir 4 caracteres' })
        if not re.match('[0-9]', pwd):
            raise serializers.ValidationError({ 'password': 'Le mot de passe doit contenir que des chiffres' })

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
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
        except:
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

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField()

class GoogleAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate(self, attrs):
        user_data = Google.validate(attrs.get('auth_token'))
        try:
            user_data['sub']
        except:
            print(user_data)
            raise serializers.ValidationError( 'le jeton est invalid' )
        attrs.setdefault('email', user_data['email'])
        attrs.setdefault('firstname', user_data['given_name'])
        attrs.setdefault('lastname', user_data['family_name'])
        attrs.setdefault('auth_provider', 'google')
        attrs.__delitem__('auth_token')

        print(attrs)
        return attrs