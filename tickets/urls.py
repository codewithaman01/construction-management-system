from django.urls import path
from .views import ticket_page, save_ticket

urlpatterns = [
    path('', ticket_page, name='ticket_page'),
    path('save/', save_ticket, name='save_ticket'),
]