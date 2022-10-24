from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """Base model should be used for every future model in app"""
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Base model Meta class. Makes base model abstract"""
        abstract = True
