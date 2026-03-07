from django.db import models
from accounts.models import User
from hr.models import Employee


# ==============================
# 📁 PROJECT MODEL
# ==============================
class Project(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    )

    name = models.CharField(max_length=200)
    description = models.TextField()

    # 👤 Project Manager (User)
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='managed_projects'
    )

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ==============================
# 📌 TASK MODEL
# ==============================
class Task(models.Model):

    STATUS_CHOICES = (
        ('todo', 'Upcoming'),
        ('in_progress', 'In Progress'),
        ('done', 'Completed'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    # 🔗 Link to Project
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    # 👷 Assigned Employee
    assigned_to = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='todo'
    )

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title