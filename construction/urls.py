from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('', include('accounts.urls')),

    # Dashboard
    path('dashboard/', include('core.urls')),

    # Project Module
    path('projects/', include('projects.urls')),

    # Ticket Module
    path('tickets/', include('tickets.urls')),
    path('hr/', include('hr.urls')),
    
]