from django.urls import path
from .views import project_page, get_tasks, create_task, update_task

urlpatterns = [
    path('', project_page),
    path('tasks/', get_tasks),
    path('create-task/', create_task),
    path('update-task/', update_task),
]