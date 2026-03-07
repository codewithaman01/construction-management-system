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
    path('attendance/', views.attendance_page),
    path('get-attendance/', views.get_attendance),
    path('mark-attendance/', views.mark_attendance),
    path('attendance-report/', views.attendance_report_page),
    path('get-attendance-report/', views.get_attendance_report),
    path('attendance-chart-data/', views.attendance_chart_data),
    path('attendance-dashboard/', views.attendance_dashboard_page),
]