import re
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all(), message="cet email est déjà")])
    date_of_birth = serializers.DateField(required=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'firstname', 'lastname', 'date_of_birth', 'gender', 'created_at', 'password']
        extra_kwargs = {
            'password': { 'write_only': True },
            'created_at': { 'read_only': True }
        }

    def validate(self, attrs):
        pwd = attrs.get('password')
        if len(pwd) < 6:
            raise serializers.ValidationError({ 'password': 'le mot de passe doit contenir au moins 6 caracteres' })
        if not re.findall('[a-zA-Z]', pwd):
            raise serializers.ValidationError({ 'password': 'Le mot de passe doit comporter au moins une lettre' })
        if not re.findall('[0-9]', pwd):
            raise serializers.ValidationError({ 'password': 'Le mot de passe doit comporter au moins un chiffre' })

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
            user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()