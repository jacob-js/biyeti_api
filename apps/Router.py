from django.urls import path, include

urlpatterns = [
    path('/users/', include('apps.users.urls')),
    path('/tickets/', include('apps.tickets.urls')),
]