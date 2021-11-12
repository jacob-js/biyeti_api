from django.db import models

# Create your models here.
class Agent(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)