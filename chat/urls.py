from django.urls import path
from . import views

urlpatterns = [
    # Page
    path('',                        views.chat_home,     name='chat_home'),

    # Room APIs
    path('get-rooms/',              views.get_rooms),
    path('create-room/',            views.create_room),
    path('open-dm/',                views.open_dm),

    # Message APIs
    path('<int:room_id>/messages/', views.get_messages),
    path('<int:room_id>/send/',     views.send_message),

    # Users
    path('get-users/',              views.get_users),
]
