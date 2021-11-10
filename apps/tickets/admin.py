from django.contrib import admin
from .models import Ticket, Place, Purchase

# Register your models here.
admin.site.register(Ticket)
admin.site.register(Place)
admin.site.register(Purchase)