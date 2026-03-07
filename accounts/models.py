from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_constraint=False
    )

    def clean_fields(self, exclude=None):
        if exclude is None:
            exclude = set()
        else:
            exclude = set(exclude)

        exclude.add('role')   # correct for set

        super().clean_fields(exclude=exclude)