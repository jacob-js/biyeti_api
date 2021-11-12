from django.urls import path
from . import views

urlpatterns = [
    path('', views.TicketsView.as_view(), name='tickets'),
    path('<uuid:id>/', views.TicketDetail.as_view(), name='ticket'),
    path('places', views.PlacesView.as_view()),
    path('places/<int:id>', views.PlaceDetailView.as_view()),
    path('purchases', views.getPurchasesList),
    path('buy', views.createPurchase),
    path('user/<uuid:user_id>', views.get_user_tickets),
    path('status/<uuid:id>', views.check_ticket_status)
]