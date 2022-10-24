from django.contrib.auth.models import User
from django.db import models

from intercars.models.base import BaseModel


class Account(BaseModel):
    """Account model class"""

    balance = models.DecimalField(default=0, decimal_places=2, max_digits=12)
    iban = models.CharField(max_length=28, unique=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=500)


class Transfer(BaseModel):
    """Money transfer between two accounts"""

    user = models.CharField(max_length=255, null=True, blank=True)
    source = models.CharField(max_length=28)
    destination = models.CharField(max_length=28)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
