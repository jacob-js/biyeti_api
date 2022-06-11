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
    phone_number = models.CharField(max_length=255, null=False, unique=True)
    avatar = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    lat = models.FloatField(null=True)
    long = models.FloatField(null=True)
    username = None

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['email'], condition=Q(is_active=True), name='Email déjà utilisé'),
            UniqueConstraint(fields=['phone_number'], condition=Q(is_active=True), name='Numéro de téléphone déjà utilisé')
        ]