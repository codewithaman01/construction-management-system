from django.urls import path
from .views import hr_dashboard, employee_page,add_employee

urlpatterns = [
    path('', hr_dashboard),
    path('employees/', employee_page),
    path('add-employee/', add_employee),
]