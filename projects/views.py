# ✅ FIXED — projects/views.py
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Project, Task
from accounts.models import User
from hr.models import Employee

# Charter says: max 6 tasks per Kanban column per project
KANBAN_TASK_LIMIT = 6


# ══════════════════════════════════════
# PROJECTS
# ══════════════════════════════════════

@login_required
def project_page(request):
    return render(request, 'projects/projects.html')


@login_required
def get_projects(request):
    projects = Project.objects.all()
    data = [{
        'id':          p.id,
        'name':        p.name,
        'description': p.description,
        'manager':     p.manager.username if p.manager else '',
        'start_date':  str(p.start_date),
        'end_date':    str(p.end_date),
        'status':      p.status,
    } for p in projects]
    return JsonResponse({'projects': data})


@login_required
@csrf_exempt
@require_POST
def create_project(request):
    data    = json.loads(request.body)
    manager = User.objects.get(id=int(data['manager']))
    Project.objects.create(
        name        = data['name'],
        description = data['description'],
        manager     = manager,
        start_date  = data['start_date'],
        end_date    = data['end_date'],
        status      = data['status'],
    )
    return JsonResponse({'status': 'created'})


@login_required
@csrf_exempt
@require_POST
def update_project(request):
    data    = json.loads(request.body)
    p       = Project.objects.get(id=data['id'])
    p.name        = data['name']
    p.description = data['description']
    p.manager     = User.objects.get(id=int(data['manager']))
    p.start_date  = data['start_date']
    p.end_date    = data['end_date']
    p.status      = data['status']
    p.save()
    return JsonResponse({'status': 'updated'})


@login_required
@csrf_exempt
@require_POST
def delete_project(request):
    data = json.loads(request.body)
    Project.objects.get(id=data['id']).delete()
    return JsonResponse({'status': 'deleted'})


# ══════════════════════════════════════
# TASKS
# ══════════════════════════════════════

@login_required
def task_page(request):
    return render(request, 'projects/tasks.html')


@login_required
def get_tasks(request):
    project_id = request.GET.get('project_id')
    tasks = Task.objects.select_related('project', 'assigned_to')
    if project_id:
        tasks = tasks.filter(project_id=project_id)

    data = [{
        'id':          t.id,
        'title':       t.title,
        'description': t.description or '',
        'project':     t.project.name,
        'project_id':  t.project.id,
        'employee':    t.assigned_to.name if t.assigned_to else '',
        'employee_id': t.assigned_to.id   if t.assigned_to else '',
        'status':      t.status,
        'start_date':  str(t.start_date)  if t.start_date else '',
        'end_date':    str(t.end_date)    if t.end_date   else '',
    } for t in tasks]
    return JsonResponse({'tasks': data})


@login_required
@csrf_exempt
@require_POST
def create_task(request):
    data    = json.loads(request.body)
    project = Project.objects.get(id=int(data['project']))
    status  = data.get('status', 'todo')

    # ✅ FIX: Enforce Kanban limit (charter: max 6 per column)
    existing = Task.objects.filter(project=project, status=status).count()
    if existing >= KANBAN_TASK_LIMIT:
        return JsonResponse(
            {'error': f'Maximum {KANBAN_TASK_LIMIT} tasks allowed in this column.'},
            status=400
        )

    employee = Employee.objects.get(id=int(data['employee'])) if data.get('employee') else None
    Task.objects.create(
        title       = data['title'],
        description = data.get('description', ''),
        project     = project,
        assigned_to = employee,
        status      = status,
        start_date  = data.get('start_date') or None,
        end_date    = data.get('end_date')   or None,
    )
    return JsonResponse({'status': 'created'})


@login_required
@csrf_exempt
@require_POST
def update_task(request):
    data       = json.loads(request.body)
    t          = Task.objects.get(id=data['id'])
    new_status = data.get('status', t.status)

    # ✅ FIX: Also enforce limit when MOVING a card to another column
    if new_status != t.status:
        existing = Task.objects.filter(project=t.project, status=new_status).count()
        if existing >= KANBAN_TASK_LIMIT:
            return JsonResponse(
                {'error': f'Maximum {KANBAN_TASK_LIMIT} tasks allowed in that column.'},
                status=400
            )

    t.title  = data.get('title', t.title)
    if data.get('project'):
        t.project = Project.objects.get(id=int(data['project']))
    if data.get('employee'):
        t.assigned_to = Employee.objects.get(id=int(data['employee']))
    t.status = new_status
    t.save()
    return JsonResponse({'status': 'updated'})


@login_required
@csrf_exempt
@require_POST
def delete_task(request):
    data = json.loads(request.body)
    Task.objects.get(id=data['id']).delete()
    return JsonResponse({'status': 'deleted'})


# ══════════════════════════════════════
# KANBAN BOARD
# ══════════════════════════════════════

@login_required
def kanban_page(request):
    # Pass column definitions to template
    columns = [
        ('todo',        'Upcoming',    'bg-slate-400'),
        ('in_progress', 'In Progress', 'bg-blue-400'),
        ('done',        'Completed',   'bg-green-400'),
    ]
    return render(request, 'projects/kanban.html', {'columns': columns})