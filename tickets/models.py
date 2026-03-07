# ✅ FIXED — tickets/models.py
from django.db import models
from accounts.models import User


class Ticket(models.Model):
    STATUS_CHOICES = (
        ('Open',        'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved',    'Resolved'),
        ('Closed',      'Closed'),
    )

    title       = models.CharField(max_length=200)
    description = models.TextField()
    image_data  = models.TextField(blank=True, null=True)   # base64 photo preview
    latitude    = models.FloatField(null=True, blank=True)  # ✅ GPS latitude
    longitude   = models.FloatField(null=True, blank=True)  # ✅ GPS longitude
    status      = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Open')
    created_by  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    created_at  = models.DateTimeField(auto_now_add=True)   # ✅ timestamp
    updated_at  = models.DateTimeField(auto_now=True)       # ✅ last updated

    def __str__(self):
        return f"#{self.id} — {self.title} [{self.status}]"