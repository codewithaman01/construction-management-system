# ✅ FIXED — tickets/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('',               views.ticket_page,          name='ticket_page'),
    path('track/',         views.track_tickets_page,   name='track_tickets'),   # ✅ new
    path('get/',           views.get_tickets,          name='get_tickets'),     # ✅ new
    path('save/',          views.save_ticket,          name='save_ticket'),
    path('update-status/', views.update_ticket_status, name='update_ticket_status'), # ✅ new
]