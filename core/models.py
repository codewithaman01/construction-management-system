from django.db import models
from accounts.models import Role


class Module(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.url})"


class RolePermission(models.Model):
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        db_constraint=False
    )

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        db_constraint=False
    )

    def clean_fields(self, exclude=None):
        if exclude is None:
            exclude = set()
        else:
            exclude = set(exclude)

        # Skip Djongo FK validation
        exclude.add("role")
        exclude.add("module")

        super().clean_fields(exclude=exclude)