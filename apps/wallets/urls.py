from django.urls import path

from apps.wallets.views import execute_balance_transfer_request, get_event_wallet, get_wallets, request_wallet_balance_transfer

urlpatterns = [
    path('', get_wallets, name='get_wallets'),
    path('<uuid:event_id>/', get_event_wallet, name='get_event_wallet'),
    path('request-transfer/<uuid:event_id>', request_wallet_balance_transfer),
    path('execute-transfer/<uuid:request_id>', execute_balance_transfer_request)
]
