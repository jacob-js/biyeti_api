from django.urls import path

from apps.wallets.views import get_wallets

urlpatterns = [
    path('', get_wallets, name='get_wallets'),
]
