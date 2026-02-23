from django.db import models
from accounts.models import Role


class Module(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)