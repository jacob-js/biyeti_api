from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid

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
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    username = None

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserManager()