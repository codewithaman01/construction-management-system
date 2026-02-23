from django.db import models
from accounts.models import User, Role


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)  # 🔥 dynamic
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.role})"


class Attendance(models.Model):

    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('leave', 'Leave'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'date')  # 🔥 prevent duplicate

    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.status}"