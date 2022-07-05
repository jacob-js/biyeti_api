from django.urls import path, include

urlpatterns = [
    path('/users/', include('apps.users.urls')),
    path('/tickets/', include('apps.tickets.urls')),
    path('/agents/', include('apps.agents.urls')),
    path('/events/', include('apps.events.urls')),
    path('/payments/', include('apps.payments.urls'))
]
