from django.urls import path
from . import views

urlpatterns = [
    path('', views.events_view),
    path('id/<uuid:event_id>', views.event_view),
    path('categorys', views.categorys_view),
    path('search', views.search_events_view),
]