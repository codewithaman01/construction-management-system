from django.shortcuts import render, redirect
from .models import Employee, Attendance


def hr_dashboard(request):
    if request.user.role.name != "HR Manager":
        return redirect('/dashboard/')

    return render(request, 'hr/dashboard.html')


def employee_page(request):
    employees = Employee.objects.all()
    return render(request, 'hr/employees.html', {'employees': employees})

import json
from django.http import JsonResponse


def add_employee(request):
    data = json.loads(request.body)

    Employee.objects.create(
        name=data['name'],
        email=data['email'],
        role=data['role']
    )

    return JsonResponse({'status': 'created'})