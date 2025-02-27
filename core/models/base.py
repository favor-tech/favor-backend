import uuid
from django.db import models
from django.utils import timezone
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = DateTimeField(editable=False, default=timezone.now)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True 