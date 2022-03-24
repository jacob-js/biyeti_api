from django.urls import path
from . import views

urlpatterns = [
    path('', views.events_view),
    path('<uuid:event_id>/', views.event_view),
    path('categorys', views.categorys_view),
]