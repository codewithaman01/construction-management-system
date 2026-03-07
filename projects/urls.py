# ✅ FIXED — projects/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('',        views.project_page, name='project_page'),
    path('tasks/',  views.task_page,    name='task_page'),
    path('kanban/', views.kanban_page,  name='kanban_page'),  # ← was missing

    # Project APIs
    path('get-projects/',   views.get_projects,   name='get_projects'),
    path('create-project/', views.create_project, name='create_project'),
    path('update-project/', views.update_project, name='update_project'),
    path('delete-project/', views.delete_project, name='delete_project'),

    # Task APIs
    path('get-tasks/',   views.get_tasks,   name='get_tasks'),
    path('create-task/', views.create_task, name='create_task'),
    path('update-task/', views.update_task, name='update_task'),
    path('delete-task/', views.delete_task, name='delete_task'),
]