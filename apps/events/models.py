from django.db import models
import uuid

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    cover = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='admin')
    name = models.CharField(max_length=255, null=False)
    cover = models.CharField(max_length=255)
    event_date = models.DateTimeField(null=False)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    location = models.CharField(max_length=255)
    long = models.FloatField(null=True)
    lat = models.FloatField(null=True)

    def __str__(self) -> str:
        return self.name

    def item(self) -> dict:
        return {
            'id': self.id,
            'created_at': self.created_at,
            'user': self.user.id,
            'name': self.name,
            'cover': self.cover,
            'event_date': self.event_date,
            'description': self.description,
            'category': self.category.id,
            'location': self.location,
            'long': self.long,
            'lat': self.lat
        }