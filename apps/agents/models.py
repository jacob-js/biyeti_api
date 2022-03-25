from django.db import models

# Create your models here.
class Agent(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, default=None)
    role = models.CharField(max_length=255, default=None)

    def __str__(self):
        return '{} - {}'.format(self.user.firstname, self.event.name)