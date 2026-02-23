from django.shortcuts import render, redirect
from core.models import RolePermission

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/')

    modules = RolePermission.objects.filter(
        role=request.user.role
    ).select_related('module')

    return render(request, 'dashboard.html', {
        'modules': modules
    })

from django.http import JsonResponse
from projects.models import Project, Task


def dashboard_data(request):
    project_count = Project.objects.count()
    task_count = Task.objects.count()

    return JsonResponse({
        'projects': project_count,
        'tasks': task_count
    })