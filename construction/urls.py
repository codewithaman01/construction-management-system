from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/',     admin.site.urls),
    path('',           include('accounts.urls')),
    path('dashboard/', include('core.urls')),
    path('projects/',  include('projects.urls')),
    path('tickets/',   include('tickets.urls')),
    path('hr/',        include('hr.urls')),
    path('store/',     include('store.urls')),
    path('chat/',      include('chat.urls')),
]