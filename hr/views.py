# ✅ FIXED — hr/views.py
import json
from datetime import date
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Count
from .models import Employee, Attendance
from accounts.models import Role


# ── HR DASHBOARD ────────────────────────────────────
@login_required
def hr_dashboard(request):
    return render(request, 'hr/hrdashboard.html')


# ── EMPLOYEES ───────────────────────────────────────
@login_required
def employee_page(request):
    return render(request, 'hr/employees.html')


@login_required
def get_employees(request):
    query     = request.GET.get('q', '')
    employees = Employee.objects.filter(name__icontains=query).select_related('role')
    data = [{
        'id':        e.id,
        'name':      e.name,
        'email':     e.email,
        'role':      e.role.name if e.role else '',
        'role_id':   e.role.id   if e.role else '',
        'is_active': e.is_active,
    } for e in employees]
    return JsonResponse({'employees': data})


@login_required
@csrf_exempt
@require_POST
def add_employee(request):
    data = json.loads(request.body)
    if not data.get('role'):
        return JsonResponse({'error': 'Role is required'}, status=400)
    role = Role.objects.get(id=int(data['role']))
    Employee.objects.create(name=data['name'], email=data['email'], role=role)
    return JsonResponse({'status': 'added'})


@login_required
@csrf_exempt
@require_POST
def update_employee(request):
    data = json.loads(request.body)
    emp  = Employee.objects.get(id=data['id'])
    emp.name      = data['name']
    emp.email     = data['email']
    emp.role      = Role.objects.get(id=int(data['role']))
    emp.is_active = data.get('is_active', emp.is_active)
    emp.save()
    return JsonResponse({'status': 'updated'})


@login_required
@csrf_exempt
@require_POST
def delete_employee(request):
    data = json.loads(request.body)
    Employee.objects.get(id=data['id']).delete()
    return JsonResponse({'status': 'deleted'})


@login_required
def get_roles(request):
    roles = Role.objects.all().values('id', 'name')
    return JsonResponse({'roles': list(roles)})


# ── ATTENDANCE ──────────────────────────────────────
@login_required
def attendance_page(request):
    return render(request, 'hr/attendance.html')


@login_required
def get_attendance(request):
    today   = date.today()
    records = Attendance.objects.filter(date=today).select_related('employee')
    data = [{'employee': r.employee.name, 'employee_id': r.employee.id,
              'status': r.status} for r in records]
    return JsonResponse({'attendance': data})


@login_required
@csrf_exempt
@require_POST
def mark_attendance(request):
    data   = json.loads(request.body)
    emp_id = data.get('employee')
    status = data.get('status')
    if not emp_id or not status:
        return JsonResponse({'error': 'Missing data'}, status=400)
    emp = Employee.objects.get(id=int(emp_id))
    Attendance.objects.update_or_create(
        employee=emp, date=date.today(),
        defaults={'status': status, 'marked_by': request.user}
    )
    return JsonResponse({'status': 'saved'})


@login_required
def attendance_report_page(request):
    return render(request, 'hr/attendance_report.html')


@login_required
def get_attendance_report(request):
    date_filter = request.GET.get('date')
    employee    = request.GET.get('employee')
    records     = Attendance.objects.all().select_related('employee')
    if date_filter:
        records = records.filter(date=date_filter)
    if employee:
        records = records.filter(employee_id=employee)
    data = [{'employee': r.employee.name, 'date': str(r.date),
              'status': r.status} for r in records]
    return JsonResponse({'data': data})


@login_required
def attendance_dashboard_page(request):
    return render(request, 'hr/attendance_dashboard.html')


@login_required
def attendance_chart_data(request):
    month   = request.GET.get('month')
    records = Attendance.objects.all()
    if month:
        year, m = month.split('-')
        records = records.filter(date__year=year, date__month=m)
    status_data = records.values('status').annotate(count=Count('id'))
    pie_labels  = [s['status'] for s in status_data]
    pie_values  = [s['count']  for s in status_data]
    emp_data    = records.filter(status='present').values(
        'employee__name').annotate(count=Count('id'))
    bar_labels  = [e['employee__name'] for e in emp_data]
    bar_values  = [e['count']          for e in emp_data]
    return JsonResponse({
        'pie_labels': pie_labels, 'pie_values': pie_values,
        'bar_labels': bar_labels, 'bar_values': bar_values,
    })