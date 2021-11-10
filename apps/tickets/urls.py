from django.urls import path
from . import views

urlpatterns = [
    path('', views.TicketsView.as_view(), name='tickets'),
    path('<uuid:id>/', views.TicketDetail.as_view(), name='ticket'),
]