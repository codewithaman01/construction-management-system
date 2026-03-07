from django.db import models
from accounts.models import User
from projects.models import Project


class Material(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('ton', 'Ton'),
        ('litre', 'Litre'),
        ('bag', 'Bag'),
        ('piece', 'Piece'),
    ]

    name = models.CharField(max_length=200, unique=True)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    reorder_level = models.FloatField(default=10)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Stock(models.Model):
    material = models.OneToOneField(Material, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.material.name} - {self.quantity}"


class StockInward(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.FloatField()
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)


class StockOutward(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.FloatField()
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)


class MaterialRequirement(models.Model):

    STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity_required = models.FloatField()
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    status = models.CharField(max_length=20, choices=STATUS, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # ✅ FIX