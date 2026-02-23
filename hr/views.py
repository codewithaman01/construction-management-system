import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Employee
from django.views.decorators.csrf import csrf_exempt


def employee_page(request):
    return render(request, 'hr/employees.html')


def get_employees(request):
    query = request.GET.get('q', '')

    employees = Employee.objects.filter(name__icontains=query)

    data = list(employees.values())
    return JsonResponse({'employees': data})


@csrf_exempt
def add_employee(request):
    data = json.loads(request.body)

    if not data.get('role'):
        return JsonResponse({'error': 'Role is required'}, status=400)

    role = Role.objects.get(id=int(data['role']))

    Employee.objects.create(
        name=data['name'],
        email=data['email'],
        role=role
    )

    return JsonResponse({'status': 'added'})


@csrf_exempt
def update_employee(request):
    data = json.loads(request.body)

    emp = Employee.objects.get(id=data['id'])

    role = Role.objects.get(id=int(data['role']))  # 🔥 FIX

    emp.name = data['name']
    emp.email = data['email']
    emp.role = role

    emp.save()

    return JsonResponse({'status': 'updated'})


@csrf_exempt
def delete_employee(request):
    data = json.loads(request.body)

    Employee.objects.get(id=data['id']).delete()

    return JsonResponse({'status': 'deleted'})

def hr_dashboard(request):
    return render(request, 'hr/hrdashboard.html')

from accounts.models import Role

def get_roles(request):
    roles = Role.objects.all().values('id', 'name')
    return JsonResponse({'roles': list(roles)})