from django.contrib import admin
from .models import Category, Ticket, Purchase, Event

# Register your models here.
admin.site.register(Ticket)
admin.site.register(Purchase)
admin.site.register(Event)
admin.site.register(Category)