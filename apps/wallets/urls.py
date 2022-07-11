from django.urls import path

from apps.wallets.views import get_event_wallet, get_wallets

urlpatterns = [
    path('', get_wallets, name='get_wallets'),
    path('<uuid:event_id>/', get_event_wallet, name='get_event_wallet')
]
