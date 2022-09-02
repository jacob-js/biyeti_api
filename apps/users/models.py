from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid

from django.db.models.constraints import UniqueConstraint
from django.db.models.query_utils import Q

# Create your models here.
class UserManager(BaseUserManager):
    use_in_migration = True
    def _create_user(self, email, password, **extra):
        if not email:
            raise ValueError("l'adresse mail est obligatoire")
        if not password:
            raise ValueError("le mot de passe est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra):
        extra['is_staff'] = False
        extra['is_superuser'] = False
        return self._create_user(email, password, **extra)

    def create_superuser(self, email, password, **extra):
        extra['is_staff'] = True
        extra['is_superuser'] = True
        return self._create_user(email, password, **extra)

class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    email = models.EmailField(unique=True, null=False, blank=False)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    password = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=255, null=True)
    date_of_birth = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    auth_provider = models.CharField(max_length=255, default='pwd')
    phone_number = models.CharField(max_length=255, null=True)
    avatar = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    notif_token = models.CharField(max_length=500, null=True, blank=True)
    lat = models.FloatField(null=True)
    long = models.FloatField(null=True)
    username = None

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['email'], condition=Q(is_active=True), name='Email déjà utilisé')
        ]

    def item(self) -> dict:
        return {
            'id': str(self.id),
            'email': self.email,
            'firstname': self.first_name,
            'lastname': self.lastname,
            'gender': self.gender,
            'date_of_birth': str(self.date_of_birth),
            'phone_number': self.phone_number,
            'avatar': self.avatar,
            'city': self.city,
            'lat': self.lat,
            'long': self.long,
            'created_at': str(self.created_at)
        }