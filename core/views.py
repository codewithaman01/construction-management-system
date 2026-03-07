from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from core.models import RolePermission
from projects.models import Project, Task
from hr.models import Employee
from tickets.models import Ticket


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import RolePermission
from projects.models import Project, Task
from hr.models import Employee
from tickets.models import Ticket


@login_required
def dashboard(request):

    # allowed modules
    permissions = RolePermission.objects.filter(role=request.user.role)
    modules = [p.module for p in permissions]

    # safe counts
    total_projects = len(list(Project.objects.all()))
    total_tasks = len(list(Task.objects.all()))

    employees = list(Employee.objects.all())
    total_employees = len([e for e in employees if e.is_active])

    tickets = list(Ticket.objects.all())
    open_tickets = len([t for t in tickets if t.status == "Open"])

    context = {
        "modules": modules,
        "total_projects": total_projects,
        "total_tasks": total_tasks,
        "total_employees": total_employees,
        "open_tickets": open_tickets,
    }

    return render(request, "dashboard.html", context)


@login_required
def dashboard_data(request):

    data = {
        "projects": len(list(Project.objects.all())),
        "tasks": len(list(Task.objects.all())),
        "employees": len(list(Employee.objects.filter(is_active=True))),
        "tickets": len(list(Ticket.objects.filter(status="Open"))),
    }

    return JsonResponse(data)