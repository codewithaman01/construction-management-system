from django.db import models
from accounts.models import User


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Task(models.Model):
    STATUS = [
        ('todo', 'Upcoming'),
        ('progress', 'In Progress'),
        ('done', 'Completed'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS, default='todo')