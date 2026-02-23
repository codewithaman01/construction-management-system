from django.shortcuts import render
from django.http import JsonResponse
from .models import Project, Task
import json


def project_page(request):
    return render(request, 'projects/kanban.html')


def get_tasks(request):
    tasks = Task.objects.values()
    return JsonResponse({'tasks': list(tasks)})


def create_task(request):
    data = json.loads(request.body)

    Task.objects.create(
        title=data['title'],
        project_id=data['project_id']
    )

    return JsonResponse({'status': 'created'})


def update_task(request):
    data = json.loads(request.body)

    task = Task.objects.get(id=data['id'])
    task.status = data['status']
    task.save()

    return JsonResponse({'status': 'updated'})