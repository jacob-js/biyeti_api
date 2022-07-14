from django.urls import path

from .views import get_user_notifications

urlpatterns = [
    path('', get_user_notifications),
]
