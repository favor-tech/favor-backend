import uuid
from django.db import models
from django.utils import timezone
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField

class SoftDeleteModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = DateTimeField(editable=False, default=timezone.now)
    updated_at = DateTimeField(null=True)
    deleted_at = DateTimeField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True
