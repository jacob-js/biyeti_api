from django.urls import path

from .views import get_user_notifications, notification_detail

urlpatterns = [
    path('', get_user_notifications),
    path('<int:notif_id>/', notification_detail)
]
