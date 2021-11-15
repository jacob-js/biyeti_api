from django.urls import path
from . import views

urlpatterns = [
    path('', views.AgentsView.as_view()),
    path('<int:id>', views.AgentDetailView.as_view())
]