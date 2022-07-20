from django.contrib import admin

from apps.wallets.models import TransferRequest, Wallet

# Register your models here.
admin.site.register(Wallet)
admin.site.register(TransferRequest)
