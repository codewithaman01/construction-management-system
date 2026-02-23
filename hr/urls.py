from django.urls import path
from . import views

urlpatterns = [
    path('', views.hr_dashboard),  # 🔥 THIS FIXES /hr/
    
    path('employees/', views.employee_page),
    path('get-employees/', views.get_employees),
    path('add-employee/', views.add_employee),
    path('update-employee/', views.update_employee),
    path('delete-employee/', views.delete_employee),
    path('get-roles/', views.get_roles),
]