from .base import BaseModel
from django.db import models
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField

class Notification(BaseModel):
    user = models.ForeignKey("User",on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField()
    read_at = DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "notification"