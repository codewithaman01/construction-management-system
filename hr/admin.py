from django.contrib import admin
from .models import Employee, Attendance


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'role', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'email')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status')
    list_filter = ('status',)