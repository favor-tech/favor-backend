from .base import BaseModel
from django.db import models
from .definitions.DateTimeWithoutTZ import DateTimeWithoutTZField as DateTimeField
from django.conf import settings
from django.utils import timezone

class Notification(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField()
    read_at = DateTimeField(null=True, blank=True)
    redirect_url = models.URLField(max_length=500, null=True, blank=True)
    sent_at = DateTimeField(default=timezone.now)
    class Meta:
        db_table = "notification"
        ordering = ["-sent_at"]