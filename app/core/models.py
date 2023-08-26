# Create your models here.
from django.db import models
from simple_history.models import HistoricalRecords
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    history = HistoricalRecords(inherit=True)

    class Meta:
        ordering = ["-created_at"]
        abstract = True
