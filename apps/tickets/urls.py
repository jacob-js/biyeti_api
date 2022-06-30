from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_event_ticket, name='tickets'),
    path('event/<uuid:event_id>/', views.get_event_tickets_view, name='tickets'),
    path('<uuid:id>/', views.TicketDetail.as_view(), name='ticket'),
    path('purchases/<uuid:event_id>', views.getPurchasesList),
    path('buy', views.createPurchase),
    path('user/<uuid:user_id>', views.get_user_tickets),
    path('status/<uuid:id>', views.check_ticket_status),
    path('sum', views.get_sum_of_purchases),
    path('scanned', views.get_scanned_tickets),
]