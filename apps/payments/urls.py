from django.urls import path
from . import views

urlpatterns = [
    path('initiate', views.initiate_payment),
    path('callback', views.callback),
]