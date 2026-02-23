from django.db import models
from accounts.models import User


class Ticket(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_data = models.TextField()  # base64 image
    status = models.CharField(max_length=50, default='Open')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)